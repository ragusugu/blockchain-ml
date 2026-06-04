#!/bin/bash
# Real-time processor quick start for the current src/backend layout.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/venv/bin/python"

if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="${PYTHON_BIN_FALLBACK:-python3}"
fi

cd "$PROJECT_ROOT"

echo "================================================"
echo "Real-Time Blockchain Data Processor"
echo "================================================"
echo ""
echo "1) CONSOLE MODE (watch live transactions)"
echo "2) JSON MODE (save to file)"
echo "3) CSV MODE (save to spreadsheet)"
echo "4) WEBHOOK MODE (send to webhook)"
echo ""

read -p "Enter choice (1-4): " choice

case "$choice" in
    1)
        export OUTPUT_MODE=console
        ;;
    2)
        export OUTPUT_MODE=json
        ;;
    3)
        export OUTPUT_MODE=csv
        ;;
    4)
        read -p "Enter webhook URL: " webhook_url
        if [ -z "$webhook_url" ]; then
            echo "No webhook URL provided"
            exit 1
        fi
        export OUTPUT_MODE=webhook
        export WEBHOOK_URL="$webhook_url"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

export PYTHONPATH="$PROJECT_ROOT/src/backend"
exec "$PYTHON_BIN" "$PROJECT_ROOT/src/backend/ml/realtime_processor.py"
