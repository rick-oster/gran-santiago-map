# Test results and evidence ledger

Timestamp: 2026-10-19. Scope: generated M0 starter source.

## Test evidence so far

- `scripts/check-m0.mjs`: **PASS** in artifact runtime (see `LOCAL_PRECHECK_RECEIPT.json`).
- Frozen specification byte comparison, Node script syntax, TypeScript AST syntax, shell syntax, YAML/JSON source checks and CI structural checks: **PASS** (see `LOCAL_PRECHECK_RECEIPT.json`).
- `npm install`, `npm run typecheck`, `npm run test:unit`, `npm run build`, `npm run test:e2e`: **NOT RUN** — this artifact runtime cannot resolve `registry.npmjs.org`.
- GitHub Actions: **NOT RUN** — repository does not yet exist.
- Android-only edit, commit, CI, deployment: **NOT RUN** — requires actual Android user session.

## Future immutable evidence

Every GitHub Actions run uploads `m0-ci-evidence-<run_id>` (14 days) with `evidence/m0-ci-receipt.json`, `evidence/vitest.json`, `evidence/playwright.json` where generated. CI receipts measure automated checks only; do not interpret as Android or deployment success.

To close M0, update `docs/M0_ACCEPTANCE_RECEIPT.json` with exact GitHub repository URL, commit SHA from Android, CI run URL, deployed URL and observed updated marker. Keep `m0GatePassed=false` until actual checks.
