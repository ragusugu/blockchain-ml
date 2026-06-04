# Deployment Notes

Last updated: 2026-06-04

## Local Development

- `./start.sh` starts the Flask API from `src/backend` and Vite from `src/frontend`.
- The script also attempts to kill existing processes on ports 5000, 3000, and 5173.
- `start.sh` exports local defaults for RPC, database, model, and streaming settings; review these before sharing logs or configs.
- Frontend dev URL is usually `http://localhost:5173`; backend URL is `http://localhost:5000`.
- Vite proxies `/api` to the Flask backend in development.

## Docker Compose

- Compose file lives at `docker/docker-compose.yml`.
- From repo root, use `bash scripts/deployment/deploy-docker.sh` or `cd docker && docker-compose up -d`.
- Services: `postgres`, `backend`, `frontend`, `ml_worker`, `scheduler`, and optional `ankr-streamer`.
- Compose uses named volumes for Postgres data and model cache.
- Backend image uses Gunicorn with 4 workers.
- Frontend image serves nginx on port `3000` and proxies `/api/` to backend.
- Optional streaming is behind the Compose `streaming` profile.

## Kubernetes

- Manifests live in `k8s/` and include namespace, ConfigMap, Secret, storage, Postgres StatefulSet, backend/frontend/worker deployments, scheduler CronJob, ingress, and deploy helper.
- `k8s/03-secrets.yaml` contains default credentials/placeholders and must be replaced for real deployments.
- `k8s/09-scheduler-cronjob.yaml` defaults to midnight. `scripts/deployment/deploy-kubernetes.sh` patches its schedule from `ETL_SCHEDULE_HOUR` and `ETL_SCHEDULE_MINUTE`.
- Ingress routes `/api`, `/health`, and `/ready` to backend, and `/` to frontend.

## Deployment Scripts

- `scripts/deployment/deploy.sh` is a menu wrapper around Docker/Kubernetes helpers.
- `scripts/deployment/deploy-docker.sh`, `cleanup-docker.sh`, and `verify-setup.sh` now calculate the repo root and use the current `docker/` layout.
- `scripts/deployment/deploy-kubernetes.sh` now builds all images from the repo root with Dockerfiles under `docker/`, applies generated ConfigMap/Secret resources without mutating tracked YAML, applies all current manifests, and patches the CronJob schedule from env values.
- `scripts/deployment/complete-deployment.sh` syntax-checks successfully as of 2026-06-04, but it is broader/destructive and should still be reviewed before use.

## Frontend Build Alignment

- Flask static hosting expects `src/frontend/dist`.
- `docker/Dockerfile.frontend` builds in `/app/frontend` and copies `/app/frontend/dist` to nginx.
- `src/frontend/vite.config.js` now sets `build.outDir` to `dist`.
- `npm run build` from `src/frontend` passed on 2026-06-04 and emitted `dist/`.
- Vite currently reports a large-chunk warning for the main JS bundle; this is an optimization opportunity, not a build failure.
