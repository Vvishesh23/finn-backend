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

# FINN — Project summary for independent GPT review

Prepared 27 October 2026. This document describes the actual local implementation and known gaps. It is not a claim that the ENAM assessment is complete.

## Prompt to give GPT

Please review this FINN prototype as a skeptical ENAM assessment evaluator and senior financial-software engineer. Separate implemented functionality from curated demonstration data, synthetic tests, planned work and unverified claims. Rank issues BLOCKER/HIGH/MEDIUM/LOW, identify the next three concrete improvements, and say whether it is ready for public assessment submission. Check financial periods, source provenance, whether the product genuinely answers research questions, mobile usability, ingestion generality and hidden operational costs. Do not assume that passing tests proves general correctness. If you need source files or test evidence, request them explicitly rather than accepting this summary as proof.

## 1. What the assessment asks for

FINN is intended to be a mobile-first Indian-equities intelligence agent with two connected workflows:

- **Push:** a prioritized filing digest, real time-window/company/category filters, configurable EOD price/volume alerts and original-source drill-down.
- **Pull:** research grounded in company annual reports, issuer earnings-call transcripts, filed results and company presentations; concise answers with citations and useful missing-source behavior for unfamiliar tickers.

Expected differentiation includes comparable quarterly revenue/EBITDA/PBT/PAT calculations and management guidance versus delivered results. Expected submission includes a publicly accessible no-login/no-evaluator-key demo, GitHub repository, genuine AI build history and covering note.

The supplied requirements were two Markdown documents in the Assessment folder. The original ENAM challenge PDFs were not supplied, so the exact official requirements and deadline are not independently verified. All CP00–CP05 gates remain PARTIAL.

## 2. What has actually been built

### A. Local interface

Four responsive screens: **The Brief, Companies, Research and Settings**. Company and filing details open in a dialog. Original source links and dates are visible. The frontend is HTML/CSS/plain JavaScript; there is no frontend build step, Next.js, TypeScript or Tailwind.

### B. Filing digest

- Default trailing 24 hours uses the actual current clock against imported snapshot records.
- Seven-day, custom-date and explicit FY25 replay windows.
- Company and category filters, rule-based category ranking, routine-event collapse and original-source details.
- Publication cutoffs apply before duplicate grouping so later source records do not leak into an earlier filing digest.
- Exact attachment URL/hash grouping preserves source records. It is not a complete semantic cross-exchange deduplication/revision system.

### C. Watchlist and EOD observations

- 18-company illustrative cross-sector mock watchlist, not a personal portfolio or certified current listing master.
- Actual price data for only **INFY, RELIANCE and HDFCBANK**; other cards explicitly lack price coverage.
- Configurable absolute close-to-close percentage threshold and volume multiple against the previous 20 finalized bars, excluding the current bar.
- Browser-local saved thresholds; results are recalculated on request and observed alert IDs are persisted without duplicates.
- Synthetic tests cover insufficient history, invalid values and an explicitly supplied corporate-action flag. A real corporate-action feed/calendar audit is absent.
- No scheduler, live price feed, browser notifications or trading integration.

### D. Research and query planner

- Validated ticker syntax and typed rule-based intent/period/metrics plans.
- Supported historical questions use **curated Infosys facts and fixed source summaries**, not a general financial-research model.
- Several fiscal-year spellings normalize to FY25. Tested unsupported/ambiguous periods return missing evidence. This is a bounded regex parser, not general date-language understanding.
- Multiple requested metrics are retained. Missing-only metrics return MISSING; mixed supported/missing results return PARTIAL.
- Broader questions return keyword-retrieved source notes plus a truthful no-model explanation.
- Valid unfamiliar tickers report missing coverage; there is no automatic discovery/indexing for arbitrary issuers.
- Evidence-versioned SQLite cache; repeated identical questions can avoid recomputation. Current cache version: extractive-v5-period-metrics.
- No runtime model, API key, billable inference, embeddings or vector database. Development subscription usage was not measured.

### E. Financial comparison and initial-guidance case

Curated Infosys consolidated Ind-AS figures, in INR crore:

| Metric | Q4 FY25 | Q3 FY25 | Q4 FY24 |
|---|---:|---:|---:|
| Revenue | 40,925 | 41,764 | 37,923 |
| PBT | 9,663 | 9,670 | 10,240 |
| Total profit / PAT including non-controlling interests | 7,038 | 6,822 | 7,975 |
| EBITDA | Not verified | Not verified | Not verified |

Percentage changes are calculated deterministically. For example, revenue QoQ is -2.01% and YoY is +7.92%. Annual FY25 revenue is a separate fact: INR 162,990 crore.

Initial FY25 management guidance from the April 2024 call is compared with the FY25 outcome reported in April 2025:

- Constant-currency revenue growth: original 1–3% guidance versus 4.2% delivered; 1.2 percentage points above the upper bound.
- Operating margin: original 20–22% guidance versus 21.1% delivered; within range.

Both original issuer transcripts are linked. This is **initial guidance only**, not guidance revisions, a rolling four-quarter tracker, an assessment of management quality or a comparison with quarterly INR revenue growth.

## 3. Data actually included

| Source | Local contents | Limitations |
|---|---|---|
| Yahoo Finance chart API | 189 raw OHLCV bars, 63 each for three symbols; 27 July–26 October 2026 | Historical snapshot; acquisition-day bar excluded conservatively |
| NSE announcements API | 20 Infosys filing records selected from the original response; acquired 27 October 2026 | No continuous ingestion or BSE feed; only one filing issuer |
| Infosys issuer results | Manually verified derived financial facts, PDF page reference | No original results PDF bundled or automatically parsed for this corpus |
| Infosys FY24/FY25 calls | Two minimal source paraphrases with page references and dates | No full transcript text index |
| Infosys FY25 annual-report HTML | One CEO-letter source note | Exact HTML publication timestamp unverified; no downloaded annual-report PDF |

Direct Infosys downloads returned HTTP 403 during the build. Three exchange-attachment downloads timed out. Issuer document contents were verified using a web reader and reduced to minimal source notes. Note hashes hash those notes, not original PDF bytes. Public access does not establish redistribution permission; review terms before hosting the samples.

Representative publisher sources:

- https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=INFY
- https://query1.finance.yahoo.com/v8/finance/chart/INFY.NS?range=3mo&interval=1d
- https://www.infosys.com/investors/reports-filings/quarterly-results/2024-2025/q4/documents/q4-and-12m-fy25-financial-results-auditorsreports.pdf
- https://www.infosys.com/investors/reports-filings/quarterly-results/2024-2025/q4/documents/transcripts/earningscall.pdf
- https://www.infosys.com/investors/reports-filings/quarterly-results/2023-2024/q4/documents/transcripts/earningscall.pdf
- https://www.infosys.com/investors/reports-filings/annual-report/annual-reports/ar-2024-25.html

## 4. Architecture and code map

```text
Reviewed JSON snapshot -> FastAPI -> SQLite/raw filing store
                                 -> time filter/grouping/ranking -> Brief
Price bars -> deterministic prior-20-session evaluator -> observations
Research question -> typed regex plan -> curated facts/source notes -> answer cache
Same-origin responsive browser UI -> API and original publisher links
```

- backend/app/main.py: API, POST size/rate limits, startup validation and frontend serving.
- backend/app/models.py: typed input/data contracts, query validation and metrics list.
- backend/app/analytics.py: percentage calculations, dimension helper, anomalies, filing grouping/cutoffs and guidance comparison.
- backend/app/research.py: bounded period/intent/metric parsing, Infosys-specific answers and source-note retrieval/cache.
- backend/app/store.py: JSON loading, SQLite raw_filings/answers/alerts tables and locks.
- frontend/: HTML/CSS/JavaScript UI.
- demo/: versioned watchlist, bars, filings, source notes and acquisition outcomes.
- scripts/import_public.py: bounded raw public acquisition and optional local-PDF extraction. Raw imports are not automatically promoted into served research.
- backend/tests/test_core.py: offline unit/API regressions using an in-memory database and synthetic edge cases.

This supports a small single-process local demo. Rate counters are process-local, not shared production quotas. Hardcoded financial answers do not yet run through a generic evidence-linked FinancialFact repository.

## 5. Tests and evidence — precise status

Latest executed backend command, from project root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider
```

Latest recorded result: **55 passed, 0 failed, 1 existing Starlette/httpx deprecation warning**, 0.50 seconds. JavaScript syntax check `node --check frontend/app.js` passed. These commands were run in the preceding implementation turn; this summary-writing task inspected their report and did not rerun them.

Earlier replay validation confirmed 18 companies, 189 bars, 4 source notes and 20 filings. Earlier interactive browser checks recorded mobile CSS viewport 375×812 and desktop 1200×800 with no page overflow. They exercised replay, filing details, guidance citations, missing ticker coverage and a volume change from 2× (zero observations) to 0.1× (three observations). Existing screenshots are actual browser captures with documented capture-scaling limitations. They predate the latest backend correctness patch; no new browser check was run for that patch.

The latest patch fixed and regression-tested:

1. FY2026 revenue incorrectly returning FY25 figures.
2. Quarterly guidance questions incorrectly receiving annual guidance comparison.
3. Revenue-plus-PBT questions omitting PBT.
4. Missing EBITDA being marked verified and the risk of another issuer's documents unlocking Infosys answers.

The suite also tests cutoffs, exact duplicate evidence, cache invalidation by note hash, distinct record dates, financial dimension helper mismatches, denominator zero, anomaly baselines, input validation, no-model fallback, source IDs, body limits and per-client request limits.

**What those tests do not prove:** the revision/hash test is synthetic, not an actual corrected-filing ingestion lifecycle. The injection test is hostile query text with no model execution, not a hostile PDF passed through a live LLM. No public deployment, Docker build, live inference, generic primary-document ingestion, distributed quota/concurrency, physical-phone lab or broad issuer correctness is verified.

## 6. Biggest remaining risks / incomplete work

1. **No public deployment, GitHub URL or genuine conversation-export link.** The project is not ready for final assessment submission. A localhost URL is not a public reviewer demo.
2. **Curated, one-issuer research.** Many financial values and summaries are explicitly coded for Infosys. The new guard prevents accidental cross-issuer answers but does not implement generic research.
3. **No completed PDF-to-research ingestion pipeline.** The CLI can acquire/extract raw unverified inputs; promotion, indexing and fact validation remain manual/incomplete. PyMuPDF is an optional dependency outside shipped requirements.
4. **Incomplete period and comparability coverage.** New regressions address known forms; regex handling is not universally correct. The generic comparison helper does not validate exact fiscal-quarter adjacency/entity/segment and is not used by the curated financial response path.
5. **Incomplete evidence invalidation.** Cache keys include note hashes and a manually bumped implementation version. Raw filing revisions alone do not automatically invalidate derived answers. Existing raw IDs are seeded with INSERT OR IGNORE; fixture edits do not update persisted rows.
6. **Limited Push breadth.** Exact attachment matching, broad category keywords, no automatic corporate-action flags/session audit, no server scheduler or category-specific notification rules.
7. **UI timing risks.** Async requests lack stale-response cancellation. FY25 filing replay still displays latest-snapshot EOD observations with their actual dates; it is not a complete historical as-of alert replay.
8. **Source permissions unresolved.** Download availability and minimal local source notes do not certify public redistribution rights.
9. **Guidance is narrow.** No later revisions or preceding-four-quarter history; no bank financial example or verified EBITDA series.
10. **No runtime AI.** This limits cost and hallucination risk but leaves the assessment's broader reasoning workflow incomplete.

## 7. Distinction from the old Indian-equities/HDD project

FINN was independently written from newly acquired public inputs. The build did not access the old repository or HDD. The old project may inform engineering ideas—causality, provenance, units, immutable evidence, deterministic tests and honest missing states—only.

Do not copy or depend on the old repository, private historical corpus, quant_data, Seagate/HDD files, 3,410 time series, Phase 3A–3G outputs, strategies, alpha/performance scores, backtests, broker/order logic, cash ledger, secrets, infrastructure, UI assets or previous screenshots. Do not scan/mount/index/hash/upload the old drive. Earlier research findings were not certified live signals and are not evidence for FINN. This assessment is an investor-information product, not a trading system.

## 8. How to run and review locally

Project root on the current machine:

`~/Documents/Codex/2026-10-27/see/outputs/finn`

```sh
cd ~/Documents/Codex/2026-10-27/see/outputs/finn
./start.sh
# With dependencies already installed:
.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Use either startup method, not both on the same port. Open http://127.0.0.1:8000. The server must restart to load changed backend code. Python 3.12+ and initial dependency-download access are required. No runtime API key is needed. Do not delete the existing database or overwrite existing work.

Reviewer journey: Brief -> FY25 replay -> results details -> management guidance -> original sources; then Settings -> adjust volume threshold -> Brief -> Research -> Q4 FY25 revenue and PBT; test FY2026 revenue, quarterly guidance, missing EBITDA and an unfamiliar ticker.

## 9. Repository state and next priorities

Branch: main. Current committed HEAD: d2221e4b88c843ede399bd8db6047cd9bb5b30e3. No remote configured. The latest correctness patch is **uncommitted** in backend/app/models.py, backend/app/research.py and backend/tests/test_core.py, with appended progress in docs/RESUME_HERE.md, docs/TEST_RESULTS.md and docs/WORKLOG.md. CODEX_HANDOFF.md is an untracked comprehensive handoff. This review file is new and also uncommitted. No commit, push, deployment or assessment email was performed for this request.

Next implementation priorities:

1. Typed issuer/period/basis/unit financial facts linked to exact evidence; generic safe answer execution rather than fixed issuer text.
2. A small genuine primary-PDF extraction, verification, promotion and citation pipeline; add issuer coverage only after generic answering is safe.
3. Review original assessment PDFs and source rights; expand Push lifecycle/coverage and regressions.
4. Deploy through an authorized free hosting/repository account and verify the real public no-login mobile workflow.
5. Add bounded runtime reasoning only if justified, complete guidance revisions/coverage, then finish submission artifacts with actual URLs.

## 10. Supporting files to attach if GPT needs evidence

This summary can be pasted alone for an initial review, but source inspection requires attachments. Useful files:

- CODEX_HANDOFF.md — detailed state, decisions, restrictions, risks and continuation.
- backend/app/research.py and backend/tests/test_core.py — actual answering behavior and tests.
- backend/app/analytics.py and models.py — calculations/contracts.
- demo/documents.json, filings.json and bars.json — actual evidence/data records.
- docs/TEST_RESULTS.md — latest 55-test continuation; docs/test-output.txt is the earlier 29-test raw run, not the latest run.
- docs/REPLAY_DATA_PROVENANCE.md and PUBLIC_DATA_ACQUISITION.md.
- docs/evidence/ — earlier browser-check notes and screenshots.
- docs/PRODUCT_DECISIONS.md, ARCHITECTURE.md and LIMITATIONS.md.
- docs/checkpoints/CHECKPOINT_INDEX.md and LATEST_CHECKPOINT.md — milestone records, all PARTIAL; these precede the latest correctness patch.

Please identify where this implementation is a credible narrow prototype versus where it falls short of a source-grounded investment-intelligence agent. In particular: is the curated no-model research adequate for an interim checkpoint, what evidence is missing for the promise tracker, and what three changes would most improve assessment readiness?
