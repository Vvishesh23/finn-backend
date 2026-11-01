# FINN deployment handoff — CP11 partial, 1 November 2026

**Public URL: NOT DEPLOYED. Live Gemini: NOT TESTED.** The source is ready for owner-controlled deployment; no account, credential, purchase, commit, push or email was performed. Do not deploy the old committed HEAD alone: the implemented work is still uncommitted. See docs/checkpoints/CP11_RELEASE_CHECKPOINT.md.

## Fastest persistent deployment

Use `deploy/render-persistent.yaml` as the Render Blueprint path, with this directory as the repository root. It defines a single Python web service, a 1 GB disk mounted at `/var/data`, SQLite at `/var/data/finn.sqlite3`, one worker, health `/health`, automatic deploys off and AI disabled. You must create/connect the repository and authorize hosting yourself. Confirm the displayed price before purchase: persistent disks require paid Render compute; no free durable-disk claim is made. Official references: https://render.com/docs/disks and https://render.com/docs/blueprint-spec (checked 31 October 2026). Only data under the mount survives redeployments. Disk-backed deployments have downtime and are single-instance.

The existing root `render.yaml` is explicitly a legacy ephemeral/no-model profile. Do not use it for inference or describe its quota storage as durable.

Alternative on an existing host: `docker compose -f deploy/compose.yaml up --build -d`. The named volume `finn_data` persists the SQLite database; the port binds only to localhost. Configure a trusted HTTPS reverse proxy on that host before making it public. Do not run `docker compose down -v`: that destroys quota records and session identity. Production secrets must be injected privately by the owner's host secret manager, never committed Compose overrides or CLI arguments. Do not expose Docker or the database port.

Docker/Compose commands are prepared, not executed here: a working Docker daemon and production host were not verified. The installed dependency set is pinned in `backend/requirements.lock`; native Render build installs it. A Linux container build and provider Blueprint validation remain owner checks. Local `pip check` passed on Python 3.12; the lock is not a package-integrity hash lock.

## Local verification and build

```
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.lock
python3 scripts/run_isolated_tests.py -q
node --test frontend/tests/navigation.test.cjs
node --check frontend/app.js
```

The test runner deliberately strips the environment and creates a temporary database; direct pytest is refused. Optional PDF extraction dependencies are separate in `backend/requirements-pdf.txt`; the serving app needs no full source PDF or HDD. To preview safely without a key: `python3 scripts/run_mock_preview.py --mode disabled --port 8011`. `--mode unavailable` and `--mode quota` are local fake-provider fault demonstrations, not real provider tests. The production entry point is always `backend.app.main:app`, never `scripts.preview_app:app`.

Production startup:

```
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1 --no-proxy-headers --no-access-log
```

Set nonsecret `FINN_DB=/var/data/finn.sqlite3`, `AI_BUDGET_STORAGE_PERSISTENT=true`, `AI_ENABLED=false`, `REASONING_PROVIDER=disabled` on the host first. The parent directory must exist and be writable on the actual durable mount. Do not use in-memory/temp storage, multiple hosts or independent replicas. Keep the same DB through restarts and rollback. The runtime persistence declaration cannot verify a cloud mount; prove durability before enabling inference.

## Health and public acceptance

`/health` must return 200 and authentic snapshot dates; it reports configured provider state, not key validity. `/api/coverage` must show 11 financial issuers and 71 facts. No login or evaluator API key is required. After you obtain the real HTTPS origin, run:

```
.venv/bin/python scripts/smoke_url.py --url https://YOUR-ACTUAL-HOST
```

Replace the hostname yourself. This script performs deterministic requests only, verifies digest/filter/replay/threshold/research paths and makes no interpretive query. It does not prove mobile rendering or live Gemini. Save its output, then follow docs/EVALUATOR_WALKTHROUGH_CP11.md on a phone and desktop. Send back the actual public URL and redacted results only.

## Private Gemini, observability and failure tests

Follow docs/SECURE_GEMINI_SETUP.md and docs/LIVE_VERIFICATION_CP11.md outside Codex. Do not grant Codex access to production shells, hosting secrets or API keys. The credential belongs only in the host's runtime secret manager. Ignore rules are not an OS isolation boundary. No live test will be claimed without your independent redacted result.

SQLite `BEGIN IMMEDIATE` reserves daily/client/minute/token usage and concurrency leases atomically. Fresh-process tests prove budgets/cache/signing identity persist using the same file; four-process tests prove a one-call cap cannot be claimed twice. These tests do not prove your cloud disk mount or protect other applications using the same provider key. Conservative defaults and exact configuration names are in `.env.example`; verify against your actual project quota. Trusted proxy CIDRs must be exact and verified; leave empty rather than trusting arbitrary forwarding headers.

Monitor health availability, aggregate usage/failure counters, status codes, latency and cache outcomes. Do not enable raw prompt, response, header, environment or SDK tracing. Default application access logs are disabled. Provider/platform logs remain outside these guarantees. GET /api/usage contains public aggregate metadata; process counters reset, SQLite daily counts persist.

## Rollback

Before changing deployment, disable reasoning and take a private consistent SQLite backup using SQLite's backup API or a stopped-service copy. Never send that backup to Codex. Keep the disk/DB intact. Redeploy a reviewed release compatible with the additive tables, keep AI disabled, and rerun health/smoke checks. Do not restore an older budget snapshot merely to roll code back: it can reset charged usage. If restoring an old backup is unavoidable, keep inference disabled until the owner reconciles today's usage with the provider. Rotate/revoke keys privately as described in the setup guide. No production action is authorized by this README.

## Repository and submission

The application source, derived public-data fixtures, tests, architecture/provenance records and checkpoints are present locally. No GitHub remote URL has been verified. Review the release file inventory before committing; never use an indiscriminate archive of the workspace. Exclude SQLite, .env files, credentials, virtual environments, full issuer/assessment PDFs and old HDD data. Original publishers retain rights; public availability is not a redistribution licence. The application links sources and ships selected derived facts only, with rights caveats.

The owner must approve/create the repository, commit/push the reviewed files, export the genuine build conversation, supply verified links, and approve the final email. This work does not fabricate share links, commits, cloud URLs or completion states.
