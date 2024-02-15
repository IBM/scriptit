#!/usr/bin/env bash

set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

fail_under=${FAIL_UNDER:-"100"}
PYTHONPATH="${BASE_DIR}:$PYTHONPATH" python3 -m pytest \
    --cov-config=.coveragerc \
    --cov=scriptit \
    --cov-report=term \
    --cov-report=html \
    --cov-fail-under=$fail_under \
    $warn_arg "$@"
