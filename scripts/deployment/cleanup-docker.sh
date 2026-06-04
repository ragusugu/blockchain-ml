#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/docker"

if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD=(docker-compose)
elif docker compose version &> /dev/null; then
    COMPOSE_CMD=(docker compose)
else
    echo "❌ Docker Compose is not installed"
    exit 1
fi

# Stop all Docker containers and remove volumes
echo "🛑 Stopping Docker Compose services..."
cd "$DOCKER_DIR"
"${COMPOSE_CMD[@]}" down -v

echo "✅ Cleanup complete"
