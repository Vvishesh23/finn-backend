# Owner-only live verification — NOT TESTED

1 November 2026. Run outside Codex's credential boundary, after the private setup in SECURE_GEMINI_SETUP.md. Do not send keys, headers, environment dumps, raw traces or production databases. No authenticated provider request was made by Codex.

| Check | Action outside Codex | Evidence to return, redacted |
|---|---|---|
| Real interpretation | Ask HINDUNILVR: `Explain FY25 consolidated revenue reporting caveats` | HTTP status, route must be gemini_grounded_interpretation, model identifier, latency, public claim/citation IDs; manually assess usefulness |
| Primary evidence | Inspect HUL PDF page 186 / printed 368–369 supporting the selected passage | Valid public source URL/page, observed reporting basis and period |
| Citations | Check every returned claim ID is one of the selected corpus source IDs; open original URLs | IDs and pass/fail; citations existing is not semantic verification |
| Unsupported claims | Ask `FY25 consolidated EBITDA` for HUL and `FY26 revenue` | Explicit missing evidence; deterministic path; no inferred unsupported amount or provider call |
| Numeric correctness | Ask WIPRO `FY25 revenue and profit` | INR crore values; no model attempt; definitions preserved |
| Timeout | On a separate private staging service, set a short timeout and submit one interpretive query. If the request completes too quickly, record timeout NOT EXERCISED rather than fabricating a timeout | 503 with evidence fallback if exercised; bounded elapsed time, usage delta. Do not flood provider or alter production networking |
| Quota | On staging lower global daily cap to 1, make one uncached interpretation and then a different one | Second 429/no extra provider attempt; use fake quota preview for UI fault checks; actual Google 429 is not guaranteed by lowering a local cap |
| Leakage | Privately inspect browser response/error/source and owner-controlled logs for credential presence without copying logs/values here | Pass/fail only. Do not search for/send the actual key through Codex |
| Accounting | Record aggregate SQLite counters/provider console before and after, repeat same-session query, then restart | Calls/reserved/provider-reported deltas; cache repeat zero new attempt; charged usage persists after restart |
| Fallback | Disable AI and ask the same question, then deterministic financial query | Retrieval notes/no synthesized interpretation; figures/dashboard remain available |

For a safe executable simulated outage/quota check on your local or private staging environment, run `python3 scripts/run_mock_preview.py --mode unavailable --port 8012` or `--mode quota --port 8012`. These are fake providers and must be labelled SIMULATED. They are not live timeout/quota proof. Automated tests also reject invented citations/numeric tokens and enforce the hard-deadline cleanup path with fake clients/processes; these do not establish real SDK/network behaviour.

Return this record without sensitive content:

```
Public HTTPS URL:
Deployed commit/release identifier:
Model / SDK version:
Test name:
HTTP status / route:
Public citation IDs:
Cache hit:
Attempted calls before → after:
Reserved units before → after:
Provider-reported tokens before → after:
Latency:
Result: PASS / FAIL / NOT EXERCISED
Redacted issue:
```

Budgets count reserved attempts, including failures, not guaranteed billed requests; input reservations are conservative bytes and output caps are provider token limits. Google's actual billing/retention/quotas require your account-side verification. Keep live status NOT TESTED until these results exist. No email is authorized by running this checklist.
