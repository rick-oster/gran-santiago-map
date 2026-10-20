# Gran Santiago Map V1 — M0 Windows bootstrap (R3)

**Purpose:** Automate the Windows bootstrap so development can subsequently be done entirely from Android. The approved V1 specification and M0 source are unchanged. The app is **not** yet the real map; M1 must first validate official geographic boundaries.

## R3 correction: reuse an already installed GitHub CLI

Observed Windows 11 result from R2:

```text
winget install --id GitHub.cli ...
Found an existing package already installed. Trying to upgrade the installed package...
No available upgrade found.
M0_WINDOWS_SETUP=FAIL STEP=INSTALL_TOOLS
ERROR=winget exited -1978335189 during INSTALL_TOOLS
```

The failure was caused by the script reading a stale process `PATH` after the first installation, concluding `gh` was missing, and repeating an unnecessary WinGet install. WinGet correctly reported that no update was available but returned a nonzero exit code. **The installed program should be reused, not reinstalled.**

R3 fixes this by:

- Refreshing persistent machine/user `PATH` **before** checking tools, not only after installation.
- Looking for `gh.exe` in WinGet user alias (`%LOCALAPPDATA%\Microsoft\WinGet\Links`) and installed package (`%LOCALAPPDATA%\Microsoft\WinGet\Packages\GitHub.cli_*`) locations.
- Running WinGet only when its `gh` executable cannot be found. After WinGet, accept an already-installed/no-upgrade result **only if `gh` can actually be located**. Do not count a failed install as success without positive evidence.
- Preserving R1's deferred `$PSScriptRoot` resolution and R2's nonfatal first-login probes.
- Allowing `-Resume` of a **verified M0 working tree**, even if a failed npm/build attempt left a new uncommitted lockfile; no `git reset`, `git clean`, destructive overwrite, or force push.

In the latest user-supplied failure, no repository or working directory was created. **Do not pass `-Resume` for that run.**

## Automatic installation (Windows 11, normal PowerShell)

Download **`Gran_Santiago_Map_M0_Windows_Automation_R3.zip`** to Downloads. Then:

```powershell
$ErrorActionPreference = 'Stop'
$zip = "$HOME\Downloads\Gran_Santiago_Map_M0_Windows_Automation_R3.zip"
$setup = "$HOME\Downloads\GranSantiago-M0-Setup"

# Preserve your existing setup and replace only files in this bootstrap package.
Expand-Archive -LiteralPath $zip -DestinationPath $setup -Force

# Check PowerShell parse, R1/R2/R3 regressions, ZIP integrity and frozen spec.
& powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "$setup\Test-GranSantiago-M0-Package.ps1"
if ($LASTEXITCODE -ne 0) { throw 'M0 package verification failed.' }

# Start; permits only user-scoped ordinary tool installs when genuinely missing.
& powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "$setup\Start-GranSantiago-M0.ps1" `
  -PublicRepository -InstallMissingTools
if ($LASTEXITCODE -ne 0) { throw 'M0 bootstrap failed. Use the printed STEP and receipt.' }
```

**Authorization:** `-PublicRepository` explicitly approves publishing the `gran-santiago-map` source publicly. `-InstallMissingTools` permits user-scope tool installations through WinGet if a tool is genuinely missing. The script never silently requests elevation. If GitHub CLI needs authentication, authorize `gh auth login` in your browser. Do not paste access tokens into chats or files.

On systems with F:, the default project path is `F:\Projects\GranSantiagoMap`; otherwise it is `%USERPROFILE%\Projects\GranSantiagoMap`. To use another folder, add `-ProjectRoot 'D:\Projects\GranSantiagoMap'` to the invocation.

## Expected preflight markers

```text
M0_INSTALLER_SYNTAX=PASS
M0_R1_PS51_PATH_FIX=PASS
M0_R2_PS51_AUTH_PROBES=PASS
M0_R3_WINGET_REUSE_CONTRACT=PASS
M0_R3_SAFE_RESUME_CONTRACT=PASS
M0_FROZEN_SPEC_IN_ARCHIVE=PASS
```

Expected script start:

```text
M0_INSTALLER_REVISION=R3_WINGET_REUSE
[TOOLS] Checking Git, Node.js, npm and GitHub CLI.
TOOLS=PASS Node=<installed version>
[VERIFY_ZIP] ...
SOURCE_SPEC_SHA256=PASS
[AUTH] Checking GitHub CLI authentication.
```

An authenticated GitHub CLI will be reused. Otherwise authorize sign-in once. If WinGet's portable GitHub CLI executable is found, it is added only to **the script process's** `PATH`; no system setting needs changing.

The rest of the successful run (actual outcomes must be observed, not inferred) prints:

```text
M0_WINDOWS_LOCAL_STATIC_UNIT_BUILD=PASS
PUSHED_COMMIT=<actual SHA>
CI_RUN=https://github.com/<account>/gran-santiago-map/actions/runs/<actual ID>
M0_CLOUD_CI_DEPLOY=PASS
M0_PAGES_HTTP=PASS https://<account>.github.io/gran-santiago-map/
M0_BRANCH_CHECKS=PASS validate
M0_WINDOWS_SETUP=PASS
M0_GATE=NOT_YET_PASSED (requires Android-only edit/commit and published-update observation)
```

The script checks source integrity, creates the public repository, configures Pages, clones it, installs npm dependencies, tests/builds it, commits/pushes, reads exact GitHub CI receipts, verifies published HTML/JS, and applies branch protection only after green CI. Remote calls, npm install, and deployment may fail independently; they are not guaranteed by package validation.

Failures produce `M0_WINDOWS_SETUP=FAIL STEP=...`, `ERROR=...`, and a JSON receipt initially at `%TEMP%\GranSantiagoM0-Evidence\windows-m0-bootstrap.json`, or in `evidence\windows-bootstrap` after the project directory is prepared.

### If a future retry is needed

- **Failure before repository creation:** rerun the command without `-Resume`.
- **Failure after repository creation:** `-Resume` is appropriate **only** for the new M0 repository created by this bootstrap. It verifies origin, default branch and frozen specification. It never discards existing source changes. Use the same `-ProjectRoot` if customized.
- **Never** delete a directory or force push merely to make a retry work.

## Mandatory final M0 acceptance from Android

The Windows setup is **not** the full milestone gate. From Android, open the printed `https://github.dev/<account>/gran-santiago-map` link, edit `src/app/build-label.ts` from `M0-BASELINE-001` to `M0-ANDROID-001`, create a branch and commit using phone only, open/merge a pull request after green `validate` CI, and verify the Pages site shows `M0-ANDROID-001`. Record the real SHA, workflow URL, and device in `docs/M0_ACCEPTANCE_RECEIPT.json` and `docs/TEST_RESULTS.md` before marking M0 accepted.

The M0 application is only the infrastructure placeholder. Real 52-comuna geometry is deferred to M1; offline functionality is an M5 deliverable.
