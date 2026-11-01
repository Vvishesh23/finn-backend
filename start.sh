#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ ! -d .venv ]; then python3 -m venv .venv; fi
.venv/bin/pip install -q -r backend/requirements.txt
exec .venv/bin/python -m uvicorn backend.app.main:app --no-proxy-headers --no-access-log --host 127.0.0.1 --port "${PORT:-8000}"
