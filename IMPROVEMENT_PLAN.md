# Blockchain ML — Improvement Plan

> Generated after full codebase audit. Organized by priority (P0 = Critical, P1 = High, P2 = Medium, P3 = Nice-to-have).

---

## P0 — Critical Bugs & Security

### 1. Dead code / unreachable `return` in `realtime_processor.py`
- **File:** `src/backend/ml/realtime_processor.py` (line ~60)
- **Issue:** Two consecutive `return` statements in `initialize()` — the second `return False` is unreachable.
- **Fix:** Remove the dead `return False`.

### 2. Missing `import os` in `realtime_processor.py`
- **File:** `src/backend/ml/realtime_processor.py` → `_output_csv()` uses `os.path.exists()` but `os` is never imported.
- **Fix:** Add `import os` at the top.

### 3. Missing `import sys` in `stream_service.py`
- **File:** `src/backend/etl/stream_service.py` → `sys.exit(1)` at the bottom without importing `sys`.
- **Fix:** Add `import sys`.

### 4. Hardcoded credentials in default config
- **File:** `src/backend/config.py` — `DATABASE_URL` contains `change-me-to-secure-password` as default.
- **Risk:** If `.env` is missing, production connects with a known password.
- **Fix:** Fail fast if `DATABASE_URL` is not set in production; only use defaults in dev mode.

### 5. Model accuracy hardcoded in frontend
- **File:** `src/frontend/src/App.jsx` (~line 850) — AI model accuracy is hardcoded as `94.5%` and ROC-AUC as `0.982`.
- **Fix:** Expose a `/api/model-info` response that returns actual metrics (already half-implemented on the backend but also hardcoded there). Store metrics alongside the model pickle.

### 6. Pickle-based model serialization
- **File:** `src/backend/ml/ai_fraud_detector.py`
- **Risk:** Pickle is vulnerable to arbitrary code execution if an untrusted model file is loaded.
- **Fix:** Use `joblib` with hash verification or ONNX export. Add integrity check on load.

### 7. Massive code duplication in `ai_dashboard.py`
- **File:** `src/backend/api/ai_dashboard.py` — 1196 lines. The synchronous `/api/transactions` route (line ~700-990) duplicates 90% of `_process_transactions_core()` (line ~200-350).
- **Fix:** Delete the duplicated logic in the sync route and call `_process_transactions_core()` directly, same as the async route already does.

---

## P1 — Architecture & Reliability

### 8. Replace Flask dev server with production WSGI
- **Current:** `app.run(debug=True)` used even in Docker/production.
- **Fix:** Use Gunicorn (`gunicorn -w 4 -b 0.0.0.0:5000 api.ai_dashboard:app`). Update `Dockerfile.backend` CMD and remove `debug=True`.

### 9. Database connection pool leaks
- **File:** `ai_dashboard.py` — `psycopg2.pool.SimpleConnectionPool` is created but if `getconn()` raises before being returned, the connection leaks.
- **Fix:** Wrap pool operations with try/finally. Consider switching to SQLAlchemy's built-in pool (already imported via `connections.py`) to have a single pool strategy.

### 10. Global mutable state in Flask app
- **Files:** `ai_dashboard.py` — uses 15+ module-level globals (`w3`, `etl_ai`, `current_data`, `active_mode`, `jobs`, etc.).
- **Risk:** Race conditions under Gunicorn multi-worker; `jobs` dict won't be shared across workers.
- **Fix:** Move `jobs` to Redis or the database. Wrap shared state in a proper application context or use Flask's `g` / app config.

### 11. No database migrations
- **Current:** Tables created with raw `CREATE TABLE IF NOT EXISTS` in `main_etl.py`.
- **Risk:** Schema changes require manual coordination; no version tracking.
- **Fix:** Add Alembic for SQL migrations. Create initial migration from current schema.

### 12. ETL `load_phase` uses `to_sql` without conflict handling
- **File:** `src/backend/etl/main_etl.py` — `batch.to_sql('transaction_receipts', ...)` with `if_exists='append'` will fail on duplicate `tx_hash` (UNIQUE constraint).
- **Fix:** Use the `ON CONFLICT DO NOTHING` approach already implemented in `persist_transactions()`, or use SQLAlchemy's `insert().on_conflict_do_nothing()`.

### 13. ML model trained on synthetic data only
- **File:** `src/backend/ml/train_ai_model.py` — Model trains exclusively on generated random data.
- **Fix:** Implement a labeled-data pipeline: (a) Collect known fraud addresses from public lists (Etherscan labels, Chainalysis). (b) Build a feature store from real historical transactions. (c) Retrain periodically on real data with proper train/val/test splits.

### 14. Feature extraction uses iterrows (slow)
- **File:** `ai_fraud_detector.py` → `extract_features()` — uses `iterrows()` which is O(n) with Python loop overhead.
- **Fix:** Vectorize feature computation using `pd.DataFrame` operations and `groupby`. This should give 10-50x speedup on datasets > 1k rows.

### 15. Block cache unbounded / not thread-safe
- **File:** `src/backend/etl/extract.py` — `_block_cache` is a plain `dict` with a manual eviction loop; not thread-safe.
- **Fix:** Replace with `functools.lru_cache` or `cachetools.TTLCache` with a lock.

---

## P2 — Code Quality & Testing

### 16. Zero automated tests
- **Current:** `test_etl.py` is a manual interactive script, not pytest-based.
- **Fix:**
  - Add `pytest` + `pytest-cov` to requirements.
  - Write unit tests for `extract.py`, `transform.py`, `ai_fraud_detector.py`.
  - Write integration tests for API routes using Flask's test client.
  - Add a CI/CD pipeline (GitHub Actions) to run tests on every push.

### 17. No type hints in most modules
- **Files:** Most backend files lack function signatures with types.
- **Fix:** Add type annotations progressively. Run `mypy` in CI.

### 18. Frontend Dockerfile ignores Vite build output
- **File:** `docker/Dockerfile.frontend` — Runs `npm run build` in the builder stage but then copies `src/static` instead of the built `dist/` output.
- **Fix:** Copy from the builder stage: `COPY --from=builder /app/frontend/dist /usr/share/nginx/html`.

### 19. App.jsx is a 960-line monolith
- **Fix:** Extract into separate modules:
  - `hooks/useTransactions.js` — all fetch/polling logic
  - `hooks/useAutoRefresh.js` — refresh timer logic  
  - `components/LeftPanel.jsx` — options + config
  - `components/CenterPanel.jsx` — stats + table
  - `components/RightPanel.jsx` — model info + legend
  - Keep `App.jsx` as a thin layout shell.

### 20. No linting or formatting configured
- **Fix:**
  - Backend: Add `ruff` or `flake8` + `black` config.
  - Frontend: Add `eslint` + `prettier` config.
  - Add pre-commit hooks.

### 21. Documentation sprawl
- **Current:** 30+ markdown files across `documentation/`, `documentation/archive/`, root-level `*.md` files, many of which are outdated or redundant.
- **Fix:** Consolidate into 4-5 docs: `README.md`, `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/API.md`, `docs/DEPLOYMENT.md`. Archive the rest.

---

## P3 — Feature Enhancements

### 22. Implement the MCP Server (from TODO.md)
- Connect `web3.py` to an MCP server using `fastmcp`.
- Expose tools: `get_transaction(tx_hash)`, `get_latest_block_number()`, `get_address_balance(addr)`.
- Wire into the AI pipeline for interactive contextual queries.

### 23. Add WebSocket support for real-time streaming
- **Current:** Frontend polls with `setInterval` (10s for realtime, 5min for batch).
- **Fix:** Add Flask-SocketIO or switch to FastAPI with WebSocket support. Push new blocks/transactions to the frontend instantly.

### 24. Add proper alerting & notifications
- Support Discord/Slack/email alerts when fraud is detected above a configurable threshold.
- The webhook plumbing is partially there (`OUTPUT_MODE=webhook`) but not exposed in the UI.

### 25. Add transaction graph analysis
- Use `networkx` to build address interaction graphs.
- Detect known fraud patterns: money laundering loops, fan-out/fan-in, Sybil clusters.
- Add a graph visualization component to the dashboard.

### 26. Add proper API authentication
- **Current:** All API endpoints are unauthenticated.
- **Fix:** Add JWT-based auth or API key middleware for production deployments.

### 27. OpenAPI/Swagger documentation
- Add `flask-restx` or `flasgger` to auto-generate API docs from route annotations.
- This replaces the need for manual API markdown docs.

### 28. Add model versioning & A/B testing
- Track model versions with metadata (training date, dataset size, metrics).
- Support running two models simultaneously and comparing outputs.
- Use MLflow or a lightweight custom registry.

### 29. Add Prometheus metrics & Grafana dashboards
- Expose `/metrics` endpoint with `prometheus_flask_instrumentator` or similar.
- Track: request latency, fraud detection rate, RPC call latency, model inference time.
- Add Grafana dashboard manifests to `k8s/`.

### 30. Multi-chain support
- **Current:** Ethereum only.
- **Fix:** Abstract the chain-specific logic (RPC URLs, value conversion, gas model) behind a `Chain` interface. Support Polygon, BSC, Arbitrum via config.

---

## Implementation Roadmap

| Phase | Items | Est. Effort | Impact |
|-------|-------|-------------|--------|
| **Phase 1** (Week 1-2) | P0 items #1-7 | 2-3 days | Fix bugs, eliminate security risks |
| **Phase 2** (Week 2-4) | P1 items #8-15 | 1-2 weeks | Production-ready architecture |
| **Phase 3** (Week 4-6) | P2 items #16-21 | 1-2 weeks | Developer experience & maintainability |
| **Phase 4** (Week 6+) | P3 items #22-30 | Ongoing | Feature differentiation |

---

## Quick Wins (< 1 hour each)

1. Fix dead code & missing imports (#1, #2, #3)
2. Delete duplicated sync route logic (#7)
3. Fix Dockerfile.frontend to use Vite build output (#18)
4. Add `gunicorn` to `requirements.txt` and update Docker CMD (#8)
5. Add `.env.example` with all documented variables
6. Add `ruff.toml` for Python linting (#20)
