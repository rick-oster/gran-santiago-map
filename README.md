# Gran Santiago Map V1

**Implementation phase: M0 infrastructure active; final dual-device acceptance pending.** The complete [frozen V1 specification](docs/V1_SPEC.md) is unchanged. This is a genuine M0 placeholder, not fabricated comuna geometry. Geographic data acquisition begins only after M0 acceptance.

- Repository: https://github.com/rick-oster/gran-santiago-map
- Deployed M0 site: https://rick-oster.github.io/gran-santiago-map/
- Development on **Windows 11 and Android**: [Dual-device workflow](docs/DUAL_DEVICE_WORKFLOW.md)
- Development and acceptance status: [Development status](docs/DEVELOPMENT_STATUS.md), [Test results](docs/TEST_RESULTS.md), [M0 receipt](docs/M0_ACCEPTANCE_RECEIPT.json)

## Windows quick start

The established checkout is `F:\Projects\GranSantiago`. From PowerShell:

```powershell
Set-Location 'F:\Projects\GranSantiago'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\scripts\Windows-Dev.ps1' -Action Setup
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\scripts\Windows-Dev.ps1' -Action Serve
```

Run `-Action Status`, `-Action Check`, `-Action Sync`, or `-Action NewBranch -BranchName 'feature/example'` as needed. The script never deletes changes, force-pushes or silently modifies protected `main`. Use pull requests.

## Android quick start

Use [the GitHub repository](https://github.com/rick-oster/gran-santiago-map) directly in your phone browser. Open a file, use the pencil icon to edit, commit to a new branch, open a PR and merge after the required `validate` check succeeds. CI now also checks PowerShell and the Windows build before `validate` is marked green. The Pages site updates on a successful push to `main`. This does **not** require Windows to be on. `github.dev` and Codespaces are optional for advanced changes; they are not required for small file edits.

## Automated checks and release gates

- **`windows-smoke`:** Windows-hosted runner parses and smoke-tests the PowerShell entrypoint, verifies the frozen specification, and runs local static/type/unit/build checks.
- **`validate`:** waits for `windows-smoke`, then runs Linux checks, desktop/mobile-emulated Playwright and machine-readable evidence generation.
- **`deploy`:** only for successful `main` CI pushes; publishes HTTPS GitHub Pages.

`validate` remains the branch-protection required check. Actual touch behavior, physical Android editing and installed-PWA offline behavior cannot be proven by Playwright emulation alone. The offline PWA/service worker is scheduled for M5; the M0 placeholder is not represented as offline-ready.

## Common local commands

```bash
npm ci
npm run verify:quick
npx playwright install chromium
npm run test:e2e
npm run dev
```

Direct dependencies are version-locked in `package.json` and transitive dependencies in `package-lock.json`. New dependencies and remote APIs require a scoped engineering decision. No API credentials, hosted backend or computer-resident server are needed for production.

## Preserved design decisions

The app will use React, TypeScript, Vite, Leaflet and bundled verified complete administrative polygons for 52 comunas; the default preset contains exactly 34 official comunas. Map preferences are device/browser-local, not synced by Git. No tile provider, cloud account, paid API, placeholder polygons or silent changes to the frozen UX are permitted.
