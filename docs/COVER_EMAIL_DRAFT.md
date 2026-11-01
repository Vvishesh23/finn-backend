# Draft only — not ready to send

Recipient: assessment@enam.com
Subject: ENAM - IIT screening - 2027

Dear ENAM team,

I built FINN, a mobile-first investment-intelligence prototype focused on helping an investor move from a company disclosure to the underlying evidence quickly.

The current local version combines an exchange-filings brief, a cross-sector mock watchlist, configurable end-of-day price and volume observations, and a narrow source-grounded research workflow. Its demonstration corpus uses genuine public data and clearly labels imported snapshots. A filing can lead to consolidated quarterly comparisons and an initial FY25 management-guidance comparison for Infosys, with both original earnings-call sources linked.

The main engineering choice is to keep calculations deterministic and make missing evidence visible. Publication timestamps are separate from reporting periods, volume baselines exclude the current session, financial comparisons preserve units and reporting basis, and research answers use versioned evidence caches. No runtime model or evaluator API key is required for supported queries.

The prototype remains narrower than the full brief: research coverage is limited, primary-document notes were manually verified, later guidance revisions are not indexed, and public deployment is pending. I have documented these limitations alongside the actual tests and browser evidence.

Before sending this note, I will add verified public-demo, repository and genuine AI-build-history links and complete the release checks.

Regards
