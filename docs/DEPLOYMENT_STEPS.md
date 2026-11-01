## CP10 update — 31 October 2026

[Current checkpoint](checkpoints/CP10_SECURE_GEMINI.md): 157 backend + four frontend tests passed, preserving 11 issuers/71 facts. [Private owner-only setup guide](SECURE_GEMINI_SETUP.md) contains the real trust boundary, privacy terms, configuration, quotas, rollback and live-test checklist. Use `python3 scripts/run_isolated_tests.py -q`; direct pytest is intentionally disabled. Actual tests use a literal clean environment, temporary SQLite and no network. Live Gemini remains NOT TESTED; public deployment remains incomplete. Do not read or configure real secrets in Codex. Historical entries below may describe the superseded direct-HTTP adapter, unscoped cache or process-local concurrency.

# Deployment preparation — NOT DEPLOYED

The app runs as one same-origin FastAPI service, so no frontend/backend CORS configuration is needed.

1. Review Yahoo/NSE/issuer terms and remove or replace any sample not permitted on a public demo. No blanket redistribution rights are claimed.
2. Choose a hosting account and plan explicitly authorized by the user. No paid account should be opened automatically.
3. Use Python 3.12, install `backend/requirements.txt`, and start `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` from project root. Or build the supplied Dockerfile. Docker build has not been executed in this session.
4. Keep a single worker. Mount persistent writable storage and set FINN_DB to its SQLite path; without a persistent disk, derived caches/observed alerts reset across deployments. Public snapshots remain in versioned JSON.
5. Do not add real API keys to the frontend. This release has no runtime model integration or secrets.
6. Verify HTTPS public `/health`, mobile Brief, replay, source details, custom date/company/category filters, threshold persistence, unknown ticker, unsupported/current research period and request-rate errors. Recheck source rights and source availability.
7. Create a user-authorized GitHub repository and push only after inspecting tracked files. Add the real URLs to the submission checklist and CP05. No verified URL exists now.

Local startup: `./start.sh`, then http://127.0.0.1:8000. A localhost URL is not a public evaluator link.

## Current deployment preparation — 27 October continuation
`render.yaml` now provides a one-service free Python/FastAPI blueprint preserving the existing frontend. Build: pip install -r backend/requirements.txt. Start: python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1. Health path /health. The user deferred account/credentials, so no service or public URL was created and no source pushed.

Official Render docs checked: https://render.com/docs/deploy-fastapi , https://render.com/docs/blueprint-spec and https://render.com/docs/free . Free service spin-down/restart loses local SQLite and incurs cold-start delay. The blueprint deliberately leaves AI_ENABLED=false; budget reservations must persist before enabling any paid provider. No purchase/plan upgrade authorized or made. Configure a durable budget store/provider caps if reasoning is enabled later. Source redistribution terms must be reviewed before uploading source snapshots.

The available Sites connector hosts Worker JavaScript rather than this existing Python service; converting the backend solely to fit that host would undermine the requested preservation of the working implementation. No parallel replacement app was built. Render configuration is preparation, not verified hosting. Docker build cannot currently run: `docker version --format '{{.Server.Version}}'` failed because no Docker daemon/socket is running. YAML syntax checks are not provider deployment validation.
