# Known Issues

Last updated: 2026-06-07

## Verified From Current Source

- If PostgreSQL is unavailable and the backend is scaled across multiple Kubernetes pods, async job fallback files are pod-local. Normal multi-worker Gunicorn inside one container is covered by shared filesystem fallback, and DB-backed storage covers multi-pod deployments.
- Public/free RPC endpoints can be slow, rate-limited, or unavailable; dashboard fetch behavior depends heavily on current endpoint health.

## Docs Or Plan Items That May Be Stale

- `IMPROVEMENT_PLAN.md` still lists some already-fixed items: missing imports in `realtime_processor.py` and `stream_service.py`, `ON CONFLICT DO NOTHING` in ETL load, thread-safe extract cache, pytest presence, and Gunicorn usage.
- `IMPROVEMENT_PLAN.md` also still references an already-fixed/stale frontend build issue involving `src/static`; current Vite output is `src/frontend/dist`.
- `.github/copilot-instructions.txt` includes stale details such as WebSocket-style Ankr language, `blockchain_fraud_model.pkl`, and a `fraud_score` database column.
- Many historical files under `documentation/legacy/` and `documentation/archive/` reference older source layout and should be treated as archived context, not current instructions.

## Security And Operations Risks

- Default database credentials are present in config/deployment templates. Replace them with environment-specific secrets for real deployments.
- Provider-style RPC examples remain in documentation as placeholders only. Do not commit or store private provider keys in Memory Bank or docs.
- `.env`, `docker/.env`, and `config/.env` exist locally but were intentionally not read into Memory Bank.
- K8s secret placeholders must be regenerated for production.
- Model artifacts are ignored by git, so deployments need an explicit model creation, mount, or registry strategy.
