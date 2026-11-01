# FINN — Desktop copy, GitHub and frontend hosting

1 November 2026. **Frontend first**, as requested. Gemini integration remains in the full backend. No real key, hosting credential, commit, push or public deployment was performed. Public deployment and live Gemini are still unverified. The existing CP11 release gate remains incomplete.

## What is in the Desktop folder

`~/Desktop/FINN` is a fresh source copy of the existing project, including backend, frontend, public derived financial fixtures, tests, setup tools, architecture, provenance, handoff and checkpoints. The original working repository is unchanged by the copy. It is not a Git clone/history export. Historical test outputs are retained; documentation home-directory prefixes are made portable. `RELEASE_FILE_MANIFEST.json` lists source hashes. `PUBLISH_SAFETY_REPORT.json` records the limited-pattern check.

`frontend-publish/` contains only the public HTML, CSS and JavaScript, `.nojekyll` and a protective `.gitignore`. **This is the folder to upload first.** It displays the existing FINN design and working navigation, clearly labelled “Frontend preview”. It makes no API calls, shows no invented financial records and disables research and observation inputs until the backend is connected. This is not the complete ENAM evaluator workflow yet.

Actual environment files, keys, databases, query caches, virtual environments, Git metadata/history and original assessment/issuer PDFs are not copied. Full source PDFs are not required to run the application. The old HDD project is neither accessed nor included. `.env.example` in the full project contains placeholders only; do not replace them with real secrets in any repository.

## 1. Put ONLY the frontend on GitHub first

Create a new empty GitHub repository named `finn-frontend`. A private repository can be connected to Render while its static website is public. Do not initialize the repository with a README, licence or gitignore if using the commands below. Sign in/authorize GitHub yourself. Use GitHub's normal browser authentication or your Git client; never place a token in the remote URL or source files.

Open Terminal and run:

```sh
cd "$HOME/Desktop/FINN/frontend-publish"
git init -b main
git add .gitignore .nojekyll index.html assets/app.js assets/style.css assets/preview.js
git diff --cached --stat
```

The staged list should contain **six files** and nothing from the backend, docs, private files or databases. Then run these yourself, replacing `YOUR_USERNAME`:

```sh
git commit -m "Publish FINN frontend preview"
git remote add origin https://github.com/YOUR_USERNAME/finn-frontend.git
git push -u origin main
```

If Git asks for your identity, configure your own preferred GitHub identity locally. No identity is configured for you. Do not upload the parent Assessment/workspace folder or an old archive. These are instructions for your actions, not actions performed by Codex. Official reference: [GitHub: add local code](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).

## 2. Host that frontend on Render Free

1. Sign in to Render yourself. Choose **New → Static Site** (not Web Service).
2. Connect GitHub and grant access only to the intended `finn-frontend` repository.
3. Select `main`. Leave Root Directory blank.
4. Set **Build Command** to `echo "Static frontend; no build required"`.
5. Set **Publish Directory** to `.`. This is safe only because this separate repository contains the public frontend files alone.
6. Add no API keys or other secrets. No package installation is needed. You may set the nonsecret `SKIP_INSTALL_DEPS=true` to avoid automatic dependency detection.
7. Create the Static Site. Copy the real HTTPS `onrender.com` URL from Render after deployment succeeds.
8. Open it in a private browser window and on a phone. All four tabs should load and show “Frontend preview”. Research must clearly require the backend. There should be no `/api` requests, provider requests or credential prompts.

Render documents Static Sites as free hosting, subject to workspace bandwidth/build limits; this does not require a paid backend plan or a trial credit. [Official Static Sites guide](https://render.com/docs/static-sites), checked 1 November 2026. Review the account's displayed terms; no credit/trial eligibility or billing action is assumed.

Optional Render response headers: `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'`. A restrictive meta policy is already in the static HTML; `frame-ancestors` requires a response header. No SPA rewrite is necessary because tabs are handled within the same page.

## Alternative: deploy the frontend from the full source repository

After publishing the full clean source (below), use a Render Static Site with Root Directory blank, Build Command `python3 scripts/build_frontend.py --output dist`, Publish Directory `dist` and nonsecret `SKIP_INSTALL_DEPS=true`. Or use Blueprint path `deploy/render-static.yaml`. Only generated `dist` assets become public files. **Never set Publish Directory to `.` for the full project repository**: that would expose backend source, documentation and fixtures as downloadable files. The backend is not run by a Static Site.

## 3. Publish the full project later, when ready

The original repository and its uncommitted work are preserved. The Desktop copy deliberately contains no old `.git` history; it starts a new source repository if you choose this route. Do not represent it as the original complete development history. Preserve the original repo/checkpoints and genuine AI build logs for submission.

```sh
cd "$HOME/Desktop/FINN"
python3 scripts/check_publish_safety.py
git init -b main
git add .
python3 scripts/check_publish_safety.py --staged
git diff --cached --stat
```

Stop if the checker fails or any unexpected file appears. The generated `frontend-publish/`, local virtual environment, `dist`, databases, actual `.env`, PDFs and credentials must not be staged. Known-pattern checks are not a universal guarantee; review the staged filenames and intended public material. Create a separate empty repository such as `finn-assessment`, then commit and push yourself:

```sh
git commit -m "Import reviewed FINN source and checkpoints"
git remote add origin https://github.com/YOUR_USERNAME/finn-assessment.git
git push -u origin main
```

No licence for third-party content is invented. Included facts/snippets are derived research fixtures with provenance/rights limitations; original full PDFs are excluded. See `docs/ARCHITECTURE_CP11.md` and `docs/LIMITATIONS.md`. Review these selected fixtures before making the repository public.

## 4. Keep Gemini for the backend phase

Gemini must **never** be called directly from a publicly hosted frontend with your key. Existing provider abstraction, SDK adapter, source-grounding, deterministic calculations, budget/security protections and tests are preserved. The frontend preview does not remove or replace them. We will connect the deployed backend in the next phase; do not disable its existing safeguards.

The easiest complete application deployment is the same-origin FastAPI service, which already serves the existing frontend. It avoids introducing cross-origin cookies/CORS changes. Keep the standalone frontend URL as a preview, or later explicitly configure/test a separated frontend/backend integration. Merely changing a hostname will not complete that integration.

Render Free Web Services lose local SQLite on sleep/restart/redeploy and cannot attach persistent disks. Therefore `deploy/render-free.yaml` is only a no-model preview profile. For the existing Gemini implementation use `deploy/render-persistent.yaml` on a paid single instance with a durable disk, or an existing persistent host. If Render grants trial credits to your account, confirm that they actually cover your chosen compute/disk and their expiry; credits do not make a free instance persistent. No external Postgres adapter is implemented. [Free limits](https://render.com/docs/free), [Persistent disks](https://render.com/docs/disks).

For the persistent deployment: `FINN_DB=/var/data/finn.sqlite3`, `AI_BUDGET_STORAGE_PERSISTENT=true`; initially `AI_ENABLED=false`, `REASONING_PROVIDER=disabled`. Prove disk persistence, then configure the real Gemini key privately in hosting environment secrets outside Codex and follow `docs/LIVE_VERIFICATION_CP11.md`. Do not put it in files, GitHub, browser code, chat, build arguments or logs. Do not send Codex secret values or production log dumps. Read `DEPLOYMENT_README.md` for startup, health, verification and rollback.

## Local setup of the complete Desktop copy

Create a new environment; the old one was intentionally not copied. Requires Python 3.12 and Node for frontend tests:

```sh
cd "$HOME/Desktop/FINN"
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.lock
python3 scripts/run_isolated_tests.py -q
node --test frontend/tests/navigation.test.cjs
python3 scripts/run_mock_preview.py --mode disabled --port 8011
```

The last command starts a no-key local preview; open `http://127.0.0.1:8011/`. Tests use an isolated literal environment and temporary database, never your real credential. To rebuild a static-only preview, choose a new output folder: `python3 scripts/build_frontend.py --output another-frontend-preview`. Existing output folders are not overwritten.

## Still not complete

GitHub publication, real Render URL, public browser verification, backend hosting and independent real Gemini validation require your actions. The frontend-only URL is a first deployment milestone, not a claim that CP11 or the ENAM submission is complete. No submission email is sent by these instructions.
