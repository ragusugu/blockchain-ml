# Known Issues

Last updated: 2026-06-04

## Verified From Current Source

- Several helper scripts reference old pre-refactor files such as `src/main_etl.py`, `src/realtime_processor.py`, `src/ai_dashboard.py`, and `src/train_ai_model.py`.
- Root `README.md` links to `docs/...`, while the current documentation directory is `documentation/`.
- `DetailModal.jsx` expects fields such as `fraud_score`, `timestamp`, and `gas_price`; the currently rendered detail UI is `TransactionDetailsPanel.jsx`.
- If PostgreSQL is unavailable and the backend is scaled across multiple Kubernetes pods, async job fallback files are pod-local. Normal multi-worker Gunicorn inside one container is covered by shared filesystem fallback, and DB-backed storage covers multi-pod deployments.
- Public/free RPC endpoints can be slow, rate-limited, or unavailable; dashboard fetch behavior depends heavily on current endpoint health.

## Docs Or Plan Items That May Be Stale

- `IMPROVEMENT_PLAN.md` still lists some already-fixed items: missing imports in `realtime_processor.py` and `stream_service.py`, `ON CONFLICT DO NOTHING` in ETL load, thread-safe extract cache, pytest presence, and Gunicorn usage.
- `.github/copilot-instructions.txt` includes stale details such as WebSocket-style Ankr language, `blockchain_fraud_model.pkl`, and a `fraud_score` database column.
- Many files under `documentation/` reference older source layout and should be checked against `src/backend` and `src/frontend` before use.

## Security And Operations Risks

- Default database credentials are present in config/deployment templates. Replace them with environment-specific secrets for real deployments.
- Provider-style RPC defaults appear in startup/config paths. Do not commit or store private provider keys in Memory Bank or docs.
- `.env`, `docker/.env`, and `config/.env` exist locally but were intentionally not read into Memory Bank.
- K8s secret placeholders must be regenerated for production.
- Model artifacts are ignored by git, so deployments need an explicit model creation, mount, or registry strategy.
