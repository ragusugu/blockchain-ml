#!/bin/bash
# Installation and verification script for the current blockchain-ml layout.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "Blockchain ML - Installation & Verification"
echo "=========================================================="
echo ""

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python not found: $PYTHON_BIN"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_BIN" -m venv venv
fi

echo "Installing Python dependencies..."
./venv/bin/pip install --upgrade pip setuptools wheel
./venv/bin/pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Review .env before production use."
else
    echo ".env already exists"
fi

echo ""
echo "Verifying Python imports..."
PYTHONPATH=src/backend ./venv/bin/python << 'PYTHON_CHECK'
from web3 import Web3
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from api import ai_dashboard
from etl.main_etl import BlockchainETL
from ml.ai_fraud_detector import BlockchainFraudDetector
print("Python imports verified")
PYTHON_CHECK

echo ""
echo "Ready. Useful commands:"
echo "  ./start.sh"
echo "  ./venv/bin/pytest"
echo "  PYTHONPATH=src/backend ./venv/bin/python -m processing.scheduler"
echo "  PYTHONPATH=src/backend ./venv/bin/python -m etl.main_etl"
echo "  cd src/frontend && npm run build"
echo ""
echo "Docs: documentation/guides/START_HERE.md"
