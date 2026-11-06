#!/usr/bin/env bash
set -Eeuo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ ! -x .venv/bin/python ]]; then
    echo '먼저 bash setup_and_run.sh를 실행하세요.' >&2
    exit 1
fi
exec .venv/bin/python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
