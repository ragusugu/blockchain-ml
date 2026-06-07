# Quick Reference

## Launch The Dashboard

```bash
cd /home/sugangokul/Desktop/blockchain-ml
./start.sh
```

- Frontend dev server: `http://localhost:3000`
- Backend API: `http://localhost:5000`
- Docker frontend: `http://localhost:3000`

## Important Files

| Path | Purpose |
|------|---------|
| `src/backend/api/ai_dashboard.py` | Flask dashboard API and static frontend host |
| `src/backend/etl/` | Extract, transform, load, storage, and streaming helpers |
| `src/backend/ml/` | Fraud detector, model training, and real-time processor |
| `src/backend/mcp_server.py` | MCP tools for blockchain and fraud analysis |
| `src/frontend/src/App.jsx` | Main React dashboard state container |
| `src/frontend/src/components/` | Dashboard UI components |
| `src/frontend/vite.config.js` | Vite dev proxy and `dist` build output |
| `tests/` | Backend unit tests |

## Common Commands

```bash
# Run backend tests
./venv/bin/pytest

# Start both local dev services
./start.sh

# Start frontend only
cd src/frontend && npm run dev

# Build frontend
cd src/frontend && npm run build

# Start backend directly
cd src/backend && python3 api/ai_dashboard.py

# Verify deployment files
bash scripts/deployment/verify-setup.sh
```

## API Endpoints

```text
GET  /api/options
GET  /api/health
GET  /api/stats
GET  /api/model-info
POST /api/transactions/async
GET  /api/transactions/job/<job_id>
POST /api/transactions
GET  /api/transaction/<tx_hash>
GET  /api/streaming/stats
GET  /api/system/status
```

## Deployment

```bash
# Docker Compose
bash scripts/deployment/deploy-docker.sh

# Kubernetes
bash scripts/deployment/deploy-kubernetes.sh

# Interactive deployment menu
bash scripts/deployment/deploy.sh
```

## Troubleshooting

| Issue | First Check |
|-------|-------------|
| RPC connection failed | `documentation/guides/RPC_CONNECTION_FIX.md` |
| Tests do not run with system Python | Use `./venv/bin/pytest` |
| Frontend API calls fail | Confirm backend is on `http://localhost:5000` |
| Build output missing | Run `npm run build` from `src/frontend` |
| Docker services stale | Run `bash scripts/deployment/cleanup-docker.sh` |
