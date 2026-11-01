# FINN CHECKPOINT CP01 — Running local source-to-screen slice — 27 October 2026 IST
Status: PARTIAL. Exit gate: PARTIAL.
Workspace: ~/Documents/Codex/2026-10-27/see/outputs/finn
Git: see docs/GIT_STATE.txt for implementation commit (documentation-only commits may follow). No remote URL.
Deployment preview: NOT DEPLOYED. Local only: http://127.0.0.1:8000.
Build mode: AUTHENTIC_HISTORICAL_REPLAY.

A. Implemented: FastAPI health, 18-company watchlist and same-origin responsive frontend. Three genuine EOD series, an NSE filing timestamp and four source notes are visible.

B. Demo: open local app -> FY25 replay -> results evidence -> Investigate guidance -> original sources. Then Settings -> 0.1× volume -> save -> Brief, three observations; restore 2× for zero. Research INFY and unfamiliar ZENSARTECH.

C. Real data: 189 Yahoo bars for INFY/RELIANCE/HDFCBANK; 20 NSE Infosys records, latest observed 27-Oct-2026 16:38:30 IST. Four primary-source-derived notes. IDs: infy-results-fy25, infy-call-fy24, infy-call-fy25. Exact URLs and dates: docs/REPLAY_DATA_PROVENANCE.md. Direct issuer 403; exchange PDF attempts timed out. No control bypass.

D. Actual tests: `python -m pytest backend/tests -q` -> 29 passed, 0 failed, 1 dependency warning; `node --check frontend/app.js` passed. Replay verification validates 18/189/4/20 rows. Evidence: docs/test-output.txt, docs/TEST_RESULTS.md.

E. Actual mobile screenshot: docs/evidence/mobile-research.jpg and mobile-settings.jpg. Observed 375×812 CSS viewport. Desktop screenshot is docs/evidence/desktop-brief.jpg if present. No concept images.

F. Finance: consolidated Ind-AS, INR crore, discrete quarter comparisons; source dates separate from publication dates, zero denominator yields no percentage, missing EBITDA stays missing. Guidance uses annual CC growth, never quarterly INR growth. No claimed management-quality score.

G. AI/security/cost: zero runtime model calls, no model/key configured. Source text is data, no tools dispatched from it. Process-local request limits tested, not a distributed quota system. Source-note/query/version cache tested. Development subscription usage not measured.

H. Risks: HIGH: public hosting/GitHub/rights clearance incomplete. MEDIUM: Annual-report/transcript PDFs not parsed automatically; manually verified source notes are used. Stack differs from Next.js.

I. Deferred: automatic full primary-PDF ingestion, broad issuer coverage, runtime model reasoning, four-quarter guidance/revisions, live polling, notifications, multi-instance quotas.

J. Next milestone: Finish source adapters and validate the Push controls. Three smallest tasks: verify source rights; add one verified issuer-document import; deploy on a user-authorized free environment and capture real public evidence.

K. Review: Can every visible number be traced to a genuine source? Is snapshot freshness clear? Are any controls or source links misleading? Is the narrow scope adequate for the original challenge once its PDFs are supplied?

## Verification commands
| Command from project root | Actual result |
|---|---|
| python -m pytest backend/tests -q | 29 passed |
| python scripts/verify_replay.py | 18 companies / 189 bars / 4 notes / 20 filings |
| node --check frontend/app.js | Passed |

Exit gate is PARTIAL because the full milestone requirements exceed this local implementation. No public release, automatic source coverage or real inference is implied.
