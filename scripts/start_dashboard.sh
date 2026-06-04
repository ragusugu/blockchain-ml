#!/bin/bash
# Start the current Flask + React dashboard layout.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=================================================="
echo "  Blockchain Fraud Detection Dashboard"
echo "=================================================="
echo ""

cd "$PROJECT_ROOT"

if [ ! -f "src/backend/api/ai_dashboard.py" ]; then
    echo "Backend dashboard entrypoint missing: src/backend/api/ai_dashboard.py"
    exit 1
fi

if [ ! -f "src/frontend/package.json" ]; then
    echo "Frontend package missing: src/frontend/package.json"
    exit 1
fi

echo "Starting dashboard with ./start.sh"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:5000"
echo ""

exec "$PROJECT_ROOT/start.sh"
