# Gran Santiago Map V1

**State: M0 starter scaffold; M0 gate NOT YET PASSED.** The frozen specification is in [`docs/V1_SPEC.md`](docs/V1_SPEC.md). This is deliberately **not** a fake map; the 52 authoritative polygon features are to be acquired/validated in M1.

## Android-only path from a brand-new repo (no Windows PC)

1. On Android Chrome, log in to your GitHub account. Open **https://github.com/new**, create repository named **`gran-santiago-map`** with **Public** visibility *only if you accept making source public*. Initialize with a README (this is necessary to create the first branch for Codespaces). On a Free plan, GitHub Pages will not publish from a private repository. Keep the repo private instead if source publicity is not acceptable, but then Pages publishing under GitHub Free cannot pass M0. Do not add secrets or tokens to this project.
2. In the new GitHub repo, tap **Code → Codespaces → Create codespace on main** (Chrome desktop-site mode if menus are hidden). This cloud IDE is used **only to seed the repository and do optional terminal debugging**, within free quotas.
3. Download `Gran_Santiago_Map_M0_Source.zip` from ChatGPT to **Android Downloads**. In the Codespaces browser editor open the file explorer and use its **Upload** action to upload the ZIP to the repository root. On small screens, use Chrome's **Desktop site** option and landscape mode as needed. Then open **Terminal → New Terminal**. Do not upload a ZIP directly to a GitHub repository; GitHub won't unpack it into source files.
4. From the Codespaces terminal, paste the following commands (use the actual ZIP name if Android renamed it):

   ```bash
   cd /workspaces/gran-santiago-map
   unzip -oq Gran_Santiago_Map_M0_Source.zip -d .
   rm Gran_Santiago_Map_M0_Source.zip
   bash scripts/phone-bootstrap.sh
   git add -A
   git commit -m "Bootstrap M0 phone-only workflow"
   git push origin main
   ```

   The repository includes `.devcontainer/devcontainer.json` targeting Node 22 for new/rebuilt Codespaces. If the first Codespace (created before the file existed) is running an older Node, use `nvm install 22 && nvm use 22` or rebuild the Codespace before bootstrap. This installs exact direct dependencies, generates `package-lock.json`, checks the source contract, runs TypeScript/unit tests and compiles the site. **If any command fails, diagnose it; do not claim M0 passed.** The Codespace has a terminal; github.dev does not.
5. GitHub → **Settings → Pages → Build and deployment → Source: GitHub Actions**. Check **Settings → Actions → General** allows GitHub Actions workflows and that Pages deploy is permitted. The `CI` workflow builds/tests before deployment. Visit **Actions → CI** on the phone; make sure `validate` and `deploy` succeed. The site will normally be available at `https://<account>.github.io/gran-santiago-map/` (use the actual URL reported by `deploy`).
6. Optionally configure branch protection/ruleset **after** first green CI: GitHub repository **Settings → Branches (or Rules → Rulesets)**, target `main`, require pull requests and passing `validate`; confirm account/plan supports required enforcement. To modify the protected branch, create a feature branch in github.dev, commit, create PR, wait for CI, merge using GitHub mobile browser. This is more reproducible than direct changes to main. If ruleset cannot be enforced on the plan, document limitation; checks still run.
7. **Required Android-only gate:** In Android browser navigate to `https://github.dev/<account>/gran-santiago-map`, edit `src/app/build-label.ts`, changing `M0-BASELINE-001` to e.g. `M0-ANDROID-001`. Open Source Control, **commit** on a branch and **push**. From GitHub browser make PR, pass `validate` and merge (or push directly to main if branch protection hasn't been configured). Watch **Actions → CI** and the Pages deploy job. Reload the actual HTTPS URL on Android: the new marker must appear. This is an actual proof of edit/commit/test/deploy *without using a Windows machine*.
8. Record the exact SHA, CI URL, published URL, new marker, branch protection and verification in [`docs/M0_ACCEPTANCE_RECEIPT.json`](docs/M0_ACCEPTANCE_RECEIPT.json) and `docs/TEST_RESULTS.md`. **Only then mark M0 PASS and proceed to M1**. Shut down/delete idle Codespace to conserve its free quota. Editing via github.dev and CI does not require keeping it running.

### Phone workflow after bootstrap

- **Ordinary edits/reviews:** `https://github.dev/<account>/gran-santiago-map` → edit file → Source Control → commit/push → PR → GitHub Actions results → merge → live Pages site.
- **Build/tests:** automatic GitHub Actions on pushes/PRs; inspect downloadable `m0-ci-evidence-*` receipt, test JSON and job logs on phone.
- **Debugging with a terminal only if needed:** Codespaces from GitHub Code menu. Use `npm ci && npm run verify:quick`, then `npx playwright install chromium && npm run test:e2e` for browser tests. Stop Codespaces when done.
- **Review/rollback:** GitHub PR Files Changed and commit history are available on the phone. Revert via GitHub web PR or make a new revert commit; do not force push.
- **Changes are not kept forever until committed:** github.dev temporarily saves uncommitted edits in local browser storage; commit regularly.
- **Limitations:** Android landscape/desktop-site mode or an external keyboard can improve github.dev usability. Android-specific gestures, physical installation and airplane mode still need actual Android smoke tests in M5.

## Other environments

In any Node 22+ environment with internet access:

```bash
npm install
npm run verify:quick
npx playwright install chromium
npm run test:e2e
npm run dev
```

The GitHub Pages workflow uses a repository path-aware Vite `base`. Production release only happens from a successful push to `main`, not from unreviewed PRs. GitHub Pages URLs are HTTPS, and GitHub Free requires a public repository.

## Cost and safety

The project requires no local PC server or paid API. github.dev is free. GitHub Pages on a public repo and standard Actions runners are free subject to service policies. Codespaces free personal-account allowances are finite; under common GitHub Free personal terms they include 120 core-hours and 15 GB-month storage, which are **not** the same as 120 hours on every VM size. Turn off spending overages and set usage budgets under GitHub billing. Do not publish keys, passwords, internal documents or private source accidentally.

## Milestone status

See [`docs/DEVELOPMENT_STATUS.md`](docs/DEVELOPMENT_STATUS.md), [`docs/TEST_RESULTS.md`](docs/TEST_RESULTS.md), [`docs/ACCEPTANCE_MATRIX.md`](docs/ACCEPTANCE_MATRIX.md), and M0's machine-readable acceptance receipt. M1–M6 are **NOT IMPLEMENTED**. In particular, offline service worker, geographic vectors, presets, and labels are future milestones per approved specification.
