# Development on Windows 11 and Android — M0

**Frozen product specification:** [V1_SPEC.md](V1_SPEC.md). This page changes only development workflow, not the V1 design. GitHub's `main` is the shared source of truth. Device-local map settings remain independent. Workstations, Codespaces, and phones are not runtime servers for the deployed application.

## Windows 11

The established checkout is `F:\Projects\GranSantiago`. PowerShell 7 is recommended; the development script is compatible with Windows PowerShell 5.1.

```powershell
Set-Location 'F:\Projects\GranSantiago'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\scripts\Windows-Dev.ps1' -Action Setup
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\scripts\Windows-Dev.ps1' -Action NewBranch -BranchName 'feature/my-change'
```

`Setup` runs `npm ci` and the M0 static, TypeScript, Vitest and production-build checks. `NewBranch` requires a clean `main`, fetches `origin/main`, and fast-forwards (never resets or force-pushes), then creates a feature branch. Edit in VS Code or another editor. Verify and publish:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\scripts\Windows-Dev.ps1' -Action Check
git add -A
git commit -m 'Describe the change'
git push -u origin feature/my-change
gh pr create --base main --head feature/my-change --fill
```

Review `validate` and `windows-smoke` in the pull request. Merge only after checks pass. To resume work after a change made on Android, switch to clean `main` then run `-Action Sync`; this uses a fast-forward only. Use `-Action Serve` for `http://127.0.0.1:5173/` during local development. **A localhost dev server is not the production PWA.**

## Android — no local Windows PC required

The least fragile path is GitHub's own **Edit this file** interface. It avoids the separate Visual-Studio-Code OAuth screen, which the browser previously displayed with a disabled authorization button:

1. Open [the repository](https://github.com/rick-oster/gran-santiago-map) in Android Chrome or Brave while signed in. Enable **Desktop site** if controls are absent.
2. Open a file; choose **Edit this file** (pencil); edit and commit **to a new branch**, not protected `main`.
3. Open the pull request in the GitHub browser UI. Watch `windows-smoke` then `validate`. Merge only after green checks.
4. Confirm the `main` push runs `deploy`, then refresh the [Pages site](https://rick-oster.github.io/gran-santiago-map/). A fresh edit is not published until merged.

For multiple-file edits, `https://github.dev/rick-oster/gran-santiago-map` is optional, not mandatory. GitHub Codespaces (within free usage quotas) provides a browser terminal; `github.dev` does not. On Codespaces, use `npm ci && npm run verify:quick`. No Windows services are needed.

## Switching devices safely

- **Windows → Android:** commit/push to feature branch; review it on phone; merge only after CI.
- **Android → Windows:** merge the PR, then from clean `main` run `Windows-Dev.ps1 -Action Sync`. Never `git reset --hard` to resolve divergence.
- **Uncommitted edits:** not synchronized. Do not expect a change typed on one device to appear on the other without a Git commit/push.
- **Conflict:** stop, inspect differences and merge deliberately. Do not overwrite local work or force-push.
- **Production:** only reviewed `main` changes deploy. Preview/PR tests do not replace an Android physical on-device check.

## M0 acceptance evidence

The original Android test change `M0-ANDROID-001` was merged in [PR #1](https://github.com/rick-oster/gran-santiago-map/pull/1) at SHA `c659eb00c4042590d9a9708b4655203c016417ec`; [CI run 39350409721](https://github.com/rick-oster/gran-santiago-map/actions/runs/39350409721) passed both validate and deploy. GitHub's evidence does not identify the physical device used and does not prove that a human observed the live Pages marker; these require an actual on-device confirmation before the M0 gate can be marked PASSED.

## Acceptance checklist

- [x] GitHub repo and Pages source configured, protected `main`, Windows initial bootstrap.
- [x] Android-named marker committed via PR and successful CI/deploy evidence obtained.
- [ ] Confirm that PR #1 was actually authored from Android without using Windows for that edit.
- [ ] Confirm `M0-ANDROID-001` appeared on Pages when viewed from Android.
- [ ] The new `windows-smoke` and `validate` checks pass on the dual-device workflow PR.
- [ ] From Windows, run `-Action Setup` and `-Action Status` using the newly merged workflow; optionally confirm a Windows-only PR round-trip.

Only then update `docs/M0_ACCEPTANCE_RECEIPT.json`, `docs/TEST_RESULTS.md`, and `docs/DEVELOPMENT_STATUS.md` with factual evidence. M1 is gated on M0 acceptance.
