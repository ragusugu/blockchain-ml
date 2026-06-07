# Testing Guide

Use this guide to verify the current `src/backend` and Vite React layout.

## Setup

```bash
cd /home/sugangokul/Desktop/blockchain-ml

# Python dependencies are expected in the local venv
./venv/bin/python --version

# Frontend dependencies are managed from src/frontend
cd src/frontend && npm install
```

## File Structure Smoke Check

```bash
test -f src/backend/api/ai_dashboard.py
test -f src/backend/etl/transform.py
test -f src/backend/ml/ai_fraud_detector.py
test -f src/frontend/src/App.jsx
test -f src/frontend/vite.config.js
test -f tests/test_transform.py
```

## Backend Unit Tests

```bash
./venv/bin/pytest
```

Focused test runs:

```bash
./venv/bin/pytest tests/test_transform.py
./venv/bin/pytest tests/test_fraud_detector.py
./venv/bin/pytest tests/test_config.py
```

## Backend Import And Compile Checks

```bash
PYTHONPATH=src/backend ./venv/bin/python -c "import api.ai_dashboard; print('ai_dashboard import ok')"

PYTHONPATH=src/backend ./venv/bin/python -m py_compile \
  src/backend/api/ai_dashboard.py \
  src/backend/etl/storage.py \
  src/backend/etl/ankr_streamer.py \
  src/backend/processing/scheduler.py \
  src/backend/ml/realtime_processor.py \
  src/backend/ml/train_ai_model.py
```

## Frontend Build

```bash
cd src/frontend
npm run build
```

The production build should emit `src/frontend/dist`, which is the folder served by the Flask backend and copied by `docker/Dockerfile.frontend`.

## Deployment File Check

```bash
bash scripts/deployment/verify-setup.sh
bash -n start.sh scripts/*.sh scripts/deployment/*.sh
```

## Optional Live Checks

These checks require live services and network access:

```bash
./start.sh
curl http://localhost:5000/api/health
curl http://localhost:5000/api/options
```

For RPC failures, see [RPC Connection Troubleshooting](RPC_CONNECTION_FIX.md).
