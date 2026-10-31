#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pidginguard run --backend "${PIDGINGUARD_BACKEND:-echo}" --name "${1:-baseline}" "${@:2}"
