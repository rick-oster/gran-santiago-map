# Test results and evidence ledger

Updated 2026-10-20. The engineering specification is unchanged.

## Previously observed tests

- Windows R4 bootstrap reused pushed commit `5c9fc9831580f48ced91cc0b9af861c0f93b335f` without new push; Node/npm install, `check:static`, TypeScript, Vitest 2/2 and Vite production build passed.
- GitHub Actions run [39346060295](https://github.com/rick-oster/gran-santiago-map/actions/runs/39346060295): `validate` and `deploy` passed; CI artifacts downloaded on Windows and deployed Pages HTTP/JS marker check passed.
- [PR #1](https://github.com/rick-oster/gran-santiago-map/pull/1) merged marker change; new `main` commit `c659eb00c4042590d9a9708b4655203c016417ec`.
- GitHub Actions [run 39350409721](https://github.com/rick-oster/gran-santiago-map/actions/runs/39350409721): `validate` and `deploy / publish` passed; all reported CI steps (including desktop/mobile-emulated Playwright) succeeded and CI evidence artifact exists.
- `M0-ANDROID-001` appears in committed source. Actual Android device of PR authoring and visual observation of Pages remain **unconfirmed by an independent physical-device receipt**.

## New proposed dual-device workflow checks

- Local source static checks (YAML structure/links and package integration): **to be executed by installer preflight**.
- Windows runner PowerShell AST, frozen-spec fingerprint, `Windows-Dev.ps1 -Action Status` and `-Action Check`: **PENDING remote CI**.
- Existing Linux `validate` after Windows dependency: **PENDING remote CI**.
- Windows physical script use and Android-only edit flow: **PENDING actual-device evidence**.

## Acceptance and evidence

The hosted CI attaches `m0-ci-evidence-<run_id>` JSON/test diagnostics. CI jobs cannot prove physical-phone interaction, source of input device, or whether the user saw a fresh deployed marker. The M0 receipt retains `m0GatePassed=false` until all required evidence is available. Do not advance to M1 until M0 is accepted.
