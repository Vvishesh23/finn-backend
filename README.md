## Start here: Desktop copy and frontend-first hosting

See [GitHub and Render steps](GITHUB_RENDER_STEPS.md) and [Desktop/frontend handoff](docs/DESKTOP_FRONTEND_HANDOFF.md). Latest checks: 165 backend and nine frontend tests pass. Gemini is preserved; the separate frontend-only preview has no backend connection yet. No public deployment or live Gemini result is claimed. Earlier CP11 entries below are historical.

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

# FINN — current implementation status (27 October 2026)

**Working local prototype; public submission still incomplete.** The original ENAM PDFs have now been read; see [authoritative requirements](docs/AUTHORITATIVE_ASSESSMENT.md). Earlier missing-PDF statements below are historical.

- Existing plain HTML/CSS/JS frontend preserved; FastAPI and SQLite backend.
- 18-label mock watchlist; **17 companies with 1,071 genuine EOD bars and 432 NSE filing records**. TATAMOTORS has an explicit acquisition/identity gap. No live scheduler.
- Generic typed `SourceEvidence` / `FinancialFact` / guidance repository: **8 evidence records, 27 facts, 2 initial guidance records** across Infosys, HUL and Asian Paints. New HUL/Asian Paints annual FY25/FY24 figures and company descriptions came from genuinely downloaded, locally parsed and visually reviewed primary PDFs; Infosys records remain labeled legacy curated evidence.
- Bounded optional Gemini reasoning adapter with server-only placeholder configuration, citation/numeric validation, SQLite daily budgets and duplicate suppression. **Real Gemini calls: zero; provider tests are mocks.** Direct financial queries stay deterministic.
- Filing-type preferences and EOD thresholds work; dates, reporting basis, periods, missing facts and snapshot status remain visible.
- Latest actual test results and phase reports: [CP06](docs/checkpoints/CP06_GENERIC_EVIDENCE.md), [CP07](docs/checkpoints/CP07_BOUNDED_REASONING.md), [latest checkpoint](docs/checkpoints/LATEST_CHECKPOINT.md). Older counts below refer to the original build, not current coverage.

## Run current code

```sh
./start.sh
# Or after dependencies are installed:
.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
.venv/bin/python -m pytest backend/tests -q
.venv/bin/python scripts/verify_replay.py
```

Open http://127.0.0.1:8000. An isolated QA preview may run on port 8001. Restart a server to load changed backend code; do not stop unrelated servers or delete databases. No login or key is needed for local deterministic/retrieval mode.

Try Research with HINDUNILVR: `FY25 consolidated revenue`; ASIANPAINT: `FY25 standalone PBT and PAT`; INFY: `Q4 FY25 revenue and PBT`. Asian Paints is not in the watchlist. Annual source facts cannot answer a quarterly request. Unknown issuers remain honest missing-source states. With no Gemini key, business/interpretive questions show reviewed source notes without a fabricated analysis.

## Data preparation / runtime reasoning / deployment

- `scripts/ingest_reviewed_pdf.py --pdf ... --manifest ... --output ...` verifies pinned original hashes, source page/basis identity, unique extraction patterns and expected reviewed amounts. `scripts/promote_evidence.py <bundle>` appends validated IDs and rejects conflicting changes. See `demo/manifests/`. This is reviewed manifest-guided extraction, not autonomous table interpretation.
- Optional local PDF extraction dependency: `pip install -r backend/requirements-pdf.txt`. Original PDF bytes stay outside the repo. Minimal derived records and citations are included; redistribution rights are not certified.
- `scripts/refresh_portfolio.py --apply --report <new-report.json>` acquires bounded public snapshots without overwriting conflicting existing identities. Use deliberately, respecting provider controls; no background crawling.
- [Runtime reasoning configuration](docs/RUNTIME_REASONING.md) explains opt-in model settings and measured-versus-mocked claims. `.env.example` is not automatically loaded.
- `render.yaml` preserves the single-service backend/frontend. User deferred hosting credentials: **no public URL exists**. Keep AI disabled on ephemeral free hosting; configure durable budgets before enabling paid inference. [Deployment steps](docs/DEPLOYMENT_STEPS.md) and `scripts/smoke_url.py --url <actual HTTPS origin>` prepare verification. Docker daemon unavailable here; no Docker build claim.

No old HDD/repository, private market corpus, strategies, secrets or UI assets were accessed or copied. No new commit/push or assessment email was performed. Source rights, live Gemini quality, wider transcript evidence, automatic fresh ingestion and public deployment remain limitations.

---

## Original local-build README (historical details below)

# FINN — Follow the evidence

A mobile-first Indian-equities intelligence prototype: a windowed filing brief, configurable EOD observations, primary-source research and an initial-guidance tracker.

## Run locally

Python 3.12+ is required. From this folder:

```sh
./start.sh
```

Open http://127.0.0.1:8000. No account or model key is required. First start downloads the pinned free Python dependencies. Subsequent starts can use `.venv/bin/python -m uvicorn backend.app.main:app --port 8000` directly.

On Windows: create a virtual environment, install `backend/requirements.txt`, then run `python -m uvicorn backend.app.main:app --port 8000`.

## Try the 2-minute workflow

1. The Brief opens on the actual trailing 24-hour clock, applied to the **imported snapshot**. No current data is invented when that window empties.
2. Select **FY25 replay**, then **Review evidence** on the April 17 results disclosure. Inspect consolidated quarterly comparisons and its exchange attachment.
3. Choose **Investigate management guidance**. Compare initial FY25 guidance with the reported FY25 outcome. Both dated earnings-call sources are linked. Later revisions are explicitly outside this example.
4. In **Settings**, lower unusual volume to 0.1×, save, then return to The Brief. Three sourced snapshot observations now cross the threshold. Restore 2× to see none.
5. Open **Research** and ask `Q4 FY25 revenue`, `FY25 annual revenue`, `Business overview`, or `Did management deliver on FY25 guidance?`. Inspect the plan and citations. Try `ZENSARTECH` for a truthful missing-source outcome.

## What is actually included

- 18-company **mock** watchlist; it is not a certified listing/security master or a personal portfolio.
- 189 real Yahoo Finance EOD bars across INFY, RELIANCE and HDFCBANK: 27 July–26 October 2026. Acquisition-day bars were conservatively excluded because finality was not independently established.
- 20 minimal public NSE Infosys announcement records, with exchange publication timestamps and original attachment links. Acquired 27 October 2026. No continuous polling.
- Four manually verified, source-linked Infosys research notes: FY25 results, FY24/FY25 calls and FY25 annual-report HTML. No original PDFs bundled and no claim of automated PDF ingestion for this corpus.
- Deterministic financial calculations, SQLite append-preserving raw filings, exact-attachment grouping, persistent answer cache and deduplicated observed alerts.
- Request validation, bounded input, same-origin frontend, security headers and process-local query rate limits. No runtime model calls or paid inference.

## Tests

From the project root after setup:

```sh
.venv/bin/python -m pytest backend/tests -q
.venv/bin/python scripts/verify_replay.py
node --check frontend/app.js
```

Recorded result: **29 passed**, one dependency deprecation warning. See `docs/TEST_RESULTS.md` and raw output. Real 375-CSS-pixel mobile and desktop browser evidence is under `docs/evidence/`.

## Public-source acquisition tools

```sh
.venv/bin/python scripts/import_public.py prices --symbol INFY
.venv/bin/python scripts/import_public.py nse --symbol INFY
```

These bounded CLI adapters save raw imports in `demo/imports/`; they do **not** silently promote unreviewed data into the app. For legally obtained issuer PDFs, install optional PyMuPDF (`pip install pymupdf`) then use `document --symbol INFY --file report.pdf --url https://publisher.example/report.pdf --title 'Issuer report' --published YYYY-MM-DD`. Extraction is unverified until manually reviewed; documents are untrusted data.

## Architecture and limits

FastAPI serves a same-origin HTML/CSS/JavaScript frontend and SQLite data. A lightweight frontend was chosen instead of Next.js to avoid build dependencies while delivering an inspectable local vertical slice. There is no remote model, scheduler, email sender, authentication, broker integration or arbitrary URL fetch API. No HDD or previous project was accessed or used.

This is **not submission-ready**: public hosting, GitHub URL, source redistribution clearance, broader issuer coverage, automated primary-PDF ingestion, runtime reasoning, four-quarter guidance history and multi-instance quotas remain open. The Dockerfile is supplied but its cloud deployment is not verified. Public-source availability does not establish redistribution permission; keep this acquired sample local until terms are reviewed. See `docs/LIMITATIONS.md` and `docs/DEPLOYMENT_STEPS.md`.
