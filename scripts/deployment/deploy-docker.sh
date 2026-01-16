#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Install from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker & Docker Compose found${NC}\n"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cat > .env << 'EOF'
POSTGRES_DB=blockchain_db
POSTGRES_USER=blockchain_user
POSTGRES_PASSWORD=change_me_to_secure_password
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
BATCH_SIZE=10
ETL_SCHEDULE_HOUR=0
ETL_SCHEDULE_MINUTE=0
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please update .env with your RPC_URL and secure password${NC}\n"
fi

# Build images
echo -e "${BLUE}🔨 Building Docker images...${NC}\n"
docker-compose build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful${NC}\n"

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}\n"
docker-compose up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start services${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Services started${NC}\n"

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check service status
echo -e "${BLUE}📋 Service Status:${NC}\n"
docker-compose ps

echo -e "\n${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Deployment Complete!                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}\n"

echo -e "${BLUE}🌐 Access the application:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:5000${NC}"
echo -e "   Database: ${BLUE}localhost:5432${NC}\n"

echo -e "${BLUE}📊 View logs:${NC}"
echo -e "   All services:  ${YELLOW}docker-compose logs -f${NC}"
echo -e "   Backend only:  ${YELLOW}docker-compose logs -f backend${NC}"
echo -e "   Frontend only: ${YELLOW}docker-compose logs -f frontend${NC}\n"

echo -e "${BLUE}🛑 To stop services:${NC}"
echo -e "   ${YELLOW}docker-compose down${NC}\n"

echo -e "${BLUE}🔄 To restart services:${NC}"
echo -e "   ${YELLOW}docker-compose restart${NC}\n"
