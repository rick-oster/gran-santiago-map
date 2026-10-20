#!/usr/bin/env bash
# Run inside the new GitHub Codespace repository AFTER uploading/extracting the starter ZIP.
set -Eeuo pipefail
if [[ ! -d .git || ! -f package.json || ! -f docs/V1_SPEC.md ]]; then
  echo 'ERROR: run from the initialized repository root after extraction.' >&2
  exit 2
fi
if ! command -v node >/dev/null || ! command -v npm >/dev/null; then
  echo 'ERROR: Codespace must have Node 22+ and npm.' >&2
  exit 2
fi
node -e 'if (+process.versions.node.split(".")[0] < 22) process.exit(2)'
echo 'M0_BOOTSTRAP_INSTALL=BEGIN'
npm install --no-audit --no-fund
npm run check:static
npm run typecheck
npm run test:unit
npm run build
if [[ ! -f package-lock.json ]]; then echo 'ERROR: npm did not generate package-lock.json' >&2; exit 2; fi
echo 'M0_BOOTSTRAP_STATIC_UNIT_BUILD=PASS'
echo 'NEXT: git add -A && git commit -m "Bootstrap M0 infrastructure" && git push origin main'
echo 'NEXT: after Pages and CI activate, make a separate marker edit from Android github.dev.'
