#!/bin/bash
# Disk Cleanup Wrapper Script - Uses venv python automatically

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON="${SCRIPT_DIR}/venv/bin/python"

# Check if venv exists
if [ ! -f "$PYTHON" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Run cleanup script with all arguments
"$PYTHON" "${SCRIPT_DIR}/cleanup_disk.py" "$@"
