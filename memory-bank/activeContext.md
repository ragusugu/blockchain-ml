# Active Context

Last updated: 2026-06-04

## Current Focus

- Memory Bank has been refreshed after a full codebase scan.
- Current app center of gravity is the dual-mode dashboard: scheduled/batch transaction analysis plus real-time/Ankr streaming status.
- Frontend production build output, model loading, async job storage, streaming persistence, model metric contract, main deployment path assumptions, stale active helper scripts, README links, DetailModal compatibility, and Kubernetes CronJob behavior have been fixed.
- The most valuable next engineering work is verifying the full dashboard happy path against live services, deciding the model artifact strategy, and replacing placeholder database credentials before real deployment.

## Recent Decisions

- Use `memory-bank/` at the repository root for durable project context.
- Add `AGENTS.md` so future Codex sessions are instructed to read and update the Memory Bank.
- Add a reusable global Codex skill at `~/.codex/skills/memory-bank` for reading, creating, and maintaining memory-bank files across projects.
- Add deeper memory files after full scan:
  `codebaseMap.md`, `apiSurface.md`, `deploymentNotes.md`, and `knownIssues.md`.
- Align Vite output to `src/frontend/dist` so Flask static serving and `docker/Dockerfile.frontend` use the same artifact path.
- Treat empty/corrupt fraud model files as "no model loaded" instead of crashing on startup or tests.
- Store async API transaction jobs in PostgreSQL table `api_jobs` when available, with JSON files under `JOB_STORE_DIR` as a local fallback.
- Persist Ankr streaming flushes through shared `etl.storage.persist_transformed_transactions()`.
- Keep deployment helpers rooted at the actual repo layout: Compose under `docker/`, Dockerfiles under `docker/`, manifests under `k8s/`.
- Return numeric model metrics from `/api/model-info` and keep frontend parsing tolerant of old formatted strings.
- Update active helper scripts to the current `src/backend` layout and remove provider-style RPC defaults from startup scripts.
- Make the Kubernetes CronJob run one ETL pass through `processing.scheduler.run_etl()` instead of starting the blocking scheduler inside each job.
- Update README links from removed `docs/` paths to current `documentation/` paths.
- Make `DetailModal.jsx` tolerate the current transaction field contract even though `TransactionDetailsPanel.jsx` is the active UI.

## Open Questions

- Whether model artifacts such as `fraud_model.pkl` should be generated locally, stored in the Docker `models_cache` volume, mounted at `/app/models`, or managed by a model registry.
- Whether PostgreSQL is required for normal dashboard use or only for scheduled-mode cache/persistence. Current API can fetch live RPC data without cache, but scheduled-mode persistence and ETL require PostgreSQL.
- Whether historical docs under `documentation/legacy/` and `documentation/archive/` should be updated, archived as-is, or removed.

## Next Useful Work

- Verify dashboard happy path with a local backend/frontend run.
- Confirm model loading and no-model fallback behavior in API endpoints.
- Replace placeholder/default database credentials before any real deployment.
- Decide whether to update or archive historical docs that still describe pre-refactor paths.
- Consider frontend code-splitting or manual chunks; Vite production build passes but warns about the main JS bundle size.
