# Desktop source copy and frontend-first handoff

1 November 2026. User requested a complete Desktop folder, safe publication steps and then frontend-first hosting. Gemini remains in the full application. No real key/account was accessed; no commit, push, purchase, public deployment or email was performed.

## Delivered scope

`~/Desktop/FINN`: portable source snapshot, with tests, derived public fixtures, architecture/provenance, historical work logs/checkpoints and deployment documentation. Original working repo/dirty branch is preserved; no Git history, virtual environment, live DB, secret files or original PDFs are exported. Local home-prefix references in text docs are made portable, with that change recorded in the manifest. New complete source copy requires a fresh environment; this is intentional, not missing implementation.

`frontend-publish/`: six explicitly public files for a separate `finn-frontend` repository and Render **Static Site**. The design/navigation is available; data/research/rules are visibly unavailable pending backend connection. Static meta CSP blocks network connections. This preview is not a fake working financial application. The main FastAPI index does not load `preview.js`; its existing behavior, 11 issuers/71 facts and server-side Gemini integration remain intact.

New tools: `scripts/build_frontend.py`, `check_publish_safety.py`, `prepare_desktop.py`. New guide: `GITHUB_RENDER_STEPS.md`. New deployment profiles: `deploy/render-static.yaml` and `deploy/render-free.yaml` (latter optional no-model ephemeral backend preview; not the requested first deployment). Updated `.gitignore`, `.dockerignore` and `scripts/package_review.py`; four synthetic packaging tests in `backend/tests/test_publication.py`, frontend preview regression in `frontend/tests/navigation.test.cjs`; two guarded branches in `frontend/app.js`, new `frontend/preview.js`. Docker's build context uses an allowlist for runtime application/assets/required public JSON only, excluding docs/tests/tools/actual env/DB material.

## Real verification

- `python3 scripts/run_isolated_tests.py -q`: **165 passed**, no failures, one existing Starlette/httpx deprecation warning. Includes all prior 161 tests and four publication safety tests.
- `/opt/homebrew/bin/node --test frontend/tests/navigation.test.cjs`: **9 passed**, no failures. New test proves boot and all four preview tabs make zero backend fetches and research inputs are disabled. Normal-app regression tests remain included.
- JavaScript syntax checks and `git diff --check`: pass.
- `python3 scripts/check_publish_safety.py`: pass, zero findings among explicitly selected source files. This checks known credential patterns/prohibited paths; it does not prove absence of every possible secret, inspect excluded secret files, OCR images or audit Git history/licensing.
- Static build executed successfully into a fresh temporary directory, with only `.nojekyll`, `index.html` and three JavaScript/CSS assets. Existing-output refusal, secret-path rejection, synthetic credential detection and symlink refusal are tested.
- Actual local browser navigation across Brief/Companies/Research/Settings succeeds. Default desktop screenshot: `evidence/desktop-release/frontend-desktop.jpg`. Responsive mobile screenshot: `evidence/desktop-release/frontend-mobile.jpg`; measured document width/scrollWidth both **360 CSS px**, no horizontal page overflow. The requested viewport override and actual DOM measurement differed; actual measurement is reported. Disabled research/backend-pending labels verified. Physical-device/public deployment checks are still not run.
- Test and publication-check outputs are stored under `evidence/desktop-release/`. Source-copy manifest hashes permit checking portable contents without including old Git metadata.

Native/Render Linux builds, live Gemini, actual GitHub publication and public frontend URL remain **NOT TESTED / NOT DEPLOYED**. Local static-server startup initially hit sandbox port restrictions; it succeeded after a local-only permission grant. No production system was contacted for these checks.

## Owner's next actions

Follow `../GITHUB_RENDER_STEPS.md`: upload only `frontend-publish/` into a new empty `finn-frontend` repository, then Render New → Static Site, branch main, no root subdirectory, build `echo "Static frontend; no build required"`, publish `.`. No key or secret is needed. Do not publish `.` from the full project as a static site. Send only the resulting public URL for verification.

Later deploy the intact backend with durable quota storage and private runtime secrets, or serve the existing complete same-origin app directly. The full-source static Blueprint builds `dist`, never publishes the repository root. Gemini has not been removed and protections have not been weakened. Independent real Gemini validation still follows `LIVE_VERIFICATION_CP11.md`; CP11 remains incomplete until the main public Push/Pull flow works. Existing CP11 checkpoint remains the historical release report, supplemented by this document.
