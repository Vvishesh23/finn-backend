# FINN CP06 — generic typed evidence / genuine PDF vertical slice

27 October 2026 IST. Status: PARTIAL against full ENAM submission; phase exit gate: PASSED for a narrow typed multi-issuer facts/PDF path. Not a claim of complete generic document extraction or interpretive research.
Branch main, committed HEAD d2221e4b88c843ede399bd8db6047cd9bb5b30e3. All new work uncommitted; previous edits preserved. Local QA http://127.0.0.1:8001; NOT DEPLOYED.

## Authoritative requirements now read
Both original PDFs in ~/Desktop/Assessment were read completely: Main (4 pages), Reference (3 pages). Rendered relevant pages inspected. The brief confirms 27 October release / 1 November 2026 deadline, 15–20 portfolio companies, generic NSE-ticker research when data exists, EOD+filings+primary reports/transcripts, mobile experience and deployed demo/GitHub/AI history/cover note. Research views are a menu, not a checklist; category list is optional guidance. User requests no-login public access. Original PDFs remain user-owned inputs outside this repository; no copies redistributed. No HDD or previous project accessed.

## Implemented and changed files
- backend/app/models.py: SourceEvidence, FinancialFact, GuidanceRecord, explicit source dates, file hashes, page/offset provenance and typed period/basis dimensions; timezone-aware research as_of.
- backend/app/evidence.py (new): generic evidence/fact repository, issuer/evidence validation, evidence visibility at cutoff, source conversion, dimension and exact-period comparisons.
- backend/app/research.py: removed issuer-specific answer branches and numerical constants; generic fact selection, annual/quarter period routing, per-metric missing state, generic guidance records and source-note retrieval. Full evidence/facts/guidance version plus raw filings enter cache key.
- backend/app/main.py: evidence source API and company document path use the new repository; company financial period labels handle annual-only sources.
- frontend/app.js: preserved HTML/CSS design; dynamic table period labels, accurate multi-issuer coverage copy.
- demo/evidence.json, facts.json, guidance.json: migrated legacy curated Infosys records, added newly extracted PDF-reviewed HUL/Asian Paints records. Original documents.json preserved.
- scripts/ingest_reviewed_pdf.py and promote_evidence.py: bounded local PDF extraction with pinned source hash, page identity, unique regex capture, manually reviewed expected values and dimensions; append-only-ID bundle promotion. This is manifest-guided extraction, NOT autonomous general table understanding.
- demo/manifests/*: reproducible source/file/page/value checks. backend/requirements-pdf.txt: optional extraction dependency.
- backend/tests/test_evidence.py: new contracts, multi-issuer/API/period/basis/source/cutoff/cache regressions. Existing tests updated only for intentional generic prior-quarter availability and response wording.

## Real coverage and provenance
Repository now contains 6 evidence entries, 27 financial facts and 2 initial guidance records.
- INFY: curated source-linked legacy figures, Q4 FY25/Q3 FY25/Q4 FY24 and FY25 annual; initial FY25 guidance and company-reported annual metrics. These were NOT newly extracted PDFs.
- HINDUNILVR: genuine downloaded FY25 annual-report PDF, consolidated annual revenue/PBT/total profit for FY25 and FY24. PDF page 186 / printed 368–369. Revenue FY25 63,121; FY24 61,896 crore. Approval/report date 24 April 2025; actual publication timestamp unknown, so historical as_of requests exclude it.
- ASIANPAINT: genuine downloaded standalone financial-statements PDF, FY25 and FY24 annual PBT/PAT/issuer-defined EBITDA. PDF page 12 / printed 351. EBITDA includes other income under its disclosed I–II definition; no silently invented total revenue or consolidated data. Approval date 8 May 2025; publication unknown.
- Public PDF bytes and page renders stay in workspace work/phase1-sources (outside repo). Only minimal derived records, original hashes, citations and extraction manifests ship. Redistribution rights not certified.
- TCS PDFs returned 403; ITC returned 406; no bypass. Acquisition outcomes retained in work/phase1-sources/acquisition*.json. EOD remains 3 companies and filing coverage remains Infosys at this checkpoint; expansion is next phase.

Source URLs:
HUL: https://www.hul.co.in/files/annual-report-2024-25.pdf
Asian Paints: https://www.asianpaints.com/content/dam/asianpaints/website/secondary-navigation/investors/annual-reports/2024-2025/Standalone-Financial_Statements.pdf
Infosys: original results URL preserved in demo/evidence.json and docs/REPLAY_DATA_PROVENANCE.md.

## Actual commands/results
From project root unless noted:
1. ../../work/venv/bin/python scripts/ingest_reviewed_pdf.py --pdf ../../work/phase1-sources/hul_ar25.pdf --manifest demo/manifests/HINDUNILVR-FY25.json --output ../../work/phase1-sources/hul-bundle.json -> 1 evidence / 6 facts.
2. Same extraction for asian_standalone25.pdf and ASIANPAINT-FY25.json -> 1 evidence / 6 facts. Original pages rendered and visually checked.
3. FINN_DB=:memory: .venv/bin/python scripts/promote_evidence.py <each bundle> -> final 6 evidence / 27 facts / 2 guidance. Immutable-ID conflicts reject replacement.
4. PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider -> 69 passed, 0 failed, 1 existing Starlette/httpx warning, 0.61 s. Raw: docs/evidence/phase1/tests.txt.
5. node --check frontend/app.js -> exit 0.
6. Actual API/answer examples saved: docs/evidence/phase1/questions.json.

The earlier intermediate integration run had 4 failures/51 passes: changed metric ordering, newly accessible real prior-year fact and two wording assertions. Those were reconciled without weakening missing/basis/period checks; final suite above passes. Synthetic tests are labeled synthetic and do not count as genuine issuer coverage.

## Three research answers and citations
1. INFY — “Q4 FY25 revenue and PBT”: Revenue INR 40,925 crore; QoQ -2.01%, YoY +7.92%. PBT INR 9,663 crore; QoQ -0.07%, YoY -5.63%. Citation infy-results-fy25, legacy curated note with original PDF page 12 reference.
2. HINDUNILVR — “FY25 consolidated revenue”: INR 63,121 crore; YoY +1.98%. Citation hul-ar25-consolidated-p186, original HUL PDF page 186, reviewed extraction/file hash.
3. ASIANPAINT — “FY25 standalone PBT and PAT”: PBT INR 4,897.18 crore, YoY -30.03%; PAT INR 3,584.88 crore, YoY -32.55%. Citation asian-ar25-standalone-p12, issuer PDF page 12, reviewed extraction/file hash.

New-ticker test: ASIANPAINT is NOT in the 18-company mock watchlist and has no issuer branch in research code. Same generic engine returns its genuine PDF facts; consolidated-PAT request correctly returns MISSING. ZENSARTECH remains explicit missing-source. HUL Q4 request cannot substitute annual figures.

## Current browser evidence
Actual local QA browser at observed 375×812 CSS pixels. HUL answer/citation and non-portfolio Asian Paints answer/citation verified through the existing UI. Asian Paints document scrollWidth 375, viewport width 375: no page horizontal overflow. Financial table scrolls inside its container.
Screenshots: docs/evidence/phase1/mobile-hul.jpg and mobile-asianpaints.jpg. Screenshots reflect application capture scaling, not a physical phone lab. Existing server left alone; isolated QA server uses in-memory DB on port 8001.

## API use/cost controls
Phase makes zero runtime model calls, no API keys or paid inference. Deterministic facts do not need a model. Existing body/rate protections retained, source documents never execute tools. Historical source visibility requires proven publication timestamp. User asked for credential placeholders and will configure Gemini/hosting later. No credentials created/stored/pushed. No provider response or inference quality claimed.

## Blockers and next actions
HIGH: no public deployment/hosting credentials; no live Gemini key; source redistribution review; only 3 research issuers and 2 new annual PDF cases. Publication times unknown for new PDFs and broad concall ingestion incomplete. The local manifest-guided extractor still needs reviewed mappings for new document layouts.
Next phase: bounded Gemini reasoning adapter with backend-only placeholder config, explicit evidence/citation checks, persistent atomic budgets, concurrency and mocked timeout/quota/key tests. Then obtain broader EOD/filing snapshots for portfolio sectors. Deployment remains prepared but blocked until an authorized hosting target is configured; no fake public URL. Preserve frontend and old-work/HDD exclusion.

Independent review questions: Are annual/quarter and standalone/consolidated distinctions sufficiently visible? Does this genuinely generalize issuer facts without claiming autonomous PDF interpretation? What minimum passage breadth is needed before interpretive Gemini answers become useful?
