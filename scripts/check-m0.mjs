import { existsSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const mustExist = [
  'docs/V1_SPEC.md', 'docs/DATA_PROVENANCE.md', 'docs/ACCEPTANCE_MATRIX.md',
  'docs/DEVELOPMENT_STATUS.md', 'docs/TEST_RESULTS.md',
  'src/app/App.tsx', 'src/app/build-label.ts', 'src/main.tsx',
  'tests/unit/build-label.test.ts', 'tests/e2e/m0.spec.ts',
  '.github/workflows/ci.yml', '.github/workflows/deploy.yml',
]
const missing = mustExist.filter((f) => !existsSync(resolve(f)))
const spec = readFileSync('docs/V1_SPEC.md', 'utf8')
const source = readFileSync('src/app/App.tsx', 'utf8')
const packageData = JSON.parse(readFileSync('package.json', 'utf8'))
const failures = [
  ...missing.map((f) => `Missing required file: ${f}`),
  ...(['M0 — Repository & phone-only workflow', 'M6 — Release acceptance'].filter((s) => !spec.includes(s)).map((s) => `Frozen spec missing: ${s}`)),
  ...(!source.includes('Sin geometría ficticia') ? ['Placeholder must say no invented geographic geometry'] : []),
  ...(!['react', 'react-dom', 'leaflet'].every((p) => p in packageData.dependencies) ? ['Required stack packages missing'] : []),
]
const result = { milestone: 'M0', check: 'static-source-contract', passed: failures.length === 0, requiredFileCount: mustExist.length, failures }
console.log(JSON.stringify(result, null, 2))
if (failures.length) process.exitCode = 1
