# Development status — Gran Santiago Map V1

Frozen [V1 specification](V1_SPEC.md) v1.0 remains unchanged, SHA-256 `eec81bb8e7ffa8af5522fd26b37b1cfd47b9cda0ec5095ebe4da8d55e93feddd`.

## M0 — ACCEPTED

- Public GitHub repo, GitHub Pages/Actions, protected `main`, Android and Windows editing documented and enabled.
- Android-authored change in [PR #1](https://github.com/rick-oster/gran-santiago-map/pull/1) built and deployed in [run 39350409721](https://github.com/rick-oster/gran-santiago-map/actions/runs/39350409721). User expressly confirms the edit was made on Android and its `M0-ANDROID-001` marker was seen on the deployed page from Android.
- Dual-device change [PR #2](https://github.com/rick-oster/gran-santiago-map/pull/2) merged at `7e6bdfe7d2ca4b9a6d7c329428cd934d2862af70`; [run 39356252271](https://github.com/rick-oster/gran-santiago-map/actions/runs/39356252271) completed with successful `windows-smoke`, `validate` and `deploy / publish`.
- Windows 11 checkout synchronized to the above commit; `Windows-Dev.ps1 -Action Setup` passed `npm ci`, static contract, TypeScript, two Vitest tests and Vite production build (`WINDOWS_LOCAL_VERIFY=PASS`).
- Independent device evidence: user attestation; GitHub cannot establish which physical device authored a change. See [machine-readable acceptance receipt](M0_ACCEPTANCE_RECEIPT.json).

## M1 — STARTED; NOT YET ACCEPTED

- Candidate source discovered: IDE SUBDERE DPA 2023, EPSG:5360, newer than the 2022 download shown in the specification. Direct official download cited in [data provenance](DATA_PROVENANCE.md).
- Offline Python inspector/staging converter and synthetic contract tests created in `data-source/scripts/m1_pipeline.py` / `data-source/tests/`.
- Source archive not yet downloaded or field-inspected in a successful integration run. Official CUT identifiers must be extracted from real data, never fabricated.
- Redistribution terms not yet independently verified: **NO** polygons committed to `public/` or a released build until cleared.
- M1 acceptance remains blocked on exactly 52 official ID-to-name records, exactly 34 unique default IDs, complete polygon/ring preservation, topological checks, source/CRS/checksums, adjacency review and explicit redistribution permission review.

## Remaining milestones

- **M2:** render real map and restore camera.
- **M3:** colors and persistent labels.
- **M4:** search, selection, presets, editable Custom, Undo.
- **M5:** installable fully offline PWA and real-device airplane-mode acceptance.
- **M6:** release acceptance, rollback tag and complete regression suite.

GitHub source changes require green pull-request CI. Never silently replace the frozen 34 default preset with a different legal/urban definition.
