# FINN — Follow the evidence

FINN is an Indian-equities research prototype built to help an investor see what changed, decide what deserves investigation, and inspect the primary evidence. It combines a dated filing brief with deterministic financial comparisons and optional, bounded Gemini interpretation.

**[Open the public application](https://finn-frontend-six.vercel.app)** · [Backend health](https://finn-backend-1.onrender.com/health) · [Research coverage](https://finn-backend-1.onrender.com/api/coverage) · [Frontend source](https://github.com/Vvishesh23/finn-frontend)

No evaluator login or personal API key is required. This is a research demonstration, not a brokerage or a live market terminal. Check the displayed dates and freshness state before using any observation.

## Push: a focused attention feed

The Brief groups imported exchange announcements, applies transparent rule-based review priorities, and links to original NSE evidence. Company, category and date filters help narrow the view. Adjustable price/volume thresholds surface unusual completed-EOD observations; they do not establish investment materiality. Full exchange descriptions stay in the evidence view.

The current code includes an owner-operated persistent refresh command, failure history, duplicate handling and review-held corrections. It does not run a background scheduler on Render. Newer records acquired during local verification are not evidence that the production database has been refreshed. A daily external scheduler is not activated. Historical replay uses an explicitly preserved bundled dataset.

## Pull: questions answered from bounded evidence

Research selects issuer, fiscal period, reporting basis and verified facts before answering. Financial arithmetic is deterministic. Interpretation can use server-side Gemini over selected public passages, with citation/numeric checks, timeouts and persistent inference limits. Missing evidence remains missing; an LLM is not used to invent a forecast or fill gaps.

Try `WIPRO — FY25 consolidated revenue and profit`, `HINDUNILVR — FY25 consolidated revenue`, or a ticker outside the research corpus. Current-year/2027 questions explain missing coverage instead of substituting FY25. The owner supplied a screenshot of one successful live Gemini answer; the full independent live security/accounting checklist is still incomplete.

## Scope and important limits

- 18 mock watchlist labels; bundled EOD coverage for 17. The unresolved TATAMOTORS source/mapping gap is explicit.
- 11 research issuers, 71 selected facts and 16 evidence records. Predominantly FY25/FY24 annual coverage, with selected Infosys/POWERGRID quarterly comparisons.
- Ten issuers use reviewed primary-PDF extractions with hashes/pages; legacy Infosys notes remain labelled as curated evidence. This is not universal ticker or annual-report coverage.
- Bundled feed: 432 filing records and 1,071 EOD bars through October 27/26, 2026. Local CP16 verification separately acquired filings through November 3 and EOD through November 2. Always use the live application's displayed dates for production state.
- No real-time stream, intraday analytics, trading, brokerage integration, forecast model or account synchronization. Financial reading explanations are small educational aids.
- Source access may fail. A recent NSE PDF check timed out during verification. Public availability does not establish redistribution permission; full source PDFs and newly acquired verification datasets are not bundled into this submission package.

## Architecture, decisions and authentic build history

- [Architecture and owner decisions](ARCHITECTURE.md)
- [AI build-history index](docs/ai-build-history/README.md)
- [Selected chronological history](docs/ai-build-history/SELECTED_HISTORY.md) — curated, with actual message excerpts and explicit summaries.
- [Available Work message record](docs/ai-build-history/FULL_WORK_TRANSCRIPT.md) — **not a complete native export**; omissions and the required original export are stated at the top.
- [Submission email draft](docs/submission/COVER_EMAIL.md) — prepared for owner review, not sent.

ChatGPT supported planning and architecture review, as reported by the owner. The coding-agent conversation records implementation, tests, debugging and deployment assistance. These roles are not a claim that every planning chat has been exported.

## Run locally without any model credential

Python 3.12 is the tested interpreter. From the repository root:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.lock
AI_ENABLED=false REASONING_PROVIDER=disabled FINN_DB=/tmp/finn-local.sqlite3 .venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. SQLite is a development default; `/tmp` is deliberately temporary and must not be presented as persistent production quota storage. This local no-key setup supports deterministic facts and retrieval. The app does not automatically load `.env` files.

The Dockerfile uses the same runtime dependencies and serves FastAPI on `$PORT` (default 8000). Render hosts the backend, Neon PostgreSQL persists imports/caches/inference budgets, and Vercel proxies `/api/*` and `/health` to the backend. Production secrets are entered privately by the owner. The current PostgreSQL adapter requires a direct Neon connection, pooling OFF; its startup timeout options are not compatible with the pooler previously attempted.

For an owner-run refresh, `python -m backend.app.refresh --symbol LT` is a dry run; `--apply` writes to the explicitly configured store. Never run production ingestion with credentials exposed to a coding agent or pasted into chat. No public import endpoint exists. Back up the database before production imports. A code rollback does not remove imported records.

## Verification and reproducibility boundary

Latest CP16 local verification: **200 backend tests, 17 disposable PostgreSQL integration tests, 12 frontend tests passed**, with one existing Starlette/httpx deprecation warning. Tests cover period/basis correctness, citations, missing evidence, quota concurrency/restarts, cache isolation, refresh duplicates/revisions/failures and UI races. Mock/synthetic tests are separate from real public-source acquisition and owner-provided live Gemini evidence.

The test suites and checkpoint artifacts are preserved in the owner's development checkout; they are not included in this minimal deployment repository. Therefore the published runtime checkout alone does not reproduce the full test counts above. The application startup/dependencies are reproducible from this repository. No claim of new tests being run as part of this documentation-only pass is made.

Backend application commit `cdc302a` and frontend commit `12e0609` were pushed on November 3. Public health on November 3 confirmed backend release `cdc302aafca78d3c4958b652696b111f47582ca2`, PostgreSQL healthy, and 11 issuers / 71 research facts through both the Render and Vercel origins. Production still reports STALE, with October 27 filings / October 26 EOD and no recorded refresh. A deployment does not perform the private database refresh automatically. The submission-readiness report records verification separately.
