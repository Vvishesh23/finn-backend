## Latest: Desktop source copy / frontend first

Read [GitHub and Render steps](GITHUB_RENDER_STEPS.md) and [Desktop/frontend handoff](docs/DESKTOP_FRONTEND_HANDOFF.md). 165 backend/nine frontend tests pass. The public-only frontend build is labelled as a preview; the complete backend and Gemini integration are preserved. No secret access, commit/push or hosting action was performed. Earlier checkpoints remain below.

## CP11 release handoff — 1 November 2026, INCOMPLETE

161 backend tests and eight frontend tests pass. No-key mobile/desktop paths were exercised; historical replay now hides later EOD cards, Latest import has a real pinned cutoff, and 429/503 retains source evidence. Eleven issuers/71 facts preserved.

**Public URL: NOT DEPLOYED / NOT PROVIDED. Live Gemini: NOT TESTED.** No real secret/account access, commit, push, purchase or email. Read [deployment handoff](DEPLOYMENT_README.md), [current CP11 checkpoint](docs/checkpoints/CP11_RELEASE_CHECKPOINT.md), [walkthrough results](docs/EVALUATOR_WALKTHROUGH_CP11.md), and [owner-only live test](docs/LIVE_VERIFICATION_CP11.md). Git HEAD alone lacks the uncommitted implementation. Earlier entries below are historical.

---

## CP10 — secure integration, 31 October 2026

Continued CP09 with 11 issuers and 71 facts preserved. **157 backend + 4 frontend tests pass** under a clean-environment runner with application network blocked. Disabled/mock/Google-SDK providers, persistent single-host inference budgets/leases, client-isolated caches, sanitized failures, bounded retries/timeouts and a privacy notice are implemented. **Live Gemini: NOT TESTED. Public deployment: NOT COMPLETE.**

No real Gemini key, secret file, production account or production environment was searched/read/configured. Do not run tests against production credentials or paste a key into chat. Git ignore rules do not isolate secrets from programs with the same OS permissions: production secrets belong on a separately controlled host, outside Codex access.

Read [CP10 and copy-ready review report](docs/checkpoints/CP10_SECURE_GEMINI.md), [owner-only secret setup/live tests](docs/SECURE_GEMINI_SETUP.md), and [CP11 procedure status](docs/checkpoints/CP11_DEPLOYMENT_READINESS.md). Test with `python3 scripts/run_isolated_tests.py -q`; demonstrate with `python3 scripts/run_isolated_tests.py --demo`. Direct pytest is deliberately refused to prevent ambient credentials entering tests. No commits or pushes. Earlier sections below are historical.

---

## Current status — CP09, 28 October 2026

Document-grounded financial research now covers **11 issuers**, with **16 evidence records and 71 facts**. Eight additional issuer PDFs were downloaded, statement pages visually reviewed, and all 44 new facts reproduced exactly from pinned manifests. Legacy Infosys curated notes remain labelled separately. Coverage is selected FY25/FY24 metrics, with additional POWERGRID and Infosys quarter comparisons; it is not comprehensive company research.

Robustness changes include consistent Decimal unit normalization (thousands/millions/crores), explicit accounting/metric definitions, mixed-currency rejection, dynamic issuer/period/basis coverage, cache revalidation and guards against stale asynchronous UI responses. **128 backend tests and 4 frontend race tests pass.** Fresh mobile WIPRO/ICICI and desktop coverage evidence is saved.

Read [CP09](docs/checkpoints/CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md) and [robustness matrix](docs/ROBUSTNESS_MATRIX.md). Exact test outputs, source acquisitions, eleven research answers/citations and remaining blockers are included. Public deployment, live Gemini validation, broad transcript/quarterly coverage and four-quarter guidance history remain incomplete. No credentials, old HDD dependencies, commits or pushes were introduced. Prior entries below are historical.

---

## Current verified state — 28 October 2026

Read [CP08](docs/checkpoints/CP08_PORTFOLIO_PUSH_AND_HANDOFF.md) for the current requirements, architecture, changed files, source-linked research examples, real coverage, commands, limitations and priority steps. Earlier sections below are historical and may describe narrower coverage.

The original ENAM PDFs have now been read. Current corpus: 18 mock holdings, authentic EOD data for 17 (1,071 bars), 432 filings, eight evidence records, 27 facts and two guidance records. Genuine reviewed HUL and Asian Paints PDFs are distinguished from legacy curated Infosys notes. No old HDD project content was used.

Latest implementation fixes company-detail versus financial-endpoint inconsistency. Both select the most recent verified financial period from the issuer corpus, with a quarter preferred at the same period end; explicit research periods never silently fall back. Missing tickers stay missing and ambiguous reporting bases remain unresolved. Regression tests cover three real issuers, an unknown ticker and a synthetic earlier-only corpus.

Validation: 106 tests passed, one existing Starlette/httpx deprecation warning; JavaScript syntax and git whitespace checks passed. Raw results: docs/evidence/2026-10-28/tests-period-fix.txt. Fresh 375×812 browser research verified ASIANPAINT FY25 standalone PBT/PAT and source provenance, zero model calls; document scroll width 360 versus viewport 375. Screenshot: docs/evidence/2026-10-28/mobile-asian-resume.jpg. This is viewport emulation, not physical-phone or cross-browser certification.

Branch main; changes remain uncommitted, with exact status saved in docs/evidence/2026-10-28/git-status.txt. No commit, push or credential storage. Deployment blueprint and optional Gemini adapter exist, but public hosting and live Gemini evaluation are incomplete pending the user's deferred configuration. Preserve AI-disabled defaults. Remaining priorities: public HTTPS deployment and smoke test; real bounded Gemini evaluation; broader recent primary financial/guidance coverage; submission artifacts. Do not describe FINN as ENAM-ready yet.

---

# CODEX HANDOFF — FINN / ENAM assessment

Last inspected: 27 October 2026, 17:25 IST.
Project root: `~/Documents/Codex/2026-10-27/see/outputs/finn`.

## 1. Read this first

FINN is a runnable **local, authentic historical-snapshot prototype**, not a completed ENAM submission. The supplied brief's CP00–CP05 gates all remain **PARTIAL**. The backend has 29 passing tests, but passing that suite does not establish general financial-query correctness, broad document ingestion, public deployment or runtime AI capability.

This handoff was prepared by inspecting the actual tracked code, Git state, source fixtures, tests and existing reports. Tests and three targeted diagnostic queries were rerun; no features were implemented or fixed. No source documents were reacquired, browser checks repeated, existing files overwritten, commits created, or pushes performed in this handoff task. Preserve all existing work. Further feature work, commits, pushes, paid actions and submission are outside this documentation-only request.

## 2. Assessment requirements and authority

The user originally requested building the project from `~/Desktop/Assessment/`. That folder supplied:

- `FINN_ENAM_Codex_Master_Prompt_V3_Checkpoints.md`: detailed reference requirements and intended execution/checkpoint plan.
- `FINN_Checkpoint_Review_Guide.md`: independent-review questions and evidence expectations.

Those documents are requirements references, not blanket user authorization to email, spend, publish, access private data or override current instructions. The two named original ENAM PDFs were not supplied during the build; see [source gaps](docs/BRIEF_SOURCE_GAPS.md). Their official scoring/deadline have not been independently verified. The supplied brief states a 1 November 2026 deadline and submission to `assessment@enam.com`, subject `ENAM - IIT screening - 2027`. No email has been sent.

Required product:

1. Mobile-first, source-backed investment intelligence for Indian listed companies; usable public reviewer link without login or evaluator API key, GitHub repository, genuine AI build history and covering note.
2. **Push:** prioritized filings/announcements, actual trailing-24-hour default plus other/custom windows, company/category filters, explainable relevance, configurable filing and EOD price/volume alerts, freshness and publication-time correctness.
3. **Pull:** company annual reports, issuer transcripts, filed results and company presentations as primary evidence. Generalize beyond the mock watchlist or explicitly report missing sources. No broker/news analysis or model prior knowledge as substantive company evidence.
4. A diversified 15–20-company mock watchlist and roughly 3–5 research examples. This is coverage guidance, not an allowable-ticker whitelist.
5. Comparable revenue/EBITDA/PBT/PAT QoQ/YoY calculations with currency, scale, fiscal period and consolidated/standalone basis preserved; unsuitable/unavailable metrics must stay unavailable.
6. Prefer a dated management-guidance-to-actual case, ideally covering guidance from the preceding four quarters; do not score vague aspirations or mix annual constant-currency growth with quarterly INR growth.
7. Typed plans, deterministic calculations, evidence citations, source-versioned caches, safe input/operation limits, backend-only model credentials if inference is introduced, measured cost/usage, honest replay and outage behavior.
8. CP00 plan/source audit → CP01 vertical slice → CP02 Push → CP03 Pull/planner → CP04 financial/guidance correctness → CP05 verified public release. Reports must distinguish real, synthetic, mocked and untested evidence.

## 3. Crucial separation from the older Indian-equities/HDD project

| FINN assessment | Older project context, as described in the brief |
|---|---|
| Independently authored investor-intelligence application | Historical daily/intraday datasets, research/backtests, event/feature stores and market-data reconciliation |
| Newly acquired permitted public sources and a portable local replay | Private historical corpus, external HDD and old project outputs must not become dependencies |
| Filing relevance, primary-source research and verifiable calculations | Strategy economic findings were explicitly uncertified for live use and prove no FINN signal |
| No trading, broker integration, alpha prediction or portfolio optimization | Strategy, simulator, execution and cash-ledger machinery is outside this assessment |

**May recreate independently:** point-in-time causality, provenance, distinct report/publication/effective/ingestion dates, strict schemas, units/basis reconciliation, immutable raw evidence, duplicate handling, prior-session baselines, reproducible tests, fail-closed uncertainty and versioned caches. Their current limited implementations live in `analytics.py`, `models.py`, `store.py` and `research.py`; do not imply complete certification.

**Must not access or copy:**

- The Seagate drive or `/Volumes/Seagate Portable Drive/Hedge Fund/data`, `quant_data`, the described 3,410 time series, private historical market data, HDD originals, prior trades/results or Phase 3A–3G artifacts. Do not locate, mount, scan, index, hash, upload or audit them.
- Old repository code, classes/functions, helper packages, legacy test datasets, infrastructure, stored research inputs or environments. Do not fetch/vendor the old project or require it for setup/deployment.
- Trading strategies, alpha/performance scores, backtests, broker/order logic, settled/unsettled cash ledger or simulator.
- Old credentials, tokens, account permissions, private datasets, UI designs, screenshots or product assets. Prior access or findings are not permission or evidence for FINN.

Build records state no old repository/HDD was accessed. This handoff inspected neither. See [engineering heritage](docs/ENGINEERING_HERITAGE.md) for the existing separation statement.

## 4. Git state and changes

Observed before creating this file:

- Branch: `main` (`git symbolic-ref --short HEAD`).
- HEAD: `d2221e4b88c843ede399bd8db6047cd9bb5b30e3` — `Record actual implementation commit and local release evidence`.
- Previous implementation commit: `1fb56b584fb37cfb382ad66b91c4798060464b22` — `Build independent FINN public-source local prototype with evidence and tests`.
- `git status --porcelain`, unstaged diff and staged diff were empty. `git remote -v` returned no configured remote. No GitHub URL exists.
- `docs/GIT_STATE.txt` deliberately identifies the earlier implementation commit; it is not the current HEAD. Prior commits identify the coding agent as `Codex <codex@localhost>`.

**Changes in this task:** only new, untracked `CODEX_HANDOFF.md`; expected status after creation is `?? CODEX_HANDOFF.md`. No staging/commit/push. Ignored local `.venv/`, caches and `finn.sqlite3` exist; a clean Git status does not mean they are absent. Preserve them. Existing `../FINN-project.zip` is a prior snapshot and is not regenerated to include this handoff.

Git on this machine is old: use `git symbolic-ref --short HEAD`, not `git branch --show-current`. The earlier build also used `git init` then `git checkout -b main` because `git init -b main` was unsupported.

### Existing implementation file inventory

All following paths predate this handoff; this is a map of prior work, not a claim they changed now.

| Files | Actual responsibility |
|---|---|
| `backend/app/main.py` | FastAPI routes, startup fixture validation, POST body/rate limits, response security headers, same-origin frontend serving |
| `backend/app/models.py` | Company/bar/document/filing/event/query/plan/rule Pydantic definitions; symbol and query validation |
| `backend/app/analytics.py` | Decimal percentage math, generic dimension comparison helper, anomalies, category ranking, exact-attachment grouping, timestamp digest and guidance-band outcome |
| `backend/app/store.py` | JSON loading; SQLite raw filing, answer and alert tables; locks and persistence |
| `backend/app/research.py` | Rule planner, curated Infosys facts/guidance, fixed source summaries, keyword retrieval, answer cache and process counters |
| `backend/tests/test_core.py` | 29 parameter-expanded offline unit/API checks, with in-memory database and synthetic edge cases |
| `frontend/index.html`, `frontend/style.css`, `frontend/app.js` | Responsive Brief/Companies/Research/Settings, details dialog, filters, queries, source links, browser-local thresholds |
| `demo/companies.json`, `bars.json`, `filings.json`, `documents.json`, `acquisition.json` | Mock watchlist, genuine public snapshot, derived source notes and acquisition outcomes |
| `scripts/import_public.py`, `scripts/verify_replay.py` | Bounded raw acquisition/offline PDF extraction CLI; fixture schema/count verification |
| `start.sh`, `backend/requirements.txt`, `.env.example`, `pytest.ini` | Local setup, dependency pins, optional DB setting and pytest discovery |
| `Dockerfile`, `.dockerignore`, `.gitignore` | Deployment preparation and exclusions; Docker build not verified |
| `README.md`, `docs/*.md`, `docs/GIT_STATE.txt` | Setup, decisions, architecture, provenance, limitations, resume/submission and review records |
| `docs/test-output.txt`, `docs/security-scan.json`, `docs/evidence/*` | Earlier raw test output, limited token-pattern scan, interactive-browser notes and actual screenshots |
| `docs/checkpoints/*` | CP00–CP05 reports, index and latest checkpoint; all PARTIAL |

## 5. Actual architecture and storage behavior

```text
Public NSE/Yahoo acquisition CLI -> raw JSON imports (not auto-promoted)
Reviewed versioned demo JSON -> FastAPI startup / in-memory company, bar and document lists
                            -> SQLite raw_filings (INSERT OR IGNORE by ID)
SQLite raw filings -> cutoff filter -> exact attachment grouping -> rule relevance -> Brief
Bars -> prior-20-session evaluator -> active observations -> SQLite deduplicated alerts
Research query -> validated regex plan -> curated facts/source-note retrieval -> SQLite cache
All responses -> same-origin HTML/CSS/JavaScript -> publisher source links
```

One Python service serves both API and UI. Default DB: project-root `finn.sqlite3`; `FINN_DB` overrides the path. Tables: `raw_filings`, `answers`, `alerts`. Company/bar/document JSON is loaded at process import and requires restart after edits. Existing raw filing IDs are not updated from edited fixtures because initialization uses `INSERT OR IGNORE`. Corrections require an explicit version/import approach; do not delete the database to hide this behavior.

The answer key contains plan, normalized question, document-note IDs/hashes and literal version `extractive-v4`. It does **not** automatically hash hardcoded financial/guidance code or raw filing revisions. Change the answer version when relevant implementation/facts change. Usage counters and rate queues are process-local; SQLite is not a distributed quota solution.

API routes actually present: `/health`, `/api/watchlist`, `/api/brief`, `/api/company/{symbol}`, its `/filings`, `/financials`, `/guidance` children, `/api/alerts`, `/api/research/query` (POST), `/api/source/{id}`, `/api/usage`, `/` and `/assets`. No server settings-write endpoint: thresholds are browser `localStorage` values sent as alert query parameters. GET alerts recalculates and persists deduplicated observations. No background ingestion/scheduler, notifications, model SDK, FTS/vector index, authentication or trading service exists.

## 6. Completed local behavior, with evidence limits

- Brief filters imported filings by timezone-aware publication cutoff before grouping, supports company/category selection, category-first relevance with recency tie-breaks, custom windows and a distinct FY25 replay. Frontend includes routine-disclosure collapse.
- Mock watchlist has 18 labels; only INFY, RELIANCE and HDFCBANK have prices. Unknown valid ticker syntax yields honest missing-source/listing-unverified status, not generic exchange discovery.
- EOD observations compare price to preceding close and volume to the previous 20 finalized bars. Warm-up, invalid data, incompatible provider/basis and supplied corporate-action flags are handled. Actual corporate-action feed and exchange-calendar completeness are absent.
- Details expose exchange timestamps, raw source metadata and links. The curated Infosys Q4 FY25 table includes revenue/PBT/total profit versus Q3 FY25 and Q4 FY24; EBITDA stays missing. Total profit includes non-controlling interests.
- Supported research questions use fixed, manually verified Infosys data/source summaries. Broader questions get keyword-selected source notes and a no-model explanation. Plans are typed rule outputs; there is no general reasoning engine or generic operation executor.
- Initial FY25 guidance case: 1–3% constant-currency growth versus reported 4.2%; 20–22% operating-margin guidance versus 21.1%. This is not a four-quarter/revision-aware management-quality assessment. Call dates and later exchange transcript publication dates are distinguished in citations.
- SQLite exact-question/evidence caching, exact URL/hash grouping, raw-row preservation and alert deduplication exist. Semantic cross-exchange relationships and a full revision lifecycle do not.
- No runtime inference key/calls/cost is required. The code's counters start at zero; development subscription cost/usage was not measured.

Source-link presence and saved earlier browser captures are evidence of the narrow local journey, not proof that every control, issuer, period or upstream error is covered. See section 9 for newly reproduced failures.

## 7. Data sources and freshness

| Data | Shipped evidence | Access/freshness qualifications |
|---|---|---|
| Yahoo Finance chart API | `demo/bars.json`: 189 raw OHLCV bars, 63 each for INFY.NS, RELIANCE.NS, HDFCBANK.NS; 27 July–26 October 2026 | Original acquisition returned 64 each; acquisition-day bar omitted conservatively. Snapshot only, no current feed. |
| NSE announcements | `demo/filings.json`: 20 Infosys records selected from a reported 2,942-row API response | Acquired 27 October 2026; latest selected disclosure 27-Oct-2026 16:38:30 IST. No BSE feed implemented. |
| Infosys results | `infy-results-fy25`: derived consolidated Ind-AS facts, original PDF page 12 | Manual web-reader verification recorded; direct download HTTP 403. |
| Infosys calls | `infy-call-fy24`, `infy-call-fy25`: minimal paraphrases, page/section refs | Calls 18-Apr-2024 and 17-Apr-2025; exchange transcript publication 23-Apr-2024 and 22-Apr-2025 respectively. Not original PDF text indexes. |
| Infosys annual report | `infy-ar-fy25`: FY25 annual-report HTML CEO-letter note | Exact HTML publication timestamp unverified; no original annual-report PDF bundled. |

Actual source endpoints include:

- `https://query1.finance.yahoo.com/v8/finance/chart/INFY.NS?range=3mo&interval=1d` (analogous RELIANCE/HDFCBANK URLs).
- `https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=INFY`.
- `https://www.infosys.com/investors/reports-filings/quarterly-results/2024-2025/q4/documents/q4-and-12m-fy25-financial-results-auditorsreports.pdf`.
- `https://www.infosys.com/investors/reports-filings/quarterly-results/2024-2025/q4/documents/transcripts/earningscall.pdf`.
- `https://www.infosys.com/investors/reports-filings/quarterly-results/2023-2024/q4/documents/transcripts/earningscall.pdf`.
- `https://www.infosys.com/investors/reports-filings/annual-report/annual-reports/ar-2024-25.html`.

See [acquisition](docs/PUBLIC_DATA_ACQUISITION.md), [full per-record provenance](docs/REPLAY_DATA_PROVENANCE.md), `demo/acquisition.json` and [rights caveats](docs/DATA_SOURCES_AND_LICENSES.md). Direct issuer requests returned 403; three NSE attachment download attempts timed out, per earlier records. No bypass was attempted. No new source availability check was made for this handoff. `work/sources/*` paths recorded in acquisition JSON refer to earlier workspace scratch data, not bundled project files or runtime dependencies. Source-note hashes identify derived notes, not original PDF bytes. Public availability does not establish hosting/redistribution rights.

## 8. Decisions to preserve or reconsider explicitly

- Prioritize a small working, inspectable investor workflow over reconstructing a historical data platform.
- FastAPI + SQLite + plain HTML/CSS/JavaScript was deliberately chosen instead of recommended Next.js/TypeScript/Tailwind. No npm/frontend build step is required. This is a stack deviation, not a Next.js implementation.
- Use authentic snapshots and explicit missing states rather than invented prices, current filings, research or guidance.
- Curated financial facts and fixed answers are a prototype shortcut. `financials()` does not execute the tested generic `compare()` helper; its comparability depends on the manually curated fixture.
- CLI imports stay raw/unverified; no unreviewed PDF content is promoted automatically. The current import tool is not a completed ingestion/indexing pipeline.
- No runtime model was integrated, rather than assuming Codex usage grants API credits. Any later provider/model/quotas require current verification and backend-only secrets.
- Single-process local deployment is the supported architecture today. No public deployment or remote repository exists.

## 9. Verification, known bugs and untested areas

### Executed again for this handoff

From project root, preserving existing reports and using in-memory test storage:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider
FINN_DB=:memory: PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/verify_replay.py
node --check frontend/app.js
```

Observed: **29 passed, 0 failed, 1 warning, 0.51 seconds**. Warning: upstream Starlette TestClient deprecates its current httpx integration. Fixture validation: 18 companies, 189 bars, 4 document notes, 20 filings; price range 2026-07-27 through 2026-10-26. JavaScript syntax check exited successfully. Tests set `FINN_DB=:memory:`; the replay command explicitly used it too. Existing `docs/test-output.txt` was not overwritten.

The suite checks health/watchlist, publication cutoffs, future duplicate exclusion, exact grouping, synthetic revision/hash invalidation, distinct record dates, dimension/scale/zero checks, anomaly baseline/warm-up/NaN/action flag, persisted alert ID dedupe, unknown ticker, selected unsafe inputs, no-model/cache behavior, guidance range, source-ID resolution, typed errors, one unsupported-period example, headers/body size, per-client request limit, and one annual-versus-quarter case.

**Do not overstate coverage:** revision test changes an in-memory note hash, not a real revised-filing pipeline. The injection test supplies hostile query text with no model/tool dispatch; it does not test an injected PDF through an LLM. Rate test exercises 31 same-client requests, not global multi-client quotas or concurrency. Finance helper tests do not prove all served query paths validate dimensions. Schema/count checks do not reverify source authenticity or licences.

### Reproduced bugs — not fixed in this task

Diagnostic method: a separate process with `FINN_DB=:memory:` and `PYTHONDONTWRITEBYTECODE=1`, calling `research.answer(Query(symbol='INFY', question=...))`.

| Priority | Input | Actual incorrect/incomplete behavior |
|---|---|---|
| HIGH | `FY2026 revenue` | Returns `VERIFIED_DERIVED` Q4 FY25 revenue (40,925 crore), because the unsupported-period regex does not match the joined `FY2026` token. The passing `Latest FY26 revenue` test does not cover this. |
| HIGH | `Q4 FY25 guidance` | Plan says Q4 historical default, but answer returns the full-year FY25 initial-guidance comparison as verified. Quarter/annual target-period matching is not enforced. |
| MEDIUM | `Q4 FY25 revenue and PBT` | Returns revenue only. Planner chooses the first recognized metric; the special multi-metric case covers “revenue” plus “profit”, not PBT. |

Additional code-inspection risks, not newly demonstrated as runtime failures:

- `answer()` annual-financial, guidance, business and cash summaries are Infosys-specific text selected after finding documents for a ticker. Adding documents for a second issuer without generalizing these branches could serve Infosys claims for that issuer. Do not merely append another issuer to `documents.json` and declare generic research complete.
- `compare()` checks metric/basis/currency/period_type/scales, not actual quarter adjacency, fiscal calendar, entity/segment or explicit period ranges; served curated financials bypass it.
- Raw filing revisions alone do not invalidate the answer cache; fixed numbers/code changes also need an explicit version change. Same-ID seed edits do not replace persisted raw rows.
- Broad keyword category rules, e.g. “outcome of board”, can overclassify as results. Ranking is relevance, not demonstrated financial materiality or predicted return.
- Async frontend requests have no cancellation/stale-response guard. Rapid navigation/filter changes could display an older response; not reproduced in this task.
- Frontend EOD observations use latest snapshot even with FY25 filing replay selected; dates are shown but this is not a historical as-of alert replay. Company cards use default observation thresholds rather than browser-custom rules.
- Raw import filenames can be reused/overwritten by the CLI. There is no append-preserving promotion workflow. Do not run acquisition as part of this documentation task.

### Earlier verification only / not rerun now

[TEST_RESULTS](docs/TEST_RESULTS.md), [browser record](docs/evidence/browser-checks.json) and `docs/evidence/*.jpg` record interactive local checks at observed 375×812 CSS pixels and desktop 1200×800; no page overflow, six replay versus one then-recent disclosure, three volume observations at 0.1× versus zero at 2×, guidance citations and unknown-ticker behavior. Screenshots have documented capture-scaling limitations. These are earlier interactive checks, not a frontend automated suite or physical-phone lab. The trailing-24-hour result is clock-dependent and must not be assumed to remain one.

Not verified: public URL, current server availability, Docker build, new clean install during this handoff, production concurrency/persistence, original primary-PDF parsing end-to-end, broad issuer/period correctness, runtime model responses/keys/quotas, current upstream accessibility, automatic corporate-action/session handling, full challenge compliance or submission. Earlier token-pattern scan is limited evidence, not a security certification.

## 10. Setup and safe continuation commands

Run from this project root, with Python 3.12+:

```sh
cd ~/Documents/Codex/2026-10-27/see/outputs/finn
./start.sh
```

`start.sh` creates `.venv` if absent, runs pip installation on every invocation, then binds to `127.0.0.1:${PORT:-8000}`. Network is needed for dependencies on initial setup and may be contacted on later starts. For an already installed environment:

```sh
.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`; localhost is not an evaluator-accessible public URL. No account or model key required. Optional `FINN_DB` selects a writable SQLite file. `.env.example` is documentation; code does not load `.env` automatically. Do not overwrite/delete the existing DB or stop an existing server without checking its state and preserving work.

For a fresh clone without a virtual environment:

```sh
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
.venv/bin/python -m pytest backend/tests -q
```

Pinned direct dependencies: FastAPI 0.162.0, Uvicorn 0.54.0, httpx 0.28.1, pytest 9.1.1. Optional PDF CLI requires a separately installed PyMuPDF; it is not in shipped requirements. Its presence in a prior development environment does not establish clean-install PDF support.

Acquisition commands below are **future commands, not executed in this handoff**:

```sh
.venv/bin/python scripts/import_public.py prices --symbol INFY
.venv/bin/python scripts/import_public.py nse --symbol INFY
# With a legally obtained local PDF and optional PyMuPDF installed:
.venv/bin/python scripts/import_public.py document --symbol INFY --file report.pdf --url https://publisher.example/report.pdf --title 'Issuer report' --published YYYY-MM-DD
```

These save unverified JSON into `demo/imports/`; they do not update served facts/documents. Publisher citation and local PDF rights require review. Respect access controls and do not bypass failed requests.

## 11. Remaining implementation steps in priority order

No items below were implemented by this documentation task.

1. **P0 — Repair query correctness before expanding coverage.** Add regression cases for the three reproduced bugs; canonicalize fiscal-year/quarter forms, reject unsupported/ambiguous periods explicitly, enforce guidance target period, and support multiple requested metrics. Make evidence status reflect actual support. Clear/version affected cached answers safely.
2. **P0 — Separate issuer-specific facts from generic answering.** Move curated facts/guidance into typed evidence-linked records with company, period, basis, scale/unit, currency, source location and verification status. Drive answers from those records, validate exact period comparability, and bind citations by ID/type instead of `docs[0]`. Remove the second-issuer contamination risk before indexing another company.
3. **P0 — Reconcile original assessment and source permissions.** Obtain original PDFs from the user if available, confirm official requirements/deadline, and review allowed acquisition/redistribution. Preserve the no-HDD boundary. Do not claim source rights merely because an endpoint returned 200.
4. **P0 — Complete a small reproducible primary-document ingestion path.** Extract genuine permitted annual-report/transcript PDFs with pages/offsets/hashes; normalize/review/promote records without overwriting prior evidence. Connect imported data to the app and retest from a fresh clone. Use explicit missing states for failures. Add more issuers only after step 2.
5. **P0 — Strengthen Push source coverage and lifecycle.** Verified symbol identity/aliases, generic normalized acquisition, more filing issuers/categories, category-based alert preferences, same-ID/correction handling, revision-driven cache invalidation, cross-exchange evidence relationships, session/corporate-action checks and robust frontend response ordering. Distinguish latest-snapshot observations from true historical-as-of replay.
6. **P0 — Prepare and verify public release in an authorized environment.** Source rights first; then an explicitly authorized free host/repository. Use the supplied one-service deployment design, test persistent SQLite and actual no-login mobile HTTPS journey. Do not start paid billing or push to an account without authorization. Dockerfile existence is not a passing build/deployment test.
7. **P1 — Expand research within measured evidence coverage.** Build searchable primary passages, business/trajectory/cash/debt support and a generic typed executor. Decide whether runtime reasoning adds value. If used, verify provider/model, keep keys backend-only, enforce real request/token/concurrency budgets and provider failure fallbacks, then test with mocks and record real usage separately. Do not claim no-model tests validate Gemini.
8. **P1 — Expand financial and promise coverage.** Four-quarter guidance with revisions, exact target/actual period/entity matching, quarterly/YTD/annual reconciliation, applicable bank metrics and additional genuine cases. Preserve missing EBITDA and distinguish percentage from percentage-point gaps.
9. **P1 — Release-quality verification and evidence.** Add frontend/mobile automation where useful, upstream-outage cases, broader query/finance regressions, global/concurrent quota tests if relevant, source-link checks and clean-start/deployment evidence. Reassess security beyond token patterns. Update checkpoints with actual results, not planned successes.
10. **P1 — Final handoff/submission.** Update the covering note with real deployed/GitHub URLs and a genuine conversation export/share link. Re-run the short reviewer journey and update CP05 only when its gate genuinely passes. Sending the assessment email requires explicit user authorization. Commit/push only when the user asks; this handoff request explicitly does not authorize either.
11. **P2 — Optional extras only after the core release works.** Notifications, richer charts, embeddings, sector context and other enhancements should not delay correctness and evaluator access.

## 12. Existing plans, checkpoints and evidence to read next

There is no separate `IMPLEMENTATION_PLAN.md`; the original master brief, product decisions, resume plan, worklog, architecture and deployment/submission checklists contain the existing plan. Do not invent an additional completed planning artifact.

- [README / running demo](README.md)
- [Product decisions and scope](docs/PRODUCT_DECISIONS.md)
- [Actual architecture](docs/ARCHITECTURE.md)
- [Resume instructions and next tasks](docs/RESUME_HERE.md)
- [Worklog](docs/WORKLOG.md)
- [Engineering heritage / explicit exclusions](docs/ENGINEERING_HERITAGE.md)
- [Acquisition](docs/PUBLIC_DATA_ACQUISITION.md), [provenance](docs/REPLAY_DATA_PROVENANCE.md), [rights](docs/DATA_SOURCES_AND_LICENSES.md)
- [Known limitations](docs/LIMITATIONS.md), [test report](docs/TEST_RESULTS.md), [earlier raw output](docs/test-output.txt)
- [Demo walkthrough](docs/DEMO_WALKTHROUGH.md), [deployment steps](docs/DEPLOYMENT_STEPS.md)
- [Authentic AI build summary](docs/AI_BUILD_LOG.md), [submission checklist](docs/SUBMISSION_CHECKLIST.md), [covering draft](docs/COVER_EMAIL_DRAFT.md)
- [Checkpoint index](docs/checkpoints/CHECKPOINT_INDEX.md)
- [CP00: plan/source audit](docs/checkpoints/CP00_PLAN_AND_SOURCE_AUDIT.md)
- [CP01: running skeleton](docs/checkpoints/CP01_RUNNING_SKELETON.md)
- [CP02: Push](docs/checkpoints/CP02_PUSH_WORKFLOW.md)
- [CP03: Pull/planner](docs/checkpoints/CP03_PULL_AND_QUERY_PLANNER.md)
- [CP04: management/correctness](docs/checkpoints/CP04_MANAGEMENT_AND_CORRECTNESS.md)
- [CP05: incomplete public release](docs/checkpoints/CP05_FINAL_RELEASE.md)
- [Latest checkpoint snapshot](docs/checkpoints/LATEST_CHECKPOINT.md)

The new query probes in this handoff qualify the older checkpoint claims: supported demo examples pass, but period and multi-metric handling remain incomplete. Earlier documents are preserved as historical records, not silently rewritten. Start the next implementation task with the reproduced correctness bugs, keep the prototype runnable, and require evidence before advancing any checkpoint.


## Continuation — local query-correctness fixes (27 October 2026)

The user subsequently asked to continue. This section supersedes the earlier statement that the reproduced query bugs remain unfixed; the initial inspection above is preserved as history.

Changes remain uncommitted on main: backend/app/models.py, backend/app/research.py, backend/tests/test_core.py, this handoff and appended progress notes. No commit or push performed. HEAD remains d2221e4b88c843ede399bd8db6047cd9bb5b30e3.

Implemented and tested:
- Conservative fiscal-period normalization accepts FY25/FY2025/FY 2025/FY2024-25/FY 2024/2025 for annual FY25 facts. Unsupported years, conflicting periods, relative periods, unsupported quarters and quarterly guidance fail closed. This is a bounded rule parser, not general natural-language date understanding.
- Typed plans preserve a metrics list; revenue plus PBT now answers both. Annual answers use the requested metrics too. Missing-only metric requests return MISSING; mixed supported/missing requests return PARTIAL.
- Financial source citations resolve the explicit result-document ID instead of positional docs[0]. Cache version changed from extractive-v4 to extractive-v5-period-metrics so old erroneous answers are not reused; existing cache rows were not deleted.
- A guard prevents issuer-specific Infosys fixed summaries being unlocked merely by adding another issuer's document. This does not implement generic issuer facts; that remains the next substantial step.

Verification: first regression run reproduced 14 failures with 36 passing cases. After fixes, 55 tests pass, zero fail, one existing Starlette/httpx deprecation warning. Final command: PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider (0.50 seconds). Includes five HTTP API regression cases. node --check frontend/app.js also passed. No new browser, live provider, PDF import, cloud deployment or model tests were run. A running server needs restart to load backend changes; no claim that an existing preview process was restarted.

Remaining next priorities: typed issuer-specific evidence/fact records and generic answer execution, strict source/fact validation and period comparability, then permitted document ingestion/coverage and public release. All CP00–CP05 gates remain PARTIAL. Original source/rights, HDD exclusions, no-model and deployment limitations remain in force. No additional source data, features beyond this correctness patch, archive regeneration, account setup or email sending occurred.
