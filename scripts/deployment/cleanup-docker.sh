#!/bin/bash

# Stop all Docker containers and remove volumes
echo "🛑 Stopping Docker Compose services..."
docker-compose down -v

echo "✅ Cleanup complete"
