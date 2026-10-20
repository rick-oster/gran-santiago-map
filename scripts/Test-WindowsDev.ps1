#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$targets = @(
    (Join-Path $PSScriptRoot 'Windows-Dev.ps1'),
    $PSCommandPath
)

try {
    foreach ($path in $targets) {
        $tokens = $null
        $errors = $null
        [void][System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$errors)
        if ($errors.Count -ne 0) {
            throw "PowerShell parser rejected $path : $($errors | Out-String)"
        }
    }
    Write-Host 'DUAL_DEVICE_POWERSHELL_SYNTAX=PASS'

    $script = Get-Content -LiteralPath $targets[0] -Raw
    foreach ($required in @('ff-only', 'Assert-Clean', 'NewBranch', 'verify:quick', 'npm.cmd', '127.0.0.1')) {
        if (-not $script.Contains($required)) { throw "Missing required safe-operation contract: $required" }
    }
    Write-Host 'DUAL_DEVICE_SAFE_GIT_CONTRACT=PASS'

    # Git may check out text using CRLF on Windows even when the committed
    # specification uses LF. Normalize *in memory* only, preserving the file.
    # Strict UTF-8 and rejection of bare CR protect the canonical content.
    $frozen = Join-Path $root 'docs/V1_SPEC.md'
    $raw = [System.IO.File]::ReadAllBytes($frozen)
    $strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
    $text = $strictUtf8.GetString($raw)
    $canonical = $text.Replace("`r`n", "`n")
    if ($canonical.Contains("`r")) { throw 'Frozen spec contains unexpected bare CR bytes.' }
    $canonicalBytes = $strictUtf8.GetBytes($canonical)
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try {
        $actual = ([BitConverter]::ToString($hasher.ComputeHash($canonicalBytes))).Replace('-', '').ToLowerInvariant()
    } finally {
        $hasher.Dispose()
    }
    $expected = 'eec81bb8e7ffa8af5522fd26b37b1cfd47b9cda0ec5095ebe4da8d55e93feddd'
    if ($actual -ne $expected) { throw "Frozen spec canonical SHA256 changed: $actual" }
    Write-Host 'DUAL_DEVICE_FROZEN_SPEC=PASS'
    Write-Host 'DUAL_DEVICE_WINDOWS_TOOLING=PASS'
} catch {
    [Console]::Error.WriteLine("DUAL_DEVICE_WINDOWS_TOOLING=FAIL $($_.Exception.Message)")
    exit 1
}
