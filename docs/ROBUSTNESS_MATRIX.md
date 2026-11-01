## CP10 update — 31 October 2026

[Current checkpoint](checkpoints/CP10_SECURE_GEMINI.md): 157 backend + four frontend tests passed, preserving 11 issuers/71 facts. [Private owner-only setup guide](SECURE_GEMINI_SETUP.md) contains the real trust boundary, privacy terms, configuration, quotas, rollback and live-test checklist. Use `python3 scripts/run_isolated_tests.py -q`; direct pytest is intentionally disabled. Actual tests use a literal clean environment, temporary SQLite and no network. Live Gemini remains NOT TESTED; public deployment remains incomplete. Do not read or configure real secrets in Codex. Historical entries below may describe the superseded direct-HTTP adapter, unscoped cache or process-local concurrency.

# FINN robustness status — CP09, 28 October 2026

These are independently implemented FINN controls, inspired by principles only. No old Indian-equities/HDD code, data, credentials, strategies or assets were accessed or copied. The original assessment PDFs are authoritative; the supplied master prompt/review guide inform acceptance checks. See checkpoints/CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md for actual coverage, commands, evidence and unresolved work.

| Principle | Current implementation and proof | Limit |
|---|---|---|
| Primary evidence and provenance | 10 issuers with reviewed PDF extraction plus legacy curated INFY notes; pinned hashes, pages, original units and minimal derived facts; 8 new PDFs reproduced exactly | Extraction uses manually reviewed manifests; no automatic issuer/document discovery |
| Point-in-time causality | Explicit publication cutoff filters; unknown publication timestamps excluded; new eight-issuer cutoff tests | Publication dates remain unknown for the new PDFs; no fabricated dates |
| Financial comparability | Exact fiscal intervals, basis, currency, standard, definition; Decimal scale conversion; real quarters kept separate from annual/YTD; mixed currency rejected | March-year-end fiscal calendar only; metric coverage partial |
| Sector-aware missing evidence | ICICI banking GAAP and total-PAT definition explicit; no invented bank EBITDA/revenue/PBT; utility regulatory PBT not silently substituted | No broad banking metric model yet |
| Honest portfolio coverage | 18 mock labels, real EOD for 17, 432 filings; configurable rules and prior-session volume denominator | Manual October 2026 snapshot, no live scheduler; TATAMOTORS gap |
| Generic ticker behavior | WIPRO outside watchlist researched through generic repository; valid unknown ticker returns MISSING | Not a certified listings master; only 11 issuers have financial facts |
| Cache correctness | Corpus/model/prompt/query cache version; normalized-unit version advanced; static assets versioned; HTTP revalidation | Server dataset changes require restart |
| UI asynchronous correctness | View/request guards stop late Brief, filter, company and research responses replacing newer views; four real-code synthetic race tests | Not full browser/network-chaos certification |
| API/model protection | Existing POST body/rate limits, capped opt-in Gemini, structured evidence IDs and number checks, call/token reservation, concurrency/cache | Request limits process-local; semantic entailment not guaranteed; provider tests mocked |
| Immutable imports and reproducibility | Existing IDs reject differing replacement; reviewed extraction pins original PDF hash and amount; verify_replay.py and verify_coverage.py run offline | Three JSON collection replacements are not one crash-atomic transaction; use CLI with no concurrent writers |
| Mobile UX | Fresh WIPRO/ICICI research at 375×812; desktop issuer coverage at 1200×800; wide table internally scrollable with hint | Viewport emulation, not real-device/cross-browser proof |
| Release honesty | Placeholder credentials and AI-disabled default; public deployment explicitly incomplete | Hosting and live Gemini configuration deferred; no public URL yet |

Validation: 128 backend tests passed (one existing deprecation warning); four frontend race tests passed. Real issuer corpus regressions are distinct from synthetic currency/scale mutations and mocked Gemini calls. No money spent, commit or push performed.
