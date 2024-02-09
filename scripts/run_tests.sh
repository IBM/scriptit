#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Set the BASE_DIR to the parent directory of the script
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Change directory to the BASE_DIR
cd "$BASE_DIR"

# Set PYTHONPATH to include BASE_DIR for importing modules correctly
PYTHONPATH="${BASE_DIR}:$PYTHONPATH" 

# Run pytest with coverage checks
python3 -m pytest \
    --cov-config=.coveragerc \
    --cov=scriptit \
    --cov-report=term \
    --cov-report=html \
    --cov-fail-under=100 \
    $warn_arg "$@"
