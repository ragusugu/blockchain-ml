# Project Brief

Last updated: 2026-06-04

## Purpose

`blockchain-ml` is a blockchain fraud detection system for Ethereum transaction data. It fetches on-chain data from RPC endpoints, transforms it into tabular transaction records, scores transactions with machine learning, exposes results through a Flask API and React dashboard, and includes Docker/Kubernetes deployment assets.

## Core Goals

- Detect suspicious Ethereum transactions with a machine-learning assisted workflow.
- Support both scheduled/batch ETL and real-time style processing.
- Cache or persist processed transaction records in PostgreSQL when enabled.
- Provide a browser dashboard for selecting processing mode, fetching recent blocks, viewing transaction stats, and inspecting transaction details.
- Expose blockchain and fraud-analysis capabilities to MCP clients through `src/backend/mcp_server.py`.
- Keep local and production deployment paths available through Docker Compose and Kubernetes manifests.

## Current Scope

- Chain focus: Ethereum mainnet-compatible RPC endpoints.
- Backend: Flask API under `src/backend/api/ai_dashboard.py`.
- ETL: extract, transform, load, and state tracking under `src/backend/etl/`.
- ML: RandomForest-based fraud detector plus IsolationForest anomaly fallback under `src/backend/ml/ai_fraud_detector.py`.
- Frontend: Vite React dashboard under `src/frontend/`.
- Deployment: Dockerfiles, Docker Compose, and Kubernetes manifests.
- Optional streaming: Ankr HTTP polling service under `src/backend/etl/ankr_streamer.py` and `streaming_manager.py`.
- MCP: FastMCP server under `src/backend/mcp_server.py` for blockchain/RPC and fraud-analysis tools.
- Operations: scheduler, disk cleanup manager, deployment scripts, and Ankr test/setup helpers.

## Memory Bank Scope

- Full source scan completed on 2026-06-04 across backend Python, frontend React, tests, scripts, Docker, Kubernetes, root docs, VS Code/GitHub metadata, and selected documentation indexes.
- Secret-bearing files such as `.env`, `docker/.env`, and `config/.env` were intentionally not read into memory.
- Generated/dependency/cache artifacts such as `venv/`, `.pytest_cache/`, `.vite/`, package lock internals, logs, and built frontend assets are not source of truth.

## Guardrails

- Do not store RPC keys, database passwords, private keys, or full sensitive URLs in memory files.
- Treat older docs and scripts as potentially stale; source files and tests are more reliable.
- Verify live blockchain/RPC behavior before relying on it because endpoints and network behavior can change.
