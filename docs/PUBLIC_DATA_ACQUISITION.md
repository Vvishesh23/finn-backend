## CP09 update — 28 October 2026

[Current checkpoint](checkpoints/CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md): 11 financial research issuers, 16 evidence records, 71 facts; eight new reviewed PDFs, 44 reproducible facts. 128 backend tests and four frontend race tests pass. [Robustness matrix](ROBUSTNESS_MATRIX.md) distinguishes implemented controls from remaining gaps. Coverage remains historical/partial; deployment and live Gemini evaluation are pending deferred configuration. Earlier entries below are historical.

# Public acquisition — verified 27 October 2026

Eight initial attempts failed under sandbox networking. After permitted network access and use of the verified system CA store:

| Source | Observed result | Imported |
|---|---|---|
| Yahoo chart, INFY.NS | HTTP 200; 64 bars | 63 prior-day-finalized daily bars |
| Yahoo chart, RELIANCE.NS | HTTP 200; 64 bars | 63 bars |
| Yahoo chart, HDFCBANK.NS | HTTP 200; 64 bars | 63 bars |
| NSE corporate-announcements, symbol INFY | HTTP 200; 2,942 raw records | 20 minimal records |
| Infosys results PDF | Direct HTTP 403; web reader returned PDF and page 12 table | Manually verified derived facts |
| Infosys FY25 call PDF | Direct HTTP 403; web reader returned 27 pages | Minimal source paraphrase, pages 3–4 |
| Infosys FY24 call PDF | Direct HTTP 403; web reader returned 28 pages | Initial guidance paraphrase, page 4 |
| Infosys annual-report PDF candidate | Direct HTTP 403 | Not downloaded |
| NSE-linked results, call, annual-report attachments | Three direct attempts timed out | No PDFs imported |
| Infosys FY25 annual-report HTML | Web reader accessible | Minimal CEO-letter source note |

Exact attempted URLs and byte counts are recorded in `demo/acquisition.json`. Yahoo pattern: `https://query1.finance.yahoo.com/v8/finance/chart/INFY.NS?range=3mo&interval=1d`. NSE: `https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=INFY`.

Successful public metadata access is not an assertion of unlimited automation or redistribution rights. No credentials, CAPTCHA bypass, rotating proxy or private session used. No repeated requests after access denial. Samples are local research artifacts; review provider terms before public deployment. No original PDFs redistributed.

The snapshot is genuine historical replay, not a live feed. Last imported EOD: 26 October 2026; source clock dates and exchange publication times remain separate. Current-day price bars excluded conservatively. Research source notes are manual verification, not an automated document-parser success claim.
