# FINN CP07 — bounded Gemini adapter, credentials deferred

27 October 2026 IST. Status PARTIAL: adapter and mocked controls implemented/tested; LIVE GEMINI NOT VERIFIED. Public deployment NOT DEPLOYED. Branch main, committed HEAD d2221e4; changes remain uncommitted.

## Changed files / behavior
backend/app/reasoning.py adds an opt-in Gemini generateContent adapter (gemini-2.5-flash by default), typed JSON claims/citations, bounded reviewed source context, no tools/search/URL context, timeout, no automatic retry, numeric-token grounding rejection and sanitized errors. backend/app/research.py routes deterministic financial facts without model calls; interpretive retrieval can make one reasoning call, de-duplicates concurrent identical requests and caches successful results by source/fact/model/prompt version. Provider failures return source-only fallback and are not durably cached. Cached answers show zero new calls. backend/app/main.py exposes enabled state and aggregate usage without keys. frontend/app.js preserves the design and displays answer limitations. .env.example provides disabled placeholder configuration. backend/tests/test_reasoning.py tests provider behavior using httpx mocks only.

Model/API references checked against Google's documentation on 27 October 2026:
https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash
https://ai.google.dev/gemini-api/docs/generate-content/structured-output
https://ai.google.dev/gemini-api/docs/pricing
Model availability, free-tier eligibility and billing remain account-specific. User will configure secret later; no key requested in chat or committed.

## Actual tests
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest backend/tests -q -p no:cacheprovider` -> 86 passed, 0 failed, one existing dependency warning, 0.65 s. Raw output docs/evidence/phase2/tests.txt. `node --check frontend/app.js` -> exit 0. One intermediate test used words absent from available source snippets and correctly made no provider call; corrected the synthetic question to match available evidence before testing concurrency suppression.

Mock-only cases: structured payload, no-tool contract, exact cited IDs, unsupported numeric claims, malformed JSON, 400/401/403/429/500, timeout/no retry, disabled/placeholder config, missing evidence, deterministic zero-call facts, persistent daily call/token reservations, concurrency admission and same-question suppression/cache. No real provider inference, output quality, latency or billing measurement is claimed. Model-generated prose can still be substantively wrong despite valid citations; UI labels it MODEL_INTERPRETATION, not verified financial fact.

## API cost and protection controls
AI_ENABLED defaults false. Placeholder/empty keys disable calls. Default local caps: 20 requests/day, 50,000 conservatively reserved tokens/day, 800 max output tokens, 12,000 evidence chars, 20-second timeout, 2 concurrent calls. SQLite BEGIN IMMEDIATE protects daily budget reservations across processes sharing a DB; single-process concurrency only, one worker recommended. Reservations include serialized UTF-8 input bytes plus output cap, are kept after failures, and are conservative bookkeeping rather than a tokenizer/billing guarantee. Actual provider-reported tokens tracked separately when returned. Cost in money NOT_MEASURED. No purchase, billing activation, API key exposure or real model request.

## Coverage, three answers and new ticker
Unchanged from CP06: 6 evidence / 27 facts / 2 guidance records across INFY legacy curated FY25/Q4 and prior comparatives; HINDUNILVR and ASIANPAINT genuine reviewed PDF annual FY25/FY24. No new source claims in this adapter phase.
- INFY Q4 FY25 revenue/PBT -> 40,925 / 9,663 INR crore, original results source infy-results-fy25.
- HINDUNILVR FY25 consolidated revenue -> 63,121 INR crore, +1.98% YoY; hul-ar25-consolidated-p186.
- ASIANPAINT FY25 standalone PBT/PAT -> 4,897.18 / 3,584.88 INR crore; asian-ar25-standalone-p12.
Exact question/API records: docs/evidence/phase1/questions.json. ASIANPAINT is not in the mock watchlist, uses generic facts path, and rejects a consolidated request when only standalone evidence exists. ZENSARTECH remains missing-source.

## Browser evidence
Current multi-issuer mobile browser verification from CP06: observed 375×812 CSS pixels; HUL and Asian Paints citations visible, no page overflow. docs/evidence/phase1/mobile-hul.jpg and mobile-asianpaints.jpg. This phase changed only limitations/configuration copy in frontend and syntax-checked it; live-provider rendering not tested because no credentials. Final browser refresh still required after subsequent Push changes.

## Blockers / next steps
Live Gemini quality and account budget verification blocked by user-deferred key. Public hosting blocked by deferred hosting target/credentials; no placeholder URL claimed. Primary-source breadth remains narrow, source rights review and unknown publication timestamps persist. Next: bounded authentic price/filing coverage across the existing watchlist, test normalization/append/conflict behavior, then refresh actual browser evidence and prepare one-service deployment config without rewriting the frontend. Do not promote synthetic model tests to genuine issuer evidence.
