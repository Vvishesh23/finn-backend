# Evaluator walkthrough and observed results — CP11 PARTIAL

1 November 2026. Public URL absent. The observations below were made on a clean local no-credential FastAPI preview, not a deployed host. Mobile 375×812 and desktop 1200×800 were exercised in the in-app browser. Physical phones, other browsers, public TLS, cold starts and cloud persistence remain unverified.

| Step | Observed result | Evidence / remaining check |
|---|---|---|
| Open Brief / Latest import | 15 grouped disclosures for trailing 24h ending 27 Oct 2026 17:13 IST; stale import explicitly labelled | mobile-lt-filter.jpg / desktop-latest-filter.jpg; public repeat required |
| Filter LT | Three disclosures, two routine, LT filing alert | Passed locally |
| Change 7 days / Latest import / FY25 replay | Controls change API interval; April replay has six INFY disclosures and hides October EOD/current alert cards | mobile-replay.jpg; current-clock 24h may truthfully be empty |
| View original NSE filing | Evidence dialog links actual NSE attachment and publication time | Link opened blank PDF viewer; rendering/access NOT VERIFIED, nse-viewer-unverified.jpg |
| Change thresholds | 0.1% / 0.1× produced 33 EOD observations; restoring 3% / 2× produced two; four filing alerts for import cutoff | mobile-threshold-low.jpg; defaults restored |
| Research WIPRO | FY25 revenue 89,088.40, PBT 17,495.70, total PAT 13,218 INR crore; verified-PDF page 272, missing EBITDA | mobile-wipro.jpg; zero inference attempts |
| Interpretive follow-up | `Explain FY25 consolidated revenue caveats` retained source evidence and disclosed no configured model | mobile-disabled.jpg; real Gemini NOT TESTED |
| Open cited Wipro report | Original URL opened | Blank PDF viewer here; rendering NOT VERIFIED; historical PDF acquisition/review is in CP09 |
| Outside corpus | ZENSARTECH FY25 revenue returns MISSING and unverified listing status | mobile-missing.jpg |
| Provider unavailable | Isolated fake-provider 503 displayed an error plus HUL cited source notes, not a blank answer | desktop-provider-503.jpg; SIMULATED, zero real Gemini calls |
| Quota exhaustion | Automated persistent client/global cap tests return 429 and deterministic research/dashboard survive; frontend renders citations on 429 | Tests passed; no real Google quota exhaustion claim |
| Restart | New process kept daily cap, cache namespace signer and cache; abandoned leases recover only after expiry | backend test_release_readiness.py; actual host restart still needed |

All screenshot paths are under evidence/cp11. Mobile page width 375 and document scrollWidth 375 were observed on WIPRO research. Comparison table scrolls internally. No login/evaluator key was requested. Source failures are not bypassed or silently replaced.

For the final public check, open your real HTTPS URL on a phone and desktop and repeat every row. Copy public URLs from the original-source links; inspect publisher PDFs in a normal browser if this viewer is blank. Submit only redacted outcomes to Codex. CP11 cannot pass on local evidence alone.
