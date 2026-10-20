# Development status — Gran Santiago Map V1

Updated 2026-10-20; frozen spec 1.0, SHA-256 `eec81bb8e7ffa8af5522fd26b37b1cfd47b9cda0ec5095ebe4da8d55e93feddd`.

## Confirmed completed M0 infrastructure

- Public repository `rick-oster/gran-santiago-map` created; protected `main` requires `validate`.
- GitHub Pages uses Actions; initial Windows bootstrap and frozen-spec check passed, with Node 24.12.0 on the user's Windows machine.
- Initial Windows static source check, TypeScript, 2 Vitest tests and production build all passed.
- First GitHub CI and Pages deployment confirmed passed on Windows bootstrap.
- A follow-up GitHub PR #1 changed the marker in `src/app/build-label.ts` to `M0-ANDROID-001`; merge commit `c659eb00c4042590d9a9708b4655203c016417ec`, CI run `39350409721`, `validate` and `deploy` successful.

## Dual-device workflow change in progress

- `scripts/Windows-Dev.ps1`: safe Windows setup, checks, local server, fast-forward sync, feature branch creation.
- `scripts/Test-WindowsDev.ps1`: PowerShell syntax, safe Git contract and frozen-spec fingerprint checks.
- `windows-smoke` CI job; Linux `validate` depends on its success; existing protected check name `validate` retained.
- Android normal GitHub web editor path documented, avoiding the previously blocked Visual-Studio-Code OAuth screen. Codespaces is optional.

**This package is a proposed PR change, not yet a successful remote CI result.** Do not mark its checks passed until the GitHub Actions job succeeds after publishing.

## Acceptance blockers

1. Verify Android PR #1 truly originated from the Android device, without Windows assistance, and the user observed `M0-ANDROID-001` on Pages from the phone.
2. Push/merge dual-device workflow change after `windows-smoke` and `validate` succeed.
3. Verify Windows script on the user's machine; record evidence in M0 receipt, test ledger and development status. M0 remains **NOT YET ACCEPTED** until all required evidence exists.

## Next milestones — still blocked

- **M1** authoritative official 52-comuna boundaries, provenance/permission, IDs, integrity, adjacency, 34 preset.
- **M2** real map and camera.
- **M3** vivid adjacency-aware colors and permanent labels.
- **M4** search, selection, custom visibility and color controls.
- **M5** offline PWA install/resilience.
- **M6** release acceptance.

No M1 geometry or later application functionality is claimed as implemented.
