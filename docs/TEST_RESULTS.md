# Test results — Gran Santiago Map V1

## M0 final acceptance — PASS

- Windows R4 bootstrap source, TypeScript and build PASS; Vitest 2/2 PASS.
- [CI run 39346060295](https://github.com/rick-oster/gran-santiago-map/actions/runs/39346060295): Linux validate + Pages deployment PASS.
- [Android marker PR #1](https://github.com/rick-oster/gran-santiago-map/pull/1): merge `c659eb00c4042590d9a9708b4655203c016417ec`; [CI run 39350409721](https://github.com/rick-oster/gran-santiago-map/actions/runs/39350409721): Linux validate + deploy PASS.
- [Dual-device PR #2](https://github.com/rick-oster/gran-santiago-map/pull/2): merge `7e6bdfe7d2ca4b9a6d7c329428cd934d2862af70`; [CI run 39356252271](https://github.com/rick-oster/gran-santiago-map/actions/runs/39356252271): Windows smoke, Linux validate/Playwright and Pages deployment all PASS.
- Windows 11 after merge: `npm ci`, source checks, TypeScript, 2/2 Vitest, Vite build and `WINDOWS_LOCAL_VERIFY=PASS` (user-provided console output).
- Android device authoring and seeing deployment: explicit user attestation; no independent physical-device recording. Device test accepted on this declared basis.

## M1 first-stage pipeline — local synthetic tests

- Six offline contract tests: **6/6 PASS** in the preparation environment, including geographic name normalizing, 52-name/34-preset shape, rejecting duplicate/invented IDs, rejecting incomplete regional datasets, shared-boundary adjacency, and geometry count fingerprints.
- Actual DPA 2023 integration: **NOT RUN**; authoritative polygon archive/schema/license still pending.
- Production GeoJSON and adjacency graph: **NOT RELEASED**; any generated candidate remains staged and excluded from Git.
- M1 milestone gate: **NOT PASSED**.
