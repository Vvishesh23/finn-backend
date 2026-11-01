## CP11 update — 1 November 2026

[Current checkpoint](checkpoints/CP11_RELEASE_CHECKPOINT.md): 161 backend and eight frontend tests pass; local browser workflow verified with explicit source-viewer gaps. [Deployment README](../DEPLOYMENT_README.md), [walkthrough](EVALUATOR_WALKTHROUGH_CP11.md), [submission status](SUBMISSION_STATUS_CP11.md). Public deployment and live Gemini remain incomplete. Earlier records below are historical.

## CP10 update — 31 October 2026

[Current checkpoint](checkpoints/CP10_SECURE_GEMINI.md): 157 backend + four frontend tests passed, preserving 11 issuers/71 facts. [Private owner-only setup guide](SECURE_GEMINI_SETUP.md) contains the real trust boundary, privacy terms, configuration, quotas, rollback and live-test checklist. Use `python3 scripts/run_isolated_tests.py -q`; direct pytest is intentionally disabled. Actual tests use a literal clean environment, temporary SQLite and no network. Live Gemini remains NOT TESTED; public deployment remains incomplete. Do not read or configure real secrets in Codex. Historical entries below may describe the superseded direct-HTTP adapter, unscoped cache or process-local concurrency.

## CP09 update — 28 October 2026

[Current checkpoint](checkpoints/CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md): 11 financial research issuers, 16 evidence records, 71 facts; eight new reviewed PDFs, 44 reproducible facts. 128 backend tests and four frontend race tests pass. [Robustness matrix](ROBUSTNESS_MATRIX.md) distinguishes implemented controls from remaining gaps. Coverage remains historical/partial; deployment and live Gemini evaluation are pending deferred configuration. Earlier entries below are historical.

## Update — 28 October 2026

Current report: [CP08](checkpoints/CP08_PORTFOLIO_PUSH_AND_HANDOFF.md). 106 tests passed with one existing warning; real mobile research verified. Public deployment and live Gemini evaluation remain pending deferred configuration. See CP08 for actual source coverage and exact evidence. Earlier entries below are historical.

# Actual verification — 27 October 2026 IST

Backend command from project root: `python -m pytest backend/tests -q` after installing `backend/requirements.txt`.

Latest result: **29 passed, 0 failed**, one upstream Starlette TestClient/httpx deprecation warning. Raw output: `docs/test-output.txt`.

Additional executed checks: `node --check frontend/app.js` passed; `python scripts/verify_replay.py` validated 18 companies, 189 bars, 4 documents and 20 filings, with EOD range 2026-07-27 through 2026-10-26. No paid inference tests or real model calls.

Earlier failures are not concealed: the first test invocation used the wrong project import root and failed collection. After correction, 27 tests passed and one failed due to overly broad record-date assignment. The imported data was corrected; annual-vs-quarter coverage was added; final 29-test run passes.

## Interactive browser verification

Real local app at http://127.0.0.1:8000. Observed mobile CSS viewport: 375 × 812. Due to application zoom, browser override dimensions differed from CSS dimensions; measurements used actual innerWidth and document scrollWidth. No page horizontal overflow observed (document scrollWidth 365, viewport width 375); financial tables scroll inside their own container.

- Brief -> FY25 replay: changed from 1 recent snapshot disclosure to 6 historical disclosures.
- Results -> details: source timestamp, consolidated revenue/PBT/PAT table, missing EBITDA and original exchange link visible.
- Investigate guidance: original 1–3% CC growth guidance vs 4.2% outcome, 1.2 percentage-point gap; 20–22% margin vs 21.1%, both transcript links visible.
- Settings: volume 2× -> 0.1× produced 3 observed alerts; restoring 2× produced 0. Saved browser-specific settings confirmed by status text.
- Actual screenshots saved in `docs/evidence/`. These are browser captures, not generated concepts.

Not tested/claimed: public deployment, Docker build, runtime model/key handling, real multiworker quotas, automatic PDF-table ingestion, full financial fixture coverage across issuers, physical phone lab. Unknown ticker and no-model fallback verified by backend tests. Broader browser results are in `docs/evidence/browser-checks.json` when present.

## Clean installation
A new project `.venv` was created and installed solely from shipped `backend/requirements.txt`. Its pytest run passed 29 tests; replay validation passed. Actual command from project root: `.venv/bin/python -m pytest backend/tests -q`. Secret-pattern scan found zero matching text files (not a proof of all possible secret absence). Desktop observed CSS viewport 1200×800, scrollWidth 1190; no page overflow. Browser captures reflect application screenshot scaling.


### 27 October continuation — query correctness
Local uncommitted fixes normalize supported fiscal-year forms, reject unsupported/ambiguous periods and quarterly guidance, preserve multiple requested metrics, label unavailable metrics honestly, and block other-issuer documents from unlocking Infosys fixed answers. Financial citations now use source ID; answer cache version bumped without deleting prior rows.
Executed: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider` -> **55 passed, 0 failed, 1 existing dependency warning**, 0.50 seconds. `node --check frontend/app.js` passed. Earlier 29-test results and browser captures above are historical. No new browser/provider/deployment checks. Details and remaining priorities: project-root CODEX_HANDOFF.md continuation section. All checkpoint gates remain PARTIAL. No commit/push.
