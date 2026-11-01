## Desktop / frontend-first update — 1 November 2026

User requested a complete Desktop copy and then frontend-first hosting. Added explicit public-asset build, publication checks, safe portable copy, GitHub/Render guide, static preview guards and packaging tests. 165 backend/nine frontend tests pass. Actual local desktop/mobile navigation verified. Gemini remains in backend; no secret/account access, commit, push or deployment. See [handoff](DESKTOP_FRONTEND_HANDOFF.md). Earlier work records remain unchanged below.

## CP11 update — 1 November 2026

[Current checkpoint](checkpoints/CP11_RELEASE_CHECKPOINT.md): 161 backend and eight frontend tests pass; local browser workflow verified with explicit source-viewer gaps. [Deployment README](../DEPLOYMENT_README.md), [walkthrough](EVALUATOR_WALKTHROUGH_CP11.md), [submission status](SUBMISSION_STATUS_CP11.md). Public deployment and live Gemini remain incomplete. Earlier records below are historical.

## CP10 update — 31 October 2026

[Current checkpoint](checkpoints/CP10_SECURE_GEMINI.md): 157 backend + four frontend tests passed, preserving 11 issuers/71 facts. [Private owner-only setup guide](SECURE_GEMINI_SETUP.md) contains the real trust boundary, privacy terms, configuration, quotas, rollback and live-test checklist. Use `python3 scripts/run_isolated_tests.py -q`; direct pytest is intentionally disabled. Actual tests use a literal clean environment, temporary SQLite and no network. Live Gemini remains NOT TESTED; public deployment remains incomplete. Do not read or configure real secrets in Codex. Historical entries below may describe the superseded direct-HTTP adapter, unscoped cache or process-local concurrency.

## CP09 update — 28 October 2026

[Current checkpoint](checkpoints/CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md): 11 financial research issuers, 16 evidence records, 71 facts; eight new reviewed PDFs, 44 reproducible facts. 128 backend tests and four frontend race tests pass. [Robustness matrix](ROBUSTNESS_MATRIX.md) distinguishes implemented controls from remaining gaps. Coverage remains historical/partial; deployment and live Gemini evaluation are pending deferred configuration. Earlier entries below are historical.

## Update — 28 October 2026

Current report: [CP08](checkpoints/CP08_PORTFOLIO_PUSH_AND_HANDOFF.md). 106 tests passed with one existing warning; real mobile research verified. Public deployment and live Gemini evaluation remain pending deferred configuration. See CP08 for actual source coverage and exact evidence. Earlier entries below are historical.

# Worklog — 27 October 2026

CP00: public-source checks performed; Yahoo/NSE succeeded, issuer direct downloads blocked. CP01: local source-to-screen app running. CP02: snapshot filters and threshold controls verified. CP03: source-note research and conservative planner implemented. CP04: one authentic initial-guidance comparison and quarter figures. CP05: local handoff tested; public release remains PARTIAL.

29 backend tests pass. Actual responsive screenshots and raw test output saved. No original PDFs, HDD, old repository, secrets, accounts or paid inference used. No email sent. Next: rights review and authorized public hosting/GitHub setup; broaden verified primary-document ingestion.


### 27 October continuation — query correctness
Local uncommitted fixes normalize supported fiscal-year forms, reject unsupported/ambiguous periods and quarterly guidance, preserve multiple requested metrics, label unavailable metrics honestly, and block other-issuer documents from unlocking Infosys fixed answers. Financial citations now use source ID; answer cache version bumped without deleting prior rows.
Executed: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider` -> **55 passed, 0 failed, 1 existing dependency warning**, 0.50 seconds. `node --check frontend/app.js` passed. Earlier 29-test results and browser captures above are historical. No new browser/provider/deployment checks. Details and remaining priorities: project-root CODEX_HANDOFF.md continuation section. All checkpoint gates remain PARTIAL. No commit/push.
