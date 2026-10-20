#requires -Version 5.1
[CmdletBinding()]
param(
    [ValidateSet('Setup', 'Check', 'Serve', 'Status', 'Sync', 'NewBranch')]
    [string] $Action = 'Status',
    [string] $BranchName = ''
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $root

function Require-Tool([string] $Name) {
    $found = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $found) {
        throw "Required tool '$Name' was not found. Install it, restart PowerShell, and retry."
    }
}
function Run([string] $Program, [string[]] $Arguments) {
    Write-Host "=> $Program $($Arguments -join ' ')"
    $saved = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & $Program @Arguments
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $saved
    }
    if ($exitCode -ne 0) { throw "$Program exited $exitCode" }
}
function Git-Value([string[]] $Arguments) {
    $saved = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $result = & git @Arguments 2>&1
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $saved
    }
    if ($exitCode -ne 0) { throw "Git $($Arguments -join ' ') failed: $($result | Out-String)" }
    return ($result | Out-String).Trim()
}
function Assert-Clean {
    $changes = Git-Value -Arguments @('status', '--porcelain')
    if ($changes) { throw "Uncommitted files found. Commit/stash them manually first; no files were discarded.`n$changes" }
}
function Sync-Main {
    Assert-Clean
    $branch = Git-Value -Arguments @('branch', '--show-current')
    if ($branch -ne 'main') { throw "Sync requires main; current branch is '$branch'. Switch safely to main first." }
    Run -Program 'git' -Arguments @('fetch', 'origin', 'main')
    Run -Program 'git' -Arguments @('merge', '--ff-only', 'origin/main')
    Write-Host 'WINDOWS_SYNC_FAST_FORWARD=PASS'
}

try {
    Require-Tool 'git'
    $repoRoot = Git-Value -Arguments @('rev-parse', '--show-toplevel')
    if ([IO.Path]::GetFullPath($repoRoot).TrimEnd('\', '/') -ne [IO.Path]::GetFullPath($root).TrimEnd('\', '/')) {
        throw "Script must run inside its own Git repository. Git=$repoRoot; Script=$root"
    }
    switch ($Action) {
        'Status' {
            Run -Program 'git' -Arguments @('status', '-sb')
            Run -Program 'git' -Arguments @('log', '-1', '--oneline')
        }
        'Sync' { Sync-Main }
        'NewBranch' {
            if (-not $BranchName) { throw "NewBranch requires -BranchName, e.g. -BranchName 'feature/m1-geometry'." }
            if ($BranchName -notmatch '^(feature|fix|docs|m[0-6])/[a-zA-Z0-9][a-zA-Z0-9/_-]*$') {
                throw 'BranchName must begin feature/, fix/, docs/, or m0/..m6/, followed by simple letters, numbers, /, _ or -.'
            }
            Run -Program 'git' -Arguments @('check-ref-format', '--branch', $BranchName)
            Sync-Main
            Run -Program 'git' -Arguments @('switch', '-c', $BranchName)
            Write-Host "WINDOWS_BRANCH_CREATED=$BranchName"
        }
        { $_ -in @('Setup', 'Check', 'Serve') } {
            Require-Tool 'node'
            Require-Tool 'npm.cmd'
            $version = (& node --version).TrimStart('v')
            if ($LASTEXITCODE -ne 0 -or [version]$version -lt [version]'22.12.0') {
                throw "Node.js >=22.12.0 required; current: $version"
            }
            if ($Action -eq 'Setup') { Run -Program 'npm.cmd' -Arguments @('ci', '--no-audit', '--no-fund') }
            if ($Action -eq 'Check' -or $Action -eq 'Setup') {
                if (-not (Test-Path -LiteralPath (Join-Path $root 'node_modules'))) {
                    throw 'Dependencies not installed; run -Action Setup first.'
                }
                Run -Program 'npm.cmd' -Arguments @('run', 'verify:quick')
                Write-Host 'WINDOWS_LOCAL_VERIFY=PASS'
            } else {
                if (-not (Test-Path -LiteralPath (Join-Path $root 'node_modules'))) {
                    throw 'Dependencies not installed; run -Action Setup first.'
                }
                Run -Program 'npm.cmd' -Arguments @('run', 'dev', '--', '--host', '127.0.0.1')
            }
        }
    }
} catch {
    [Console]::Error.WriteLine("WINDOWS_DEV=FAIL ACTION=$Action ERROR=$($_.Exception.Message)")
    exit 1
}
