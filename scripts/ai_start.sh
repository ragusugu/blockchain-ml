#!/bin/bash
# AI fraud detection helper for the current src/backend layout.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/venv/bin/python"

if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="${PYTHON_BIN_FALLBACK:-python3}"
fi

cd "$PROJECT_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src/backend"

echo "============================================================"
echo "Blockchain Fraud Detection - AI Module"
echo "============================================================"
echo ""
echo "1) Train AI model"
echo "2) Show model info"
echo "3) Run tests"
echo "4) Show integration hints"
echo ""

read -p "Choose option (1-4): " choice

case "$choice" in
    1)
        exec "$PYTHON_BIN" "$PROJECT_ROOT/src/backend/ml/train_ai_model.py"
        ;;
    2)
        "$PYTHON_BIN" << 'PYTHON_INFO'
from ml.ai_fraud_detector import BlockchainFraudDetector
detector = BlockchainFraudDetector()
print("Model loaded:", detector.model is not None)
print("Metrics:", detector.metrics)
print("Features:", detector.feature_names)
PYTHON_INFO
        ;;
    3)
        exec "$PYTHON_BIN" -m pytest tests/test_fraud_detector.py
        ;;
    4)
        cat << 'EOF'
Current AI integration files:
  src/backend/ml/ai_fraud_detector.py
  src/backend/ml/ai_integration.py
  src/backend/ml/train_ai_model.py

Useful examples:
  from ml.ai_integration import AIEnrichedETL
  etl_ai = AIEnrichedETL()
  enriched = etl_ai.enrich_with_fraud_scores(raw_transactions)

Dashboard model endpoint:
  GET /api/model-info
EOF
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
