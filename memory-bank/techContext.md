# Technical Context

Last updated: 2026-06-04

## Stack

- Backend: Python 3, Flask, Flask-CORS, Web3.py, pandas, NumPy, SQLAlchemy, psycopg2, cachetools.
- ML: scikit-learn RandomForestClassifier, IsolationForest, StandardScaler, joblib model persistence.
- MCP: FastMCP in `src/backend/mcp_server.py`.
- Frontend: React 18, Vite, Material UI, axios, framer-motion, lucide-react, recharts.
- Storage: PostgreSQL table `transaction_receipts` plus `pipeline_state`.
- Deployment: Docker Compose in `docker/docker-compose.yml`; Kubernetes manifests in `k8s/`.

## Important Environment Variables

- `RPC_URL`: primary Ethereum RPC URL; can contain comma-separated candidates.
- `ANKR_RPC_URL`: RPC URL for the optional Ankr streaming service.
- `DATABASE_URL`: SQLAlchemy/PostgreSQL connection string.
- `BATCH_SIZE`, `MAX_WORKERS`: ETL batching and parallel extraction.
- `MODEL_ENABLED`, `MODEL_PATH`, `FRAUD_THRESHOLD`, `TRAIN_MODEL_ON_BATCH`: ML behavior.
- `MAX_BLOCKS_PER_REQUEST`, `STORE_BATCH_RESULTS`: dashboard/API processing limits and persistence.
- `JOB_STORE_DIR`: filesystem fallback directory for async API job JSON files.
- `POLLING_INTERVAL`, `ANKR_POLLING_INTERVAL`, `ANKR_BATCH_SIZE`, `STREAMING_ENABLED`: real-time and Ankr polling behavior.
- `ETL_SCHEDULE_HOUR`, `ETL_SCHEDULE_MINUTE`: scheduler timing.

## Common Commands

- Run tests with local venv: `./venv/bin/pytest`
- System Python test command currently unavailable: `python3 -m pytest`
- Start both dev services: `./start.sh`
- Start frontend only: `cd src/frontend && npm run dev`
- Build frontend: `cd src/frontend && npm run build`
- Backend dev server from `src/backend`: `python3 -m flask run --host=0.0.0.0 --port=5000`
- Backend direct module from `src/backend`: `python3 api/ai_dashboard.py`
- Production backend command in Docker: `gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 api.ai_dashboard:app`
- Docker Compose from current layout: `cd docker && docker-compose up -d`
- Optional streaming profile from current layout: `cd docker && docker-compose --profile streaming up -d`
- Deployment menu script: `bash scripts/deployment/deploy.sh`
- Verify Docker/K8s setup files: `bash scripts/deployment/verify-setup.sh`
- MCP server stdio from `src/backend`: `python3 -m mcp_server`
- MCP server SSE from `src/backend`: `python3 -m mcp_server --sse --port 8000`

## Notes

- Current shell check showed Python 3.12.3, Node v24.12.0, and npm 11.6.2. `pytest` and `python3 -m pip` were unavailable in this environment on 2026-06-04.
- Local `venv/` exists and includes `pip`, `pytest`, `flask`, `fastmcp`, and related tools.
- `.gitignore` ignores `.env`, `venv/`, Python caches, node/build caches, `*.pkl`, `fraud_model.pkl`, logs, and sqlite/db files.
- `.env.example` documents public RPC defaults and placeholder provider-key URLs.
- `start.sh` sets default environment variables and starts Flask plus Vite. Review its default RPC configuration before sharing or committing credential-like values.
- `scripts/start_dashboard.sh` and `scripts/ai_start.sh` reference older `src/...` paths and may be stale compared with the current `src/backend/...` layout.
- Docker backend copies `src/backend` to `/app` and sets `PYTHONPATH=/app`.
- Frontend build output is `src/frontend/dist`, which matches Flask static hosting and `docker/Dockerfile.frontend`.
- Docker/Kubernetes helper scripts now calculate the repo root from their own location instead of assuming the caller's current directory.
