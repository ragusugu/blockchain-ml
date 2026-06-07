# Dashboard Guide

The dashboard is a Vite React app backed by the Flask API in `src/backend/api/ai_dashboard.py`.

## Run Locally

From the repository root:

```bash
./start.sh
```

This starts:

- Flask API on `http://localhost:5000`
- Vite frontend on `http://localhost:3000`

For separate terminals:

```bash
cd src/backend
python3 api/ai_dashboard.py
```

```bash
cd src/frontend
npm run dev
```

## Dashboard Flow

1. Choose scheduled or real-time mode.
2. Select a processing option or block count.
3. Fetch transactions through `/api/transactions/async`.
4. Poll `/api/transactions/job/<job_id>` until the job completes.
5. Review summary metrics, the transaction table, and transaction details.

The frontend falls back to the synchronous `/api/transactions` endpoint if async processing is unavailable.

## Important Frontend Files

| File | Purpose |
|------|---------|
| `src/frontend/src/App.jsx` | Main dashboard state and API flow |
| `src/frontend/src/main.jsx` | React entrypoint and Material UI theme |
| `src/frontend/src/hooks/useStreamingData.js` | Streaming/system status polling hooks |
| `src/frontend/src/components/ModeSelector.jsx` | Scheduled vs real-time entry view |
| `src/frontend/src/components/TransactionTable.jsx` | Paginated transaction list |
| `src/frontend/src/components/TransactionDetailsPanel.jsx` | Active transaction details panel |
| `src/frontend/src/components/StreamingStatus.jsx` | Streaming and system status cards |

## Important Backend Endpoints

```text
GET  /api/options
GET  /api/health
GET  /api/stats
GET  /api/model-info
POST /api/model-toggle
POST /api/transactions/async
GET  /api/transactions/job/<job_id>
POST /api/transactions
GET  /api/transaction/<tx_hash>
GET  /api/streaming/stats
GET  /api/streaming/health
GET  /api/system/status
```

## Build For Production

```bash
cd src/frontend
npm run build
```

The generated assets are written to `src/frontend/dist`. The Flask app serves that directory for local production-style runs, and the frontend Docker image copies the same directory into nginx.

## Troubleshooting

| Issue | First Check |
|-------|-------------|
| Frontend cannot reach API | Confirm Flask is running on `http://localhost:5000` |
| RPC connection failed | See `documentation/guides/RPC_CONNECTION_FIX.md` |
| No transactions are returned | Try fewer blocks and verify the RPC endpoint |
| Model info says no model loaded | Train or mount a model artifact configured by `MODEL_PATH` |
| Streaming status unavailable | Confirm `STREAMING_ENABLED` and `ANKR_RPC_URL` settings |

## Verification

```bash
./venv/bin/pytest
cd src/frontend && npm run build
PYTHONPATH=src/backend ./venv/bin/python -c "import api.ai_dashboard; print('ai_dashboard import ok')"
```
