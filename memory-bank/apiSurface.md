# API Surface

Last updated: 2026-06-04

## Flask App

- Main app file: `src/backend/api/ai_dashboard.py`.
- Flask static folder points at `src/frontend/dist`.
- CORS is enabled.
- The app initializes a global `BlockchainFraudDetector`, optional database engine, and optional streaming service manager.

## Health And Status

- `GET /health`: lightweight container health check with service status, model status, and timestamp.
- `GET /ready`: readiness check; returns 503 when the database engine is unavailable or unhealthy.
- `GET /api/health`: dashboard health payload with system stats, model readiness, optional database status, and uptime.
- `GET /api/stats`: non-blocking dashboard statistics from PostgreSQL when available, otherwise defaults.
- `GET /api/performance`: process and model performance stats.
- `GET /api/system/status`: streaming-oriented system status, including DB/model/RPC/streaming fields.

## Options And Transactions

- `GET /api/options`: returns block-count presets used by the UI, filtered by `MAX_BLOCKS_PER_REQUEST`.
- `POST /api/transactions/async`: creates a background transaction-processing job stored in PostgreSQL when available, otherwise `JOB_STORE_DIR`.
- `GET /api/transactions/job/<job_id>`: polls async job state and result.
- `POST /api/transactions`: synchronous transaction processing path.
- `GET /api/transaction/<tx_hash>`: transaction detail lookup from PostgreSQL cache first, then RPC fallback.

## Model And Streaming

- `POST /api/model-toggle`: enables/disables model use in the dashboard process.
- `GET /api/model-info`: returns model availability, path, metrics, feature importance, and config.
- `GET /api/streaming/stats`: streaming manager stats or disabled/unavailable response.
- `GET /api/streaming/health`: streaming manager health when available.

## Transaction Processing Behavior

- Request body supports `option`, `blocks`, and `mode`.
- `option` maps to presets from `PROCESSING_OPTIONS`; `blocks` is clamped by `MAX_BLOCKS_PER_REQUEST`.
- Mode aliases are normalized to `scheduled` or `realtime`.
- Real-time mode starts the streaming service if available and uses live RPC extraction for the requested block range.
- Scheduled mode stops streaming, tries PostgreSQL cache first, then falls back to live extraction.
- Responses include transactions, summary stats, processing time, model status, data source, mode info, and optional streaming status.
- Returned transaction arrays are capped at 100 records for the dashboard.
- Async job data is shared through PostgreSQL when available, so Gunicorn workers can poll the same job state. Filesystem fallback is intended for local/dev use.

## Frontend Calls

- `src/frontend/src/App.jsx` calls `/api/options`, `/api/health`, `/api/stats`, `/api/model-info`, `/api/transactions/async`, `/api/transactions/job/<job_id>`, `/api/transactions`, and `/api/model-toggle`.
- `src/frontend/src/hooks/useStreamingData.js` polls `/api/streaming/stats`, `/api/system/status`, and `/api/streaming/health`.
- The Vite dev server proxies `/api` to `http://localhost:5000`.

## MCP Tools

- Server file: `src/backend/mcp_server.py`.
- Tools: `get_latest_block`, `get_block_details`, `get_transaction_details`, `get_address_balance`, `get_address_transaction_count`, `analyze_transaction_fraud`, and `get_model_info`.
- Resource: `config://rpc`.
- Stdio and SSE modes are supported through CLI flags.
