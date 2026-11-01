# CP11 — release handoff, INCOMPLETE

1 November 2026, Asia/Kolkata. Submission deadline is today. **Public deployment URL: NOT DEPLOYED / NOT PROVIDED. Live Gemini: NOT TESTED.** The main evaluator flow has been checked locally, not on a public deployment. CP11 therefore does not pass its required release gate.

## Repository state

Branch `main`, exact HEAD `d2221e4b88c843ede399bd8db6047cd9bb5b30e3`. **Dirty:** modified and untracked implementation files from CP06–CP11 remain uncommitted. No commit, push, remote creation, hosting account access, production secret change, billing action or assessment email was performed. The current HEAD alone is not the implemented application. Exact current file list: ../evidence/cp11/git-status.txt.

Existing work/checkpoints are preserved. Read CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md, CP10_SECURE_GEMINI.md, the earlier CP11_DEPLOYMENT_READINESS.md and ../../CODEX_HANDOFF.md. Original ENAM PDFs were read previously and remain authoritative; the supplied Markdown plans do not authorize secret/account access or submission actions. No old Indian-equities/HDD project was accessed or copied.

## Freeze verification and fixes

Preserved 11 financial research issuers, 71 verified facts, 16 evidence records, two guidance records, 18 mock holdings, 17 authentic EOD series / 1,071 bars and 432 filings. No new source content or claimed coverage was invented.

Genuine blockers fixed incrementally:

- The frontend previously threw away a valid research fallback when the backend returned 429/503. It now shows a clear error and retains cited source evidence, missing/model status and a usable input.
- Default Brief now opens **Latest import**, pinned to the actual latest stored filing timestamp, with the interval visible. Real-clock 24h/7d controls remain available and can correctly be empty as the import ages.
- April replay and custom historical views hide later EOD/current-alert cards. October EOD prices are not presented as April prices. Filing-alert cutoff matches the displayed Latest import interval and price dates remain explicit.
- Persistent deployment profile uses a single instance and disk-backed SQLite. Root render.yaml remains preserved but prominently labelled legacy ephemeral/no-model only.
- Public HTTP smoke now checks coverage, latest digest, company filter, historical replay, anomaly thresholds and deterministic covered/unknown research without invoking inference.

No frontend framework rewrite or major architecture replacement.

## Exact CP11 files changed / added

Application: backend/app/main.py; frontend/app.js, index.html; backend/tests/test_expanded_coverage.py (asset version); frontend/tests/navigation.test.cjs.

Release tests/tools: backend/tests/test_release_readiness.py; scripts/smoke_url.py; scripts/run_mock_preview.py; scripts/preview_app.py (local fake faults only); scripts/package_review.py; backend/requirements.lock; Dockerfile; deploy/render-persistent.yaml; deploy/compose.yaml; render.yaml (legacy warning).

Handoff: DEPLOYMENT_README.md; docs/LIVE_VERIFICATION_CP11.md; EVALUATOR_WALKTHROUGH_CP11.md; ARCHITECTURE_CP11.md; AI_BUILD_HISTORY_INDEX.md; COVER_EMAIL_CP11_DRAFT.md; SUBMISSION_STATUS_CP11.md; this report; append-only current-status updates to README.md, CODEX_HANDOFF.md, GPT_REVIEW.md, docs/RESUME_HERE.md, TEST_RESULTS.md, WORKLOG.md, SUBMISSION_CHECKLIST.md, DEMO_WALKTHROUGH.md, and checkpoint index/latest/earlier CP11 procedure. Evidence: docs/evidence/cp11/*.

## Executed commands and real results

| Command | Actual result |
|---|---|
| `python3 scripts/run_isolated_tests.py -q` | **161 passed, zero failed**, one existing Starlette/httpx deprecation warning; ../evidence/cp11/backend-tests.txt |
| `node --test frontend/tests/navigation.test.cjs` | **8 passed, zero failed**; ../evidence/cp11/frontend-tests.txt |
| `node --check frontend/app.js` | Exit 0 |
| `git diff --check` | Exit 0 |
| `python3 scripts/run_isolated_tests.py --demo` | Mock-only demo passes; corpus assertion 11/71 preserved; ../evidence/cp11/mock-demo.json |
| Clean-environment `.venv/bin/python -m pip --isolated check` | No broken requirements found (executed during preceding CP11 work) |
| Clean-environment YAML parser / path checks | Both deployment files parsed; single-instance/durable paths align; ../evidence/cp11/deploy-config-check.json. Provider schema validation NOT RUN |
| `python3 scripts/run_mock_preview.py --mode disabled --port 8011` | Actual clean-environment no-key local preview |
| `python3 scripts/run_mock_preview.py --mode unavailable --port 8012` | Actual local fake 503 provider preview, zero real Gemini calls |

The prior CP10 157 backend/four frontend tests remain included. Four backend release checks and four frontend acceptance tests were added. Existing four-process one-call budget test still passes. New fresh-process restart test proves daily call cap, cached answer namespace and session signer persist in one SQLite file. Abandoned leases continue blocking after process exit and recover after synthetic expiry without resetting charged usage. Atomic reservation uses BEGIN IMMEDIATE; failures/retries remain charged. Client quotas/global budget/cache-isolation/no-key tests pass.

These are local/application tests. A cloud persistent-volume restart, production reverse proxy, Linux Docker build, Render schema/build, public HTTP smoke and physical-device/cross-browser checks have **not** been executed. No tests are reported as failing in the final suite; these unexecuted acceptance gates remain blockers.

## Actual end-to-end browser results

See [walkthrough matrix](../EVALUATOR_WALKTHROUGH_CP11.md), with screenshot paths under ../evidence/cp11.

- 375×812 mobile Latest import and LT filter: three disclosures and two collapsed routine disclosures; source dialog showed actual NSE URL/time. April replay: six INFY disclosures, later price observations hidden.
- Thresholds 0.1% / 0.1×: 33 EOD observations; restored 3% / 2×: two. Four filing alerts at actual import cutoff. Defaults restored.
- WIPRO FY25 revenue/profit: 89,088.40 / 17,495.70 / 13,218 INR crore for revenue/PBT/total PAT, primary PDF page 272 / printed 286; missing EBITDA; no inference. WIPRO is outside the mock watchlist and uses the generic pipeline.
- Follow-up `Explain FY25 consolidated revenue caveats`: honest retrieval-only fallback with source passage and zero inference when model disabled.
- ZENSARTECH FY25 revenue: MISSING, no sources or inference; syntax accepted without listing certification.
- Desktop 1200×800 time-window/company controls exercised. Fake provider 503 displayed error **and** HUL source evidence; simulated, not live outage proof.
- WIPRO mobile page width/document scrollWidth both 375; table scrolls internally.
- NSE and Wipro primary PDF URLs opened blank viewers here. Navigation is observed; publisher download/render/access is **NOT VERIFIED** in this browser. Historical acquisitions/reviews in CP09 remain distinct from current source accessibility.

Local URLs are not public deployment URLs. Public evaluator workflow remains NOT VERIFIED.

## Deployment prepared and manual steps

[Deployment README](../../DEPLOYMENT_README.md) gives reproducible native/container builds, startup, health, durable-volume requirements, public smoke and rollback. `deploy/render-persistent.yaml` is a paid disk-backed one-instance option, not a free persistent service. Docker Compose is an existing-host option with a named volume and loopback port for an owner-configured HTTPS proxy. No purchase was made. Owner must confirm cost and actually mount/test storage. The full installed public dependency set is pinned for Python 3.12; no Linux build or cryptographic package lock claim.

Owner participation required, in order:

1. Review intended file inventory and current uncommitted work. Create/authorize GitHub repository and commit/push the reviewed source yourself, or explicitly authorize those actions separately. Do not publish secret files, databases or full PDFs.
2. Set up host and durable volume yourself. Apply the persistent blueprint or existing-host Compose; deploy AI disabled. Confirm budget DB survives restart/redeploy. No independent replicas.
3. Provide the actual public HTTPS URL only. Run scripts/smoke_url.py and repeat phone/desktop walkthrough. Source publisher rendering must be checked in a normal browser if this viewer remains blank.
4. Configure runtime Gemini secret privately outside Codex only after account quota/privacy review. Follow SECURE_GEMINI_SETUP.md and LIVE_VERIFICATION_CP11.md; send redacted outcomes, never key/headers/environment/log dumps.
5. Export/share genuine build conversation and add verified public/repository/history links. Review final covering draft and approve sending separately. No email is sent by this work.

## Secret boundary and remaining security risks

No real credential, existing .env/secret file or hosting account was accessed. Tests/preview receive literal clean environments and use disabled/fake providers; test network connections are blocked. SDK adapter code is present but real authenticated use remains NOT TESTED. Ignore rules/package exclusions are not a barrier against same-OS-privilege access; production secrets require a separate owner-controlled host/secret manager outside Codex.

SQLite shared-file limits are atomic across processes on one host, not independent replicas. A claimed persistent path does not prove cloud durability. Address quotas are approximate (NAT/shared ingress and rotating IP risks); exact trusted proxy configuration is required. Session-cache cookies are not authentication/encryption. Old CP09 unscoped cache data remains privately preserved and unused. Plausible unsupported verbal claims can pass citation/numeric structure checks; human entailment review remains required. PII heuristics are incomplete. Provider/platform logs/retention/account quotas and other users of the same key remain outside application guarantees.

## Submission deliverables / blockers

Prepared: deployment README/profiles; local source with tests; architecture/integrity overview; source provenance/limitations; raw executed test results; authentic work-log/history index; concise draft email; evaluator walkthrough; owner-only live test; source-only review export tool.

**Not complete:** actual GitHub publication, public deployment URL and main public Push/Pull verification, independent live Gemini validation, actual publisher rendering here, genuine conversation export/share link, final links/email approval. No redistribution licence is invented for full source material; export excludes original PDFs/secret files/SQLite/HDD inputs. The explicit export selection can detect only limited patterns in included files, not guarantee all repository/history content is secret-free.

Current CP11 status: **PARTIAL / INCOMPLETE**. Next decisive action is owner deployment with durable storage and provision of its real public URL. No further feature expansion should delay this gate.
