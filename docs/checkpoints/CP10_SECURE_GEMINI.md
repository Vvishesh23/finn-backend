# CP10 — Secure Gemini integration (mock validated; live NOT TESTED)

31 October 2026. CP09 continued incrementally. The 11-issuer / 71-fact corpus is preserved. Baseline was 128 backend plus four frontend tests (132 total); the final regression run has 157 backend plus four frontend tests (161 total). The production provider has not made an authenticated request. No production account, secret or deployment was accessed. CP11 is a prepared manual procedure, not a completed public deployment.

## Implemented architecture and secret boundary

Query → validated local plan → primary-evidence retrieval with exact period/basis/as-of → deterministic facts/ratios/guidance OR bounded interpretation → atomic SQLite quota/lease → MockReasoningProvider or Google-SDK GeminiReasoningProvider → structured claims/citation/numeric-token checks → per-session cache → response. Disabled provider retains retrieval/no-model fallback. No model executes SQL, Python, shell, external URLs or tools.

The provider abstraction is backend/app/providers.py. Gemini uses pinned google-genai 2.34.0 with a configurable gemini-3.5-flash-lite default (official documentation checked 31 October). The SDK endpoint is pinned, proxy-environment/redirect behavior disabled, automatic tools disabled, internal retries disabled, and outputs bounded. A local child process enforces the SDK wall deadline; failure details never cross as raw exception/provider text. Retry defaults to zero, optionally one transient retry with backoff and a new budget reservation; 429 is never retried.

Credential access is restricted in application code to the explicit production provider. Configuration/health/usage/mock/disabled paths do not read the key. Tests and mock preview receive a literal clean environment and temporary DB, with no ambient environment copied. SDK tests use an injected fake credential loader and fake client. No .env or existing secret file was read or created. Git/Docker exclusions and a Docker source allowlist reduce accidental packaging.

**Trust boundary:** ignore rules do not conceal secrets from an agent/program with the same OS permissions. A production process and its administrator can read runtime credentials. Real separation requires a user-controlled host/secret manager outside the Codex environment. This implementation does not provide an OS security boundary or prove unknown pre-existing files contain no secrets. No secret-discovery scan was performed because the user forbids it. See ../SECURE_GEMINI_SETUP.md for exact owner-only steps.

## Abuse prevention and privacy

Persistent SQLite transactions coordinate client/global daily counts, client/global fixed-minute counts, reserved tokens and expiring concurrency leases across processes using one shared DB file. Defaults: 6 per client/minute, 20/client/day, 6 global/minute, 100 global/day, two active calls, 100,000 reserved token-units/day. Every retry is charged. Gemini requires an explicit persistent-storage declaration and a non-temporary DB path; this cannot prove the host mount survives redeployment. Multiple independent replicas are unsupported.

Request/body/query/context/output/time limits are configurable and bounded. Global/client inference denials produce 429; concurrency/provider unavailability produce 503. Deterministic financial answers and dashboard routes remain available. Ordinary POST rate limits are still process-local and are not described as distributed enforcement.

HTTP inference-cache keys are namespaced by a signed browser session and hashed address; Secure/HttpOnly/SameSite=Strict cookies and private/no-store response headers apply. New cache storage has a one-day read expiry and a 1,000-row cap; pruning is on writes. The old unscoped answers table is preserved but never read. Application counters store pseudonymous identities, not raw IPs. Raw prompts/complete responses are not operational log fields. Public query content can still appear in its private cached answer; this is documented. Platform/OS logs and administrators remain outside the guarantee.

The inference request sends only the question and bounded public snippets, not files, full databases, cookies, client addresses or environment values. Obvious private inputs are blocked heuristically; exhaustive PII detection is not claimed. A research-screen notice discloses outbound processing and cache handling. Provider retention/free-tier considerations and current official sources are documented in ../SECURE_GEMINI_SETUP.md.

## Exact changed files for this phase

- .env.example
- .gitignore
- .dockerignore
- Dockerfile
- render.yaml
- start.sh
- backend/requirements.txt
- backend/app/providers.py
- backend/app/inference_limits.py
- backend/app/client_privacy.py
- backend/app/reasoning.py
- backend/app/research.py
- backend/app/store.py
- backend/app/main.py
- backend/app/models.py
- backend/tests/conftest.py
- backend/tests/test_reasoning.py
- backend/tests/test_secure_gemini.py
- backend/tests/test_core.py
- backend/tests/test_expanded_coverage.py
- frontend/app.js
- frontend/index.html
- scripts/run_isolated_tests.py
- scripts/mock_reasoning_demo.py
- scripts/run_mock_preview.py
- docs/SECURE_GEMINI_SETUP.md
- docs/checkpoints/CP10_SECURE_GEMINI.md
- docs/checkpoints/CP11_DEPLOYMENT_READINESS.md
- README.md
- CODEX_HANDOFF.md
- GPT_REVIEW.md
- docs/RESUME_HERE.md
- docs/TEST_RESULTS.md
- docs/WORKLOG.md
- docs/RUNTIME_REASONING.md
- docs/DEPLOYMENT_STEPS.md
- docs/ROBUSTNESS_MATRIX.md
- docs/checkpoints/LATEST_CHECKPOINT.md
- docs/checkpoints/CHECKPOINT_INDEX.md
- docs/evidence/cp10/

The git status snapshot includes earlier uncommitted phases too; it is not a claim that every current uncommitted file was newly changed by CP10. Source corpus demo JSON/manifests were not changed in CP10. Branch main remains uncommitted/unpushed.

## Actual commands and results

| Executed command | Actual outcome |
|---|---|
| `python3 scripts/run_isolated_tests.py -q` | 157 passed; one existing Starlette/httpx deprecation warning. ../evidence/cp10/backend-tests.txt |
| `node --test frontend/tests/navigation.test.cjs` | Four passed; zero failed. ../evidence/cp10/frontend-tests.txt |
| `node --check frontend/app.js` | Exit 0 |
| `python3 scripts/run_isolated_tests.py --demo` | Isolated mock-only demo; ../evidence/cp10/mock-demo-final.json |
| `git diff --check` | Exit 0 |
| `python3 scripts/run_mock_preview.py` | Actual local 127.0.0.1:8010 preview with clean environment, mock provider and temporary DB |

The SDK was installed with a subprocess using a literal clean environment: `.venv/bin/python -m pip --isolated install --no-cache-dir google-genai==2.34.0`. No real credential or authenticated request was used. Package installation accessed PyPI; this is distinct from the network-blocked application test suite.

Initial new multi-connection tests exposed a baseline test module overriding FINN_DB with an in-memory DB. The override was removed; the isolated runner now owns a temporary file, and both connection-level and actual multi-process checks pass. No old regression test was dropped.

## Mock demonstration and research routing

**HINDUNILVR — Explain FY25 consolidated revenue caveats**

HTTP 200; route `mock_grounded_interpretation`; status `MODEL_INTERPRETATION`. The supplied issuer passage is the available evidence; this is a mock interpretation, not live Gemini analysis.

This is a deliberately fixed fake-provider demonstration, not a live Gemini research answer. Its fake attempt count is not a real API call.

Source: [Hindustan Unilever Limited — PDF page 186 / printed pages 368–369, consolidated profit and loss](https://www.hul.co.in/files/annual-report-2024-25.pdf); method pdf_extracted_reviewed.

**WIPRO — FY25 revenue and profit**

HTTP 200; route `deterministic`; status `VERIFIED_DERIVED`. WIPRO · FY25 annual · Consolidated Ind-AS; INR crore; annual periods. Revenue: INR 89,088.40 crore. Definition: Revenue from operations. YoY -0.75%. PBT: INR 17,495.70 crore. Definition: Profit before tax including share of associate and joint venture. YoY +18.85%. PAT (total profit): INR 13,218.00 crore. Definition: Total profit including non-controlling interests. YoY +18.95%.

Source: [Wipro Limited — PDF page 272 / printed page 286](https://www.wipro.com/content/dam/nexus/en/investor/annual-reports/2024-2025/Integrated-annual-report-2024-25.pdf); method pdf_extracted_reviewed.

**HINDUNILVR — FY25 consolidated PAT margin**

HTTP 200; route `deterministic`; status `VERIFIED_DERIVED`. HINDUNILVR · FY25 annual: total-PAT/revenue margin 16.91%. Deterministic calculation; PAT and revenue retain their cited definitions.

Source: [Hindustan Unilever Limited — PDF page 186 / printed pages 368–369, consolidated profit and loss](https://www.hul.co.in/files/annual-report-2024-25.pdf); method pdf_extracted_reviewed.

**INFY — Did management deliver on FY25 guidance?**

HTTP 200; route `deterministic`; status `VERIFIED_DERIVED`. FY25 Constant-currency revenue growth: original 1–3%, actual 4.2%; exceeded, gap beyond band 1.2 percentage points. FY25 Operating margin: original 20–22%, actual 21.1%; met, gap beyond band 0.0 percentage points. Initial guidance comparison only. Subsequent revisions and a rolling four-quarter promise history are not indexed. Not an assessment of management quality.

Source: [Infosys — PDF page 4, CEO remarks](https://www.infosys.com/investors/reports-filings/quarterly-results/2023-2024/q4/documents/transcripts/earningscall.pdf); method legacy_curated_note.

Source: [Infosys — PDF page 3, CEO remarks](https://www.infosys.com/investors/reports-filings/quarterly-results/2024-2025/q4/documents/transcripts/earningscall.pdf); method legacy_curated_note.

**ZENSARTECH — Explain FY25 risks**

HTTP 200; route `deterministic`; status `MISSING`. ZENSARTECH: source unavailable in this local corpus or as-of cutoff. Ticker syntax is valid; exchange listing status is unverified.

The repeated interpretive question hit the same-session cache with zero new fake attempts. Real Gemini calls: **zero**. No monetary savings or billing estimate is claimed. Amount/ratio/guidance examples above use genuine stored issuer facts and deterministic arithmetic; source notes remain labelled reviewed-PDF versus legacy-curated. The fake interpretation does not demonstrate semantic answer quality.

## Security test evidence

- Startup/disabled metadata and retrieval work with credential reads explicitly made to fail; fake-provider operation requires no credential. No real socket connection is allowed in application tests.
- An injected SDK client validates actual SDK config types, fixed endpoint, fake credential loading, timeout, single SDK attempt and disabled tools. The wall-deadline cleanup path is tested with an injected fake process; real authenticated SDK execution is NOT TESTED.
- Fake credential canaries are absent from frontend/health/usage/responses; provider 400/401/403/429/500 and exceptions are sanitized. Missing credential fake adapter returns safe 503 plus source retrieval.
- Existing malformed input/body tests and configurable query/body bounds pass. Context/input budgets prevent provider invocation. Obvious private questions are not sent.
- Same-session cache hit and separate-session miss are demonstrated; source-version changes invalidate model answers; forged session cookies rotate.
- Client minute/day limits, global minute/day/token caps and exhausted-budget no-call paths pass. A four-process test sharing one SQLite file permits exactly one reservation under a one-call global cap. Leases seen from a second connection enforce the concurrency cap.
- Optional retries are bounded and cannot exceed the global budget; provider 429 is not retried.
- Untrusted evidence stays a data field; no tool configuration is granted. Invalid citation IDs/unsupported numerical claims are rejected. This is not proof that every plausible verbal hallucination or prompt injection is detectable.
- Explicit standalone research cannot silently use consolidated evidence. Existing fiscal/currency/unit/publication/provenance/revision regressions remain passing. Numerical PAT-margin calculation is deterministic; unsupported ratios fail closed.

## Browser evidence

Actual isolated mock preview at 375×812: the privacy notice and a HINDUNILVR mock interpretation with primary-source citation were visible; repeat showed cached response and zero Gemini calls. Page scrollWidth 375 equals viewport 375. Screenshot: ../evidence/cp10/mobile-mock-privacy.jpg. This is viewport testing, not a physical-phone or cross-browser certification. No pre-existing server or production configuration was used.

## Remaining limitations and exact next steps

1. Owner reviews this checkpoint before any further major phase. The requested CP11 manual procedure is prepared in CP11_DEPLOYMENT_READINESS.md, but no host/secret was accessed and no public deployment is verified.
2. Owner privately configures durable single-host storage, trusted ingress and runtime secret, verifies actual model/project quota and current provider terms, then runs the owner-only checklist. Live Gemini remains NOT TESTED. Health reports configuration, not credential validity or actual model availability.
3. Per-client is an approximate address allowance: NAT users may share a quota, address rotation can evade a client allowance, and public unauthenticated service cannot prevent all abuse. Global persistent caps still bound this application; other apps sharing the same provider key are outside those caps. Distributed replicas need a shared service before enabling inference.
4. Cache isolation is bearer-session isolation, not user authentication or encryption. A stolen cookie/compromised host is outside that guarantee. Old cache data remains for owner-only review/purge.
5. Semantic entailment, comprehensive PII detection, live-model answer quality, real provider quota/retention/account behavior, live SDK execution and paid billing have not been certified. Usage reservations include failed/local generation attempts and conservative bytes, not exact billed token counts.
6. The financial corpus is still narrow historical evidence; broad transcripts, recent quarters and rolling four-quarter management history remain unfinished. No old HDD/repository content was accessed.

## Copy-ready independent review

Review FINN CP10 as a security/finance engineer. The implementation preserves 11 issuers/71 facts and passes 157 backend + four frontend tests. It provides disabled/mock/Google-SDK providers, isolated no-network tests, deterministic facts/ratios, signed-session caches, persistent single-host SQLite budgets/leases, bounded retries/timeouts and safe HTTP failures. Real Gemini and public deployment are NOT TESTED. No real key/secret file/account was accessed. Please inspect the exact files, mock demo, quota tests and owner-only setup guide; assess remaining risks in proxy identity, cache retention, SDK process lifecycle, prompt/citation safeguards and single-host deployment. Do not infer live model quality from mock tests.
