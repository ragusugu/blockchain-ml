#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/docker"

if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD=(docker-compose)
elif docker compose version &> /dev/null; then
    COMPOSE_CMD=(docker compose)
else
    COMPOSE_CMD=()
fi

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Docker Compose Deployment Script    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if [ ${#COMPOSE_CMD[@]} -eq 0 ]; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Install from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker & Docker Compose found${NC}\n"

cd "$DOCKER_DIR"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cat > .env << 'EOF'
POSTGRES_DB=blockchain_db
POSTGRES_USER=blockchain_user
POSTGRES_PASSWORD=change_me_to_secure_password
RPC_URL=https://ethereum.publicnode.com
BATCH_SIZE=10
ETL_SCHEDULE_HOUR=0
ETL_SCHEDULE_MINUTE=0
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please update .env with your RPC_URL and secure password${NC}\n"
fi

# Build images
echo -e "${BLUE}🔨 Building Docker images...${NC}\n"
"${COMPOSE_CMD[@]}" build

echo -e "${GREEN}✅ Build successful${NC}\n"

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}\n"
"${COMPOSE_CMD[@]}" up -d

echo -e "${GREEN}✅ Services started${NC}\n"

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check service status
echo -e "${BLUE}📋 Service Status:${NC}\n"
"${COMPOSE_CMD[@]}" ps

echo -e "\n${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Deployment Complete!                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}\n"

echo -e "${BLUE}🌐 Access the application:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:5000${NC}"
echo -e "   Database: ${BLUE}localhost:5432${NC}\n"

echo -e "${BLUE}📊 View logs:${NC}"
echo -e "   All services:  ${YELLOW}cd docker && ${COMPOSE_CMD[*]} logs -f${NC}"
echo -e "   Backend only:  ${YELLOW}cd docker && ${COMPOSE_CMD[*]} logs -f backend${NC}"
echo -e "   Frontend only: ${YELLOW}cd docker && ${COMPOSE_CMD[*]} logs -f frontend${NC}\n"

echo -e "${BLUE}🛑 To stop services:${NC}"
echo -e "   ${YELLOW}cd docker && ${COMPOSE_CMD[*]} down${NC}\n"

echo -e "${BLUE}🔄 To restart services:${NC}"
echo -e "   ${YELLOW}cd docker && ${COMPOSE_CMD[*]} restart${NC}\n"
