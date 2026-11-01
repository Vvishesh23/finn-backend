# CP08 — portfolio Push and generic evidence checkpoint

Recorded 28 October 2026, before the next implementation phase. This is a tested prototype, not a submission-ready release. Read alongside CP06_GENERIC_EVIDENCE.md, CP07_BOUNDED_REASONING.md, ../../CODEX_HANDOFF.md and ../AUTHORITATIVE_ASSESSMENT.md. Earlier plans and checkpoints are historical records, not current completion claims.

## Requirements and architecture

The two original ENAM assessment PDFs were read, extracted and visually inspected. They supersede interpretations in planning documents. Required: 15–20 mock holdings, portfolio Push, primary-source Pull beyond the watchlist, phone-friendly no-login public deployment, source provenance and an authentic AI history. Keep the existing FastAPI/SQLite backend and plain HTML/CSS/JavaScript frontend. No old Indian-equities/HDD project has been accessed or copied. Do not copy its code, datasets, credentials, storage assumptions or product scope; engineering principles alone are inspiration.

## Implemented and changed files

Typed FinancialFact/SourceEvidence/GuidanceRecord models and generic research retrieval/comparison replace issuer-specific answers (backend/app/models.py, evidence.py, research.py). Genuine reviewed PDF extraction and immutable-ID promotion are available through scripts/ingest_reviewed_pdf.py and promote_evidence.py, with manifests in demo/manifests. This remains operator-reviewed extraction, not autonomous PDF understanding.

Bounded optional Gemini reasoning, evidence-linked structured output, daily call/token reservations, concurrency limits, sanitized failures and caching are implemented in backend/app/reasoning.py. Deterministic calculations do not call Gemini. No live Gemini call has been tested; the key remains an environment placeholder. Mock tests establish adapter behavior only, not model answer quality.

Portfolio acquisition, real filing categories, configurable thresholds and filing alerts are implemented in scripts/refresh_portfolio.py, backend/app/analytics.py and main.py, frontend/app.js and style.css. Data changed in demo/bars.json, filings.json, evidence.json, facts.json and guidance.json. Tests changed in backend/tests/test_core.py, test_evidence.py, test_ingestion.py and test_reasoning.py. Deployment preparation: render.yaml, .env.example, scripts/smoke_url.py and docs/DEPLOYMENT_STEPS.md. Render has not built or served this app.

## Real coverage

18 mock holdings; 17 have 63 real daily bars each (1,071 total), 27 July–26 October 2026. 432 stored issuer filings span 17 holdings. TATAMOTORS provider attempts failed; no replacement series was fabricated. Acquisition report: ../evidence/phase3-acquisition.json; per-company counts: ../evidence/2026-10-28/coverage.json. Snapshot ingestion was 27 October; there is no live poller.

Eight source evidence records, 27 financial facts and two guidance records. INFY: curated reviewed primary-source notes, FY25 annual, Q4/Q3 FY25 and Q4 FY24; not newly extracted PDF evidence. HINDUNILVR: genuine downloaded FY25 report, consolidated FY25/FY24 revenue/PBT/total PAT and business passage. ASIANPAINT: genuine downloaded FY25 standalone statements, FY25/FY24 PBT/PAT/issuer-defined EBITDA and company background. Asian Paints total revenue is unverified. PDF publication dates are unknown and therefore excluded at explicit historical publication cutoffs. Approval dates are not publication dates. Original PDFs remain outside the repository; only minimal derived records are included.

## Actual research answers

1. “INFY Q4 FY25 revenue and PBT”: revenue INR40,925 crore, QoQ −2.01%, YoY +7.92%; PBT INR9,663 crore, QoQ −0.07%, YoY −5.63%. [Issuer results, PDF page 12](https://www.infosys.com/investors/reports-filings/quarterly-results/2024-2025/q4/documents/q4-and-12m-fy25-financial-results-auditorsreports.pdf). Evidence method: legacy curated note.
2. “HINDUNILVR FY25 consolidated revenue”: INR63,121 crore; FY24 INR61,896 crore. [Annual report, PDF page 186](https://www.hul.co.in/files/annual-report-2024-25.pdf). Evidence method: reviewed PDF extraction; consolidated, not standalone.
3. “ASIANPAINT FY25 standalone PBT and PAT”: PBT INR4,897.18 crore, YoY −30.03%; PAT INR3,584.88 crore, YoY −32.55%. [Standalone statements, PDF page 12](https://www.asianpaints.com/content/dam/asianpaints/website/secondary-navigation/investors/annual-reports/2024-2025/Standalone-Financial_Statements.pdf). This issuer is outside the mock watchlist and uses the generic pipeline, with no issuer answer branch. ZENSARTECH FY25 revenue correctly returns MISSING; no listing or financial coverage is invented.

Exact answer payloads and citations: ../evidence/2026-10-28/questions-resume.json.

## Executed validation

- `.venv/bin/python -m pytest -q`: 101 passed, one existing Starlette/httpx deprecation warning. Raw output ../evidence/2026-10-28/tests-resume.txt. Synthetic unit fixtures and mocked Gemini responses are distinct from the real issuer data above.
- `.venv/bin/python scripts/verify_replay.py`: 18 companies, 1,071 bars, 432 filings, eight evidence records, 27 facts, two guidance records. Raw output ../evidence/2026-10-28/replay-resume.txt.
- `node --check frontend/app.js` and `git diff --check` passed in the preceding verification.
- `.venv/bin/python scripts/refresh_portfolio.py --apply --report docs/evidence/phase3-acquisition.json` acquired the authentic portfolio snapshot on 27 October.
- Mobile/browser evidence captured 27 October: ../evidence/final/mobile-business.jpg, mobile-lt-filter.jpg and desktop-brief.jpg; mobile width 375 pixels and desktop 1200 pixels. These are dated evidence, not a new 28 October browser validation. Fresh browser verification remains pending at this checkpoint.
- Docker build was not tested: daemon unavailable. Public HTTPS smoke test has not run because no public URL exists.

## API usage and cost

Real Gemini calls: zero. Defaults: AI disabled, 20 calls/day, 50,000 reserved tokens/day, 800 output tokens/call, 12,000 evidence characters and two concurrent calls. SQLite reserves budget before provider requests, including failures; successful answers cache by query and corpus version. No automatic provider retries. These are usage caps, not a guaranteed monetary bill. Free ephemeral hosting must keep AI disabled until durable budget storage is configured. Usage payload: ../evidence/2026-10-28/usage-resume.json.

## Repository and setup

Branch main; inspected HEAD d2221e4b88c843ede399bd8db6047cd9bb5b30e3. All work above remains uncommitted; no push, remote setup, credentials or account creation. Obtain the exact current file list with `git status --short`, as subsequent fixes can extend it.

Local: `python3 -m venv .venv`, `.venv/bin/python -m pip install -r backend/requirements.txt`, `.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`. Optional PDF tools: backend/requirements-pdf.txt. Configure real secrets only on the server; never paste keys into documents or commit them.

## Remaining work, in priority order

1. Fix inconsistent default financial periods between company-detail and financial endpoints; test missing coverage and preserve explicit historical labels.
2. Recheck phone and desktop interactions on the current running version; address observed issues and save new proof.
3. Deploy existing Python app to a user-configured host, verify public no-login HTTPS with scripts/smoke_url.py. Credentials were deferred by the user; deployment remains mandatory and blocked on hosting configuration.
4. With a server secret available, run bounded real Gemini evaluations against authentic issuer evidence; inspect citation entailment, failures, budgets and cost. Never mark mocks as live tests.
5. Expand recent primary financial periods, quarterly and guidance history beyond INFY; correct TATAMOTORS listing/provider mapping using verified sources. Broaden reviewed extraction without weakening comparability/publication rules.
6. Finish submission repository/history URL, public phone demo and covering note. No submission email is authorized.

Known limits: historical narrow financial corpus; no automatic document discovery; keyword-based filing categorization; no rolling four-quarter management history; source publication dates incomplete; process-local request limits; ephemeral hosting budgets not durable; semantic entailment is not guaranteed by structured/numeric output checks. Disk space is low; no previous work was deleted.

## Post-checkpoint correction and verification — 28 October

Implemented priority 1: backend/app/research.py now provides company_financials(), selecting the newest verified financial period from issuer facts with quarterly preference at the same end date; backend/app/main.py uses it consistently for both company endpoints. Explicit research queries retain exact requested periods. Five regression cases were added in backend/tests/test_evidence.py, including genuine three-issuer endpoint consistency, missing ticker isolation and a synthetic FY24-only repository.

`.venv/bin/python -m pytest -q`: **106 passed, one existing deprecation warning**. Output: ../evidence/2026-10-28/tests-period-fix.txt. `node --check frontend/app.js` and `git diff --check` passed. Exact uncommitted status: ../evidence/2026-10-28/git-status.txt.

Fresh browser verification at 375×812: ASIANPAINT FY25 standalone PBT/PAT answered with the cited PDF, missing revenue remained blank, publication time remained explicitly unknown, and zero model calls were shown. Document scrollWidth 360 <= viewport 375; screenshot ../evidence/2026-10-28/mobile-asian-resume.jpg. This is responsive viewport evidence, not physical-phone certification. Local preview was restarted with the changed backend. Public deployment and live Gemini tests remain incomplete.
