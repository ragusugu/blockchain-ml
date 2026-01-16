#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Deployment Selection Menu           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

echo -e "${YELLOW}Choose deployment method:${NC}\n"
echo "1) Docker Compose (Single server, simpler)"
echo "2) Kubernetes (Multi-server, scalable)"
echo "3) View deployment documentation"
echo "4) Exit"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}Starting Docker Compose deployment...${NC}\n"
        bash scripts/deployment/deploy-docker.sh
        ;;
    2)
        echo -e "${BLUE}Starting Kubernetes deployment...${NC}\n"
        bash scripts/deployment/deploy-kubernetes.sh
        ;;
    3)
        echo -e "${BLUE}Opening documentation...${NC}\n"
        cat documentation/guides/DEPLOYMENT_GUIDE.md 2>/dev/null || echo "Documentation not found"
        ;;
    4)
        echo -e "${YELLOW}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
