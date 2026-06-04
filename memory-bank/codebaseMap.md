# Codebase Map

Last updated: 2026-06-04

## Backend Source

- `src/backend/config.py`: singleton `cfg`; all major env vars and RPC fallback list.
- `src/backend/connections.py`: cached `get_web3()`, `get_db_engine()`, and `reset_connections()`.
- `src/backend/logging_config.py`: app logging setup.
- `src/backend/api/ai_dashboard.py`: Flask app, async job endpoints, transaction processing core, PostgreSQL cache/persist helpers, model toggle, health/status/streaming routes, static frontend serving.
- `src/backend/mcp_server.py`: FastMCP server exposing blockchain query tools, fraud analysis, model info, and `config://rpc`.

## ETL

- `src/backend/etl/extract.py`: Web3 block and receipt extraction, parallel block extraction, 5-minute TTL block cache.
- `src/backend/etl/transform.py`: Pandas normalization, type casting, null handling, DB-compatible column renames, validation.
- `src/backend/etl/main_etl.py`: `BlockchainETL` orchestration, table creation, batch load with `ON CONFLICT (tx_hash) DO NOTHING`, `pipeline_state`.
- `src/backend/etl/storage.py`: shared transformed-transaction persistence helper with table creation and `ON CONFLICT (tx_hash) DO NOTHING`.
- `src/backend/etl/ankr_streamer.py`: HTTP polling streamer for Ankr RPC, block buffering, transaction flattening, transform-on-flush.
- `src/backend/etl/streaming_manager.py`: singleton lifecycle wrapper around `AnkrBlockchainStreamer`.
- `src/backend/etl/stream_service.py`: standalone streaming service with signal handling.

## ML

- `src/backend/ml/ai_fraud_detector.py`: feature extraction, RandomForest training/prediction, IsolationForest anomaly detection, joblib model persistence, report generation.
- `src/backend/ml/ai_integration.py`: three integration styles: after-transform enrichment, before-load filtering, and parallel analysis.
- `src/backend/ml/realtime_processor.py`: continuous polling processor with output modes `console`, `json`, `csv`, `webhook`.
- `src/backend/ml/train_ai_model.py`: synthetic transaction generation, model training, feature importance, anomaly check, report output.

## Processing And Utilities

- `src/backend/processing/scheduler.py`: APScheduler daily ETL runner plus startup run.
- `src/backend/processing/test_etl.py`: live/manual ETL validation script; depends on real RPC and optionally DB.
- `src/backend/utils/disk_cleanup.py`: disk usage monitor, old file cleanup, Docker prune, background monitor.

## Frontend

- `src/frontend/src/App.jsx`: main state container; mode selection, options, async transaction fetching, fallback sync fetch, auto-refresh, model toggle, metrics, table/detail layout.
- `src/frontend/src/main.jsx`: Material UI dark theme and `ErrorBoundary` wrapper.
- `src/frontend/src/hooks/useStreamingData.js`: polling hooks for `/api/streaming/stats`, `/api/system/status`, and `/api/streaming/health`.
- `src/frontend/src/components/ModeSelector.jsx`: initial scheduled vs real-time selection view.
- `src/frontend/src/components/OptionCard.jsx`: processing option card.
- `src/frontend/src/components/TransactionTable.jsx`: paginated transactions table with copy and Etherscan actions.
- `src/frontend/src/components/TransactionDetailsPanel.jsx`: active right-side transaction details drawer.
- `src/frontend/src/components/DetailModal.jsx`: older modal-style details component; currently imported but not rendered by `App.jsx`.
- `src/frontend/src/components/StreamingStatus.jsx`: live system status cards.
- `src/frontend/src/components/Header.jsx`, `StatCard.jsx`, `ErrorBoundary.jsx`: shell/status/presentation components.
- `src/frontend/vite.config.js`: dev proxy and build output config.

## Tests

- `tests/test_config.py`: config smoke tests and default credential warning.
- `tests/test_transform.py`: transform and validation unit tests.
- `tests/test_fraud_detector.py`: feature extraction, train/predict, joblib roundtrip, anomaly detection.

## Scripts

- `start.sh`: one-command local dev startup for Flask and Vite.
- `scripts/start_react.sh`: frontend-only Vite startup.
- `scripts/start_dashboard.sh`, `scripts/install.sh`, `scripts/realtime_start.sh`, `scripts/ai_start.sh`: older/pre-refactor helper scripts; verify before use.
- `scripts/setup_ankr_streaming.sh`: Ankr streaming setup/reference output.
- `scripts/test_ankr_streaming.py`: live Ankr connectivity and streaming-manager test script.
- `scripts/keep_ports_alive.sh`: restarts Kubernetes port-forward processes.
- `scripts/deployment/*.sh`: deployment menu, Docker/K8s helpers, cleanup, quick references, and larger complete-deployment flow.

## Infrastructure

- `docker/docker-compose.yml`: postgres, backend, frontend, ml_worker, scheduler, optional `ankr-streamer` profile.
- `docker/Dockerfile.backend`: Python/Gunicorn Flask image.
- `docker/Dockerfile.frontend`: Node build plus nginx serving.
- `docker/Dockerfile.worker`: runs `ml/realtime_processor.py`.
- `docker/Dockerfile.scheduler`: runs `processing/scheduler.py`.
- `docker/nginx.conf`: serves frontend and proxies `/api/` to backend.
- `k8s/`: namespace, configmap, secret, storage, Postgres StatefulSet, backend/frontend/worker deployments, scheduler CronJob, ingress.

## Docs And Metadata

- `README.md`: main overview but contains stale `docs/...` links and some path drift.
- `IMPROVEMENT_PLAN.md`: older audit; some items already fixed, some still valid.
- `roadmap.md`: broad architecture/roadmap; useful but some line counts and bug status may be stale.
- `TODO.md`: MCP server task marked complete.
- `.github/copilot-instructions.txt`: rich project guide but contains several stale details.
- `.vscode/mcp.json`: local MCP config for this project.
