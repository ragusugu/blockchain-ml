#!/bin/bash

# Ankr Streaming Setup & Quick Reference
# =====================================

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   ANKR STREAMING - QUICK SETUP & REFERENCE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"

# Function to display section
show_section() {
    echo -e "${YELLOW}$1${NC}"
    echo "───────────────────────────────────────────────────────"
}

# Function to show command
show_command() {
    echo -e "${GREEN}$1${NC}"
}

# ======================== SETUP STEPS ========================
show_section "1️⃣  SETUP STEPS"

echo "Step 1: Update .env file with Ankr configuration"
show_command "  ANKR_RPC_URL=https://rpc.ankr.com/eth"
show_command "  ANKR_POLLING_INTERVAL=12"
show_command "  ANKR_BATCH_SIZE=10"
show_command "  STREAMING_ENABLED=true"

echo ""
echo "Step 2: Start services with streaming"
show_command "  docker-compose --profile streaming up -d"

echo ""
echo "Step 3: Verify streaming is running"
show_command "  docker-compose logs -f ankr-streamer"

echo ""

# ======================== COMMANDS ========================
show_section "2️⃣  COMMON COMMANDS"

echo "Start everything (batch + streaming):"
show_command "  docker-compose --profile streaming up -d"

echo ""
echo "Start only batch (original setup, NO streaming):"
show_command "  docker-compose up -d"

echo ""
echo "View streaming logs:"
show_command "  docker-compose logs -f ankr-streamer"

echo ""
echo "Check all services status:"
show_command "  docker-compose ps"

echo ""
echo "Stop streaming (keep batch running):"
show_command "  docker-compose stop ankr-streamer"

echo ""
echo "Stop everything:"
show_command "  docker-compose down"

echo ""
echo "View streaming statistics:"
show_command "  docker-compose logs ankr-streamer | grep '📊'"

echo ""

# ======================== WHAT'S RUNNING ========================
show_section "3️⃣  WHAT'S RUNNING"

echo "WITHOUT --profile streaming (default):"
echo "  ✅ Backend API (port 5000)"
echo "  ✅ Frontend (port 3000)"
echo "  ✅ PostgreSQL (port 5432)"
echo "  ✅ Scheduler - Batch ETL (original)"
echo "  ✅ ML Worker"
echo "  ❌ Ankr Streamer (disabled)"

echo ""
echo "WITH --profile streaming:"
echo "  ✅ Backend API (port 5000)"
echo "  ✅ Frontend (port 3000)"
echo "  ✅ PostgreSQL (port 5432)"
echo "  ✅ Scheduler - Batch ETL (original)"
echo "  ✅ ML Worker"
echo "  ✅ Ankr Streamer (ENABLED - NEW)"

echo ""

# ======================== ENVIRONMENT VARIABLES ========================
show_section "4️⃣  ENVIRONMENT VARIABLES"

echo "Ankr Streamer Configuration:"
echo "  ANKR_RPC_URL              Free Ankr endpoint (no key needed)"
echo "  ANKR_POLLING_INTERVAL     Seconds between polls (default: 12)"
echo "  ANKR_BATCH_SIZE           Blocks per batch (default: 10)"
echo "  STREAMING_ENABLED         Enable/disable (default: true)"

echo ""
echo "Batch Processing Configuration (unchanged):"
echo "  RPC_URL                   Your RPC endpoint for batch"
echo "  DATABASE_URL              PostgreSQL connection"
echo "  ETL_SCHEDULE_HOUR         When to run batch"
echo "  ETL_SCHEDULE_MINUTE       When to run batch"

echo ""

# ======================== FEATURES ========================
show_section "5️⃣  FEATURES"

echo "✅ Real-time Block Streaming"
echo "   • Blocks streamed as soon as they're mined"
echo "   • ~1 block per 12 seconds on Ethereum"

echo ""
echo "✅ Free Service"
echo "   • Uses Ankr's free RPC (no cost, no API key)"
echo "   • Unlimited requests"

echo ""
echo "✅ Independent from Batch"
echo "   • Streaming doesn't affect batch ETL"
echo "   • Both can run simultaneously"
echo "   • Different RPC endpoints possible"

echo ""
echo "✅ Automatic Buffering"
echo "   • Batches blocks for efficient DB writes"
echo "   • Configurable batch size"

echo ""
echo "✅ Error Handling"
echo "   • Automatic retries on connection failure"
echo "   • Graceful degradation"

echo ""
echo "✅ Monitoring"
echo "   • Real-time statistics"
echo "   • Block and transaction counts"
echo "   • Error tracking"

echo ""

# ======================== FILE LOCATIONS ========================
show_section "6️⃣  NEW FILES CREATED"

echo "Core Modules:"
echo "  📄 src/backend/etl/ankr_streamer.py"
echo "     └─ Main Ankr streaming engine"

echo ""
echo "  📄 src/backend/etl/streaming_manager.py"
echo "     └─ Service manager and lifecycle"

echo ""
echo "  📄 src/backend/etl/stream_service.py"
echo "     └─ Standalone service entry point"

echo ""
echo "Configuration:"
echo "  📄 docker/docker-compose.yml"
echo "     └─ Updated with optional ankr-streamer service"

echo ""
echo "Documentation:"
echo "  📄 documentation/guides/ANKR_STREAMING_SETUP.md"
echo "     └─ Complete setup guide"

echo ""

# ======================== TROUBLESHOOTING ========================
show_section "7️⃣  TROUBLESHOOTING"

echo "Problem: Streaming not starting"
show_command "  Solution: docker-compose logs ankr-streamer"

echo ""
echo "Problem: Connection refused"
show_command "  Solution: Check internet, verify Ankr is accessible"

echo ""
echo "Problem: High memory usage"
show_command "  Solution: Reduce ANKR_BATCH_SIZE or increase ANKR_POLLING_INTERVAL"

echo ""
echo "Problem: Missing modules"
show_command "  Solution: Rebuild Docker image: docker-compose build"

echo ""

# ======================== QUICK START ========================
show_section "8️⃣  QUICK START (30 SECONDS)"

echo ""
echo "1️⃣  Update .env (add Ankr settings - see example above)"
echo ""
echo "2️⃣  Start with streaming:"
show_command "  cd /path/to/blockchain-ml"
show_command "  docker-compose --profile streaming up -d"
echo ""
echo "3️⃣  Wait 10 seconds and check logs:"
show_command "  docker-compose logs ankr-streamer"
echo ""
echo "4️⃣  Done! Streaming is running 🎉"
echo ""

# ======================== VERIFICATION ========================
show_section "9️⃣  VERIFY SETUP"

echo "Check services running:"
show_command "  docker-compose ps"

echo ""
echo "Check streaming logs for success:"
show_command "  docker-compose logs ankr-streamer | grep '✅'"

echo ""
echo "Check batch still works:"
show_command "  docker-compose logs scheduler"

echo ""

# ======================== NEXT STEPS ========================
show_section "🔟 NEXT STEPS"

echo "1. 📝 Update .env with Ankr settings"
echo "2. 🚀 Start with: docker-compose --profile streaming up -d"
echo "3. 👀 Monitor: docker-compose logs -f ankr-streamer"
echo "4. 📊 View stats: docker-compose logs ankr-streamer | grep 📊"
echo "5. 🔗 Integrate into your application"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Ankr Streaming is ready to use!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
