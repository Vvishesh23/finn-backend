# CP09 — Eleven issuer research coverage and robustness

28 October 2026. User target: 10–15 document-grounded research issuers. Delivered: 11 issuers with verified financial facts, preserving the existing repository and plain frontend. This is historical, selected-metric coverage, not comprehensive issuer research or ENAM submission readiness.

## Requirements and earlier checkpoints

Both original assessment PDFs were previously read; see [authoritative requirements](../AUTHORITATIVE_ASSESSMENT.md). The PDFs call for 15–20 mock holdings and roughly 3–5 ad-hoc research cases. The existing portfolio has 18 labels; 17 have authentic EOD series. This phase expands Pull research beyond the prior three issuers, including WIPRO outside the watchlist. Read [CP08](CP08_PORTFOLIO_PUSH_AND_HANDOFF.md), CP06_GENERIC_EVIDENCE.md, CP07_BOUNDED_REASONING.md, ../../CODEX_HANDOFF.md, and the original master prompt/review guide in the supplied Assessment folder. Their instructions do not authorize commits, spending or restricted-content publication. No prior Indian-equities/HDD project was accessed or copied.

## Actual corpus coverage

| Issuer | Verified periods | Imported metrics | Basis | Evidence |
|---|---|---|---|---|
| ASIANPAINT | FY25 annual, FY24 annual | ebitda, pat, pbt | standalone | pdf_extracted_reviewed |
| BAJFINANCE | FY25 annual, FY24 annual | pat, pbt, revenue | consolidated | pdf_extracted_reviewed |
| DRREDDY | FY25 annual, FY24 annual | pat, pbt, revenue | consolidated | pdf_extracted_reviewed |
| HINDUNILVR | FY25 annual, FY24 annual | pat, pbt, revenue | consolidated | pdf_extracted_reviewed |
| ICICIBANK | FY25 annual, FY24 annual | pat | consolidated | pdf_extracted_reviewed |
| INFY | Q4 FY25, Q3 FY25, FY25 annual, Q4 FY24 | free_cash_flow, operating_margin, pat, pbt, revenue, revenue_growth_cc | company_reported, consolidated | legacy_curated_note |
| LT | FY25 annual, FY24 annual | pat, pbt, revenue | consolidated | pdf_extracted_reviewed |
| NTPC | FY25 annual, FY24 annual | pat, revenue | consolidated | pdf_extracted_reviewed |
| POWERGRID | Q4 FY25, Q3 FY25, FY25 annual, Q4 FY24, FY24 annual | pat, revenue | consolidated | pdf_extracted_reviewed |
| RELIANCE | FY25 annual, FY24 annual | pat, revenue | consolidated | pdf_extracted_reviewed |
| WIPRO | FY25 annual, FY24 annual | pat, pbt, revenue | consolidated | pdf_extracted_reviewed |

Totals: 16 evidence records, 71 facts, two guidance records. Eight newly downloaded and visually reviewed original PDFs produced 44 new facts; all re-extracted exactly against pinned hashes and reviewed manifests (../evidence/cp09/pdf-reproduction.json). INFY remains legacy curated primary-source notes; the other ten issuers use genuine reviewed PDF extraction. Original PDFs and rendered statement images stay outside the repository; minimal derived amounts, hashes, source URLs and page references are included. No redistribution rights are asserted.

New annual documents cover FY25 and FY24. POWERGRID additionally covers Q4/Q3 FY25 and Q4 FY24 revenue and total PAT. Unknown exact publication times remain unknown: all eight new documents are excluded from explicit historical publication cutoffs. Report approval dates are not publication timestamps. ICICI is banking Indian GAAP, not Ind-AS. Its imported metric is total profit before minority interest, not owner-attributable profit. Bank revenue/PBT/EBITDA have not been forced into industrial metrics. Utility PBT before regulatory deferral movements is not substituted for conventional PBT. Reliance gross sales including GST are not used as net revenue.

## Changed functionality and files

- backend/app/models.py and evidence.py: support original thousands as a unit, derive a generic coverage inventory from verified evidence/facts, expose metrics/bases/periods/methods and unknown publication dates.
- backend/app/research.py: Decimal unit conversion into consistent display units (INR crore), reject mixed currencies/accounting standards in one income statement, retain exact fiscal and comparison dimensions, expose issuer-specific metric definitions in answers/tables. Unrelated USD free cash flow no longer contaminates INR income-statement validation.
- backend/app/main.py: GET /api/coverage; browser/API responses require cache revalidation. Existing rate/body/model controls preserved.
- frontend/app.js and index.html: dynamic coverage count and issuer selectors, actual period/basis disclosure, correct table units/definitions, mobile table scroll hint, delayed response guards for navigation/filters/research/company selection, versioned assets to prevent stale frontend after an update. No framework rewrite.
- scripts/ingest_reviewed_pdf.py: preserve manifest document kind for actual financial results versus annual reports. scripts/verify_coverage.py: offline acceptance over each financial issuer; no provider inference.
- demo/manifests/*-FY25-consolidated.json: eight pinned-source reviewed extraction manifests. demo/evidence.json and facts.json: append 8 evidence records and 44 facts; existing IDs/work preserved.
- backend/tests/test_expanded_coverage.py and frontend/tests/navigation.test.cjs: real corpus regression checks and clearly labelled synthetic currency/scale/race cases.

## Actual questions and answers

**WIPRO: FY2025 pat**

WIPRO · FY25 annual · Consolidated Ind-AS; INR crore; annual periods. PAT (total profit): INR 13,218.00 crore. Definition: Total profit including non-controlling interests. YoY +18.95%.

Source: [Wipro Limited — PDF page 272](https://www.wipro.com/content/dam/nexus/en/investor/annual-reports/2024-2025/Integrated-annual-report-2024-25.pdf). Evidence method: pdf_extracted_reviewed. Zero model calls.

**ICICIBANK: FY2025 pat**

ICICIBANK · FY25 annual · Consolidated Indian GAAP (banking); INR crore; annual periods. PAT (total profit): INR 54,569.38 crore. Definition: Total net profit before deducting minority interest, including associates; banking Indian GAAP. YoY +18.42%.

Source: [ICICI Bank Limited — PDF page 130](https://www.icici.bank.in/content/dam/icicibank/managed-assets/docs/investor/annual-reports/2025/icici-bank-2025-financial-statements.pdf). Evidence method: pdf_extracted_reviewed. Zero model calls.

**NTPC: FY2025 pat**

NTPC · FY25 annual · Consolidated Ind-AS; INR crore; annual periods. PAT (total profit): INR 23,953.15 crore. Definition: Total profit including net regulatory deferral account movements and non-controlling interests. YoY +12.29%.

Source: [NTPC Limited — PDF page 264](https://www.ntpc.co.in/sites/default/files/annual-report/complete-reports/Annual%20Report%202024-25_1.pdf). Evidence method: pdf_extracted_reviewed. Zero model calls.

**New ticker test:** WIPRO is outside the mock portfolio; its generic FY2025 PAT question returned INR13,218 crore total profit and +18.95% YoY, linked to PDF page 272 / printed page 286. It has no issuer-specific answer code. The complete eleven-issuer answers/citations are saved in ../evidence/cp09/research-acceptance.json. Missing unknown tickers and missing periods remain explicit; general syntax does not certify listing status.

## Commands executed and actual outputs

| Command | Result / raw evidence |
|---|---|
| `.venv/bin/python -m pytest -q` | 128 passed, 1 existing Starlette/httpx deprecation warning; ../evidence/cp09/backend-tests.txt |
| `node --test frontend/tests/navigation.test.cjs` | 4 passed, 0 failed; ../evidence/cp09/frontend-tests.txt |
| `node --check frontend/app.js` | Exit 0 |
| `.venv/bin/python scripts/verify_replay.py` | 18 companies; 1,071 bars; 432 filings; 16 evidence; 71 facts; 2 guidance; ../evidence/cp09/replay.txt |
| `.venv/bin/python scripts/verify_coverage.py --min-issuers 10 --output docs/evidence/cp09/research-acceptance.json` | 11 financial issuers, 71 facts, 11 tested issuer answers, 0 model calls |
| `git diff --check` | Exit 0 |

Acquisition commands run from the workspace: `work/venv/bin/python work/coverage-expansion/fetch.py`, `fetch-more.py`, and `fetch-utilities.py`. They call curl with certificate checks, HTTP/1.1, bounded time and 40 MB size caps. Initial NSE urllib requests failed certificate trust; system curl attempts had transport errors/timeouts. TCS returned 403, HCLTech timed out, initial NTPC download timed out; no controls were bypassed. Official issuer-hosted fallbacks succeeded for eight issuers. Each actual attempt is retained in ../evidence/cp09/*downloads*.json.

Manifest preparation was run with `work/venv/bin/python work/coverage-expansion/build_manifests.py`; an executed Python loop called extract_bundle(original_pdf, manifest) and promote(bundle, demo) for each source. A second executed loop re-extracted all eight originals and asserted equality with the imported bundles, producing pdf-reproduction.json. Full source pages were rendered with PyMuPDF and visually inspected before promotion. Extraction remains operator-reviewed; no autonomous table-understanding claim.

An intermediate test run had seven failures because the new mixed-currency check included an unrelated USD free-cash-flow fact with the INR income statement. Income-statement validation was corrected to inspect only relevant metrics; the final complete test run passes. Browser testing also exposed cached old JavaScript; versioned assets plus revalidation address this.

## Current browser evidence

In-app browser: actual WIPRO FY25 revenue/PBT/PAT question at 375×812 showed normalized INR crore amounts, source page and missing EBITDA. Document scrollWidth 375 equals viewport width 375; wide comparison table scrolls internally. Actual ICICI FY25 PAT question showed INR54,569.38 crore and explicitly unknown publication time. At 1200×800, the research screen displayed all eleven coverage selectors. Screenshots: ../evidence/cp09/mobile-wipro.jpg, mobile-icici.jpg, desktop-coverage.jpg. This is responsive viewport testing, not physical-phone or cross-browser certification. Four delayed-response tests use synthetic deferred network responses and the real frontend code; they are not live outage simulations.

## API usage, cost and integrity

Actual Gemini calls remain zero; deterministic research needs no key. Existing opt-in limits: 20 calls/day, 50,000 reserved tokens/day, 800 output tokens, 12,000 evidence characters, two concurrent requests; successful-answer cache uses corpus/model/prompt versions. This change advances the research cache version for normalized units. No live Gemini quality/cost certification; no paid actions. AI remains disabled with placeholder credentials. Keep AI disabled on ephemeral hosting until durable budget storage is configured. Minimal publisher facts are linked, not full source PDFs redistributed.

## Branch, remaining blockers and next steps

Branch main; all changes uncommitted. No commit/push, account creation or credential storage. Exact current file status is saved to ../evidence/cp09/git-status.txt.

1. Deploy to the user-configured host and run the public HTTPS smoke test. Public no-login URL remains mandatory and incomplete; hosting credentials were deferred.
2. Add genuine transcript/business passages and recent quarterly results across more of these issuers; eleven issuers with selected FY25 facts is not eleven comprehensive research dossiers. More than two ad-hoc covered names beyond the watchlist remain desirable.
3. Expand the real rolling four-quarter management promise history. Current two guidance records concern one original Infosys annual guidance case; no broader promise tracker is claimed.
4. Validate bounded live Gemini with a server secret and inspect citation entailment/answer usefulness/provider usage; existing provider tests remain mocked.
5. Resolve TATAMOTORS provider/listing identity with authoritative evidence; do not invent replacement prices. Improve filing classification beyond keywords and automate permitted refreshes.
6. Verify public cold starts, mobile/cross-browser behavior, persistent budget storage and final repository/history/submission artifacts.

CP09 coverage/robustness milestone is implemented and tested; release remains PARTIAL. Exact next implementation step: add primary transcript and quarterly evidence while the external deployment configuration remains pending.

Final running-server check: an executed `.venv/bin/python` httpx client requested `http://127.0.0.1:8000/api/coverage` and `/api/usage`; HTTP200, 11 financial issuers, Cache-Control no-cache, model disabled. Raw result: ../evidence/cp09/live-local-smoke.json. This verifies local HTTP only, not public deployment.
