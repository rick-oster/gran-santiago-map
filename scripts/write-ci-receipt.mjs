import { mkdirSync, writeFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'

const checks = {
  install: process.env.M0_INSTALL || 'not-run',
  static: process.env.M0_STATIC || 'not-run',
  typecheck: process.env.M0_TYPECHECK || 'not-run',
  unit: process.env.M0_UNIT || 'not-run',
  build: process.env.M0_BUILD || 'not-run',
  playwrightSetup: process.env.M0_BROWSER_SETUP || 'not-run',
  e2e: process.env.M0_E2E || 'not-run',
}
const allPassed = Object.values(checks).every((x) => x === 'success')
const receipt = {
  schema: 1,
  milestone: 'M0',
  scope: 'GitHub Actions automated checks only (not Android physical acceptance)',
  timestampUtc: new Date().toISOString(),
  sourceCommit: process.env.GITHUB_SHA || null,
  githubRun: process.env.GITHUB_RUN_ID ? `https://github.com/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}` : null,
  nodeVersion: process.version,
  lockfilePresent: existsSync('package-lock.json'),
  checks,
  automatedChecksPassed: allPassed,
  androidCommitObserved: false,
  publishedUpdateObserved: false,
  m0GatePassed: false,
}
mkdirSync('evidence', { recursive: true })
writeFileSync(join('evidence', 'm0-ci-receipt.json'), JSON.stringify(receipt, null, 2) + '\n')
console.log('M0_CI_RECEIPT=' + (allPassed ? 'AUTOMATED_CHECKS_PASS' : 'AUTOMATED_CHECKS_NOT_PASS'))
console.log(JSON.stringify(receipt, null, 2))
