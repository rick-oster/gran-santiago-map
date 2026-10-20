# M0 Android acceptance checklist

This is a physical verification procedure. It cannot be replaced by desktop Playwright emulation.

### A. Bootstrap entirely from the phone

- [ ] Open GitHub on Android, create a **public** `gran-santiago-map` repo with README (only if publishing source publicly is acceptable).
- [ ] Start Codespaces from **Code > Codespaces** in the new repo (Chrome Desktop site + landscape if needed).
- [ ] Download the M0 ZIP to the phone, upload it using the Codespaces file explorer, extract in repo root.
- [ ] Run `bash scripts/phone-bootstrap.sh` and see `M0_BOOTSTRAP_STATIC_UNIT_BUILD=PASS`.
- [ ] Confirm `package-lock.json` was generated; `git add -A`, commit, push.

### B. GitHub Actions and Pages

- [ ] GitHub Settings > Pages > Build and deployment > GitHub Actions.
- [ ] Check Actions > CI > **validate** (green) and **deploy** (green).
- [ ] Download `m0-ci-evidence-<run_id>` and inspect `m0-ci-receipt.json` for `automatedChecksPassed: true` and `lockfilePresent: true`.
- [ ] Open the deployment URL reported by the `deploy` job in Android Chrome; check for M0 baseline screen and visible marker.
- [ ] Enable branch checks on `main` (if supported by account/visibility): require `validate`.

### C. Prove edit-to-publish from Android only

- [ ] On the phone, open `https://github.dev/<account>/gran-santiago-map`.
- [ ] Create a feature branch (if protection enabled). Edit **only** `src/app/build-label.ts`: `M0-BASELINE-001` -> `M0-ANDROID-001`.
- [ ] Commit and push via Source Control; make PR/merge after successful `validate` if branch protection is enabled.
- [ ] The new `main` CI run passes **validate** and **deploy**.
- [ ] Refresh the HTTPS Pages site, and verify **M0-ANDROID-001** is displayed, without starting any PC, local server or local build.
- [ ] Save exact repository URL, edited commit SHA, CI run URL, Pages URL and the observed marker in `docs/M0_ACCEPTANCE_RECEIPT.json`; record what browser/phone was used.

**Expected:** M0 can be accepted only if the actual Android-initiated edit reaches the deployed HTTPS site after automated tests pass. M1 remains blocked until this gate is satisfied.

If a step fails: inspect the first failing GitHub Actions step, use the uploaded `evidence` artifact and the job logs, change the source from Android, push a new commit, and rerun validation. Never turn a failing step green by disabling tests.
