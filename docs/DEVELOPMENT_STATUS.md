# Development status — Gran Santiago Map V1

Updated: 2026-10-19. Spec version: 1.0 (frozen).

## Completed in delivered starter (source only)

- Initial React + TypeScript + Vite project files and responsive honest M0 placeholder.
- Leaflet included as locked **direct dependency version**; map rendering deliberately not implemented before M1 validation.
- Vitest unit contract; Playwright Chromium desktop and mobile-emulation tests.
- GitHub Actions automatic CI, Pages deployment using a reusable workflow, downloadable JSON evidence receipt.
- Android-only bootstrap documentation, Node 22 Codespaces devcontainer, exact commands, build-marker acceptance mechanism.
- Frozen specification copied without changing design decisions, source and acceptance docs.
- Structural static check executable directly with Node.js; local syntax/structure checks PASSED, receipt in docs/LOCAL_PRECHECK_RECEIPT.json.

## Not verified/accepted

- Package install, actual TypeScript build, unit/e2e execution (artifact runtime cannot access npm registry).
- GitHub repository creation, branch checks, Pages settings, online HTTPS deployment.
- Android-only edit/commit/push, observation of CI run/deployed updated marker on phone.

## Pending in order

1. **M0:** User creates public GitHub repository (if public hosting acceptable), uploads ZIP in Android Codespaces, runs bootstrap, commits/pushes, enables Pages/branch checks.
2. **M0:** CI and Pages receipts must be inspected; Android edits BUILD_MARKER, pushes, confirms deployed new marker.
3. **M1:** Acquire/validate official 52-comuna source, licensing, official 34 preset identities, topology, versioned static geometry and adjacency. Do not start until M0 accepted.
4. M2–M6: implement sequentially against the frozen spec; mark each PASS only with evidence.

## Engineering decisions

- No placeholder comuna IDs, approximated polygon outlines, tiles, or network map providers.
- Pages deploy happens only on `main` after the entire CI `validate` job succeeds.
- PR CI runs but cannot publish/overwrite the production Pages site.
- On free accounts, GitHub Pages requires public source; do not publish privately owned code without a conscious user choice.
- Dependency versions are exact direct versions and a transitive lockfile must be generated/committed during first Codespaces bootstrap.
- Android phone physical smoke check is independent of Playwright mobile emulation.
- PWA offline/manifest/service-worker work is M5, not misrepresented as implemented at M0.
