# System Patterns

Last updated: 2026-06-04

## Runtime Architecture

- `src/backend/config.py` centralizes environment-backed settings in singleton `cfg`.
- `src/backend/connections.py` owns cached Web3 and SQLAlchemy engine creation with retries/fallbacks.
- `src/backend/logging_config.py` configures shared logging and suppresses noisy dependency logs.
- `src/backend/api/ai_dashboard.py` is the Flask API and static frontend host.
- `src/frontend/src/App.jsx` is the main React dashboard state container.
- `src/frontend/vite.config.js` proxies `/api` to `http://localhost:5000` in dev and builds to `src/frontend/dist`.
- `AGENTS.md` instructs future sessions to read the full Memory Bank before work.

## ETL Data Flow

1. `etl.extract.extract_blocks()` fetches full Ethereum blocks and transaction receipts through Web3. `extract.py` uses a process-local `TTLCache(maxsize=200, ttl=300)` guarded by a lock.
2. `etl.transform.transform_data()` normalizes raw rows into database/model-compatible columns:
   `from_address` to `from_addr`, `to_address` to `to_addr`, `timestamp` to `block_timestamp`, `value_eth` to `value`, `gas_price_gwei` to `gas_price`.
3. `etl.transform.validate_data()` checks required transformed fields.
4. `etl.main_etl.BlockchainETL` creates tables, loads batches into PostgreSQL with `ON CONFLICT (tx_hash) DO NOTHING`, and updates `pipeline_state`.
5. Dashboard requests can also persist transformed scheduled-mode batches in the background through `persist_transactions()`.
6. `etl.storage.persist_transformed_transactions()` is shared storage logic for transformed transaction rows, currently used by Ankr streaming flushes.

## Dashboard/API Flow

- Frontend calls `/api/options`, `/api/health`, `/api/stats`, `/api/model-info`, and transaction endpoints.
- `App.jsx` prefers `/api/transactions/async`, then polls `/api/transactions/job/<job_id>` every 3 seconds until completion or timeout, then falls back to `/api/transactions`.
- `_process_transactions_core()` enforces mutually exclusive modes:
  scheduled mode stops streaming, real-time mode starts streaming when available.
- Scheduled mode tries PostgreSQL cache first, then falls back to live RPC extraction.
- API responses normalize transaction fields for UI display and cap returned transactions to 100.
- Async jobs are stored in PostgreSQL table `api_jobs` when available, with JSON files under `JOB_STORE_DIR` as a local fallback. Completed/error jobs have 10-minute TTL cleanup.
- Health and stats endpoints are deliberately non-blocking and do not call slow initialization.

## ML Pattern

- `BlockchainFraudDetector` loads `MODEL_PATH` if present.
- Training uses synthetic labels when no labels are provided.
- Prediction requires a trained model and scaler; no model returns `None`.
- MCP fraud analysis falls back to `anomaly_detection()` if no trained model is available.
- `AIEnrichedETL.enrich_with_fraud_scores()` runs transform, RandomForest prediction, and anomaly scoring.
- `train_ai_model.py` generates synthetic transactions, trains `fraud_model.pkl`, and emits `fraud_report.json`.

## Streaming Pattern

- `AnkrBlockchainStreamer` polls Ankr HTTP RPC, tracks last seen block, buffers block data, flattens transactions, and transforms buffered batches.
- `StreamingServiceManager` wraps the streamer and exposes initialize/start/stop/stats helpers for API use.
- Streaming is intended to run independently from batch ETL, and dashboard mode switching avoids running both paths at once.
- Current streamer flush path transforms buffered transactions and persists them to PostgreSQL when `STORE_BATCH_RESULTS` is enabled and a database engine is available.

## MCP Pattern

- `src/backend/mcp_server.py` exposes tools for latest block, block details, transaction details, address balance, address transaction count, fraud analysis, and model info.
- It also exposes read-only RPC configuration as MCP resource `config://rpc`.
- `.vscode/mcp.json` points MCP clients at `venv/bin/python src/backend/mcp_server.py` and uses a public RPC default.

## Documentation Pattern

- Root `README.md`, `IMPROVEMENT_PLAN.md`, `roadmap.md`, and `TODO.md` are the most useful root-level docs.
- Many `documentation/` files are historical and reference pre-refactor paths such as `src/ai_dashboard.py`.
- Treat docs as supporting context; verify against source.
