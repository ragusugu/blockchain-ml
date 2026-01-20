#!/bin/bash
# One-Command Startup Script for Blockchain ML
# Starts both frontend and backend automatically

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$WORKSPACE_ROOT/src/backend"
FRONTEND_DIR="$WORKSPACE_ROOT/src/frontend"

# Functions
print_header() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

check_requirements() {
    print_header "Checking Requirements"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found"
        return 1
    fi
    print_success "Python 3 found"
    
    # Check Flask
    if ! python3 -c "import flask" 2>/dev/null; then
        print_error "Flask not found. Run: pip install -r requirements.txt"
        return 1
    fi
    print_success "Flask installed"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js not found. Install from https://nodejs.org/"
        return 1
    fi
    print_success "Node.js found: $(node --version)"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm not found"
        return 1
    fi
    print_success "npm found: $(npm --version)"
    
    return 0
}

setup_environment() {
    print_header "Setting Up Environment"
    
    export FLASK_ENV=development
    # When starting from backend dir, use relative module path
    export FLASK_APP=api/ai_dashboard.py
    export RPC_URL="${RPC_URL:-https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu}"
    export DATABASE_URL="${DATABASE_URL:-postgresql://blockchain_user:change-me-to-secure-password@127.0.0.1:5432/blockchain_db}"
    export POLLING_INTERVAL=10
    export MAX_WORKERS=5
    
    print_success "Environment variables configured"
    return 0
}

install_frontend_deps() {
    print_header "Setting Up Frontend"
    
    if [ -d "$FRONTEND_DIR/node_modules" ]; then
        print_success "node_modules already exists"
    else
        print_info "Installing npm packages..."
        cd "$FRONTEND_DIR"
        npm install --legacy-peer-deps
        cd "$WORKSPACE_ROOT"
        print_success "npm dependencies installed"
    fi
    
    return 0
}

start_backend() {
    print_header "Starting Backend (Flask)"
    
    print_info "Starting Flask server on http://localhost:5000..."
    cd "$BACKEND_DIR"
    python3 -m flask run --host=0.0.0.0 --port=5000 &
    BACKEND_PID=$!
    
    sleep 2
    
    if kill -0 $BACKEND_PID 2>/dev/null; then
        print_success "Backend started (PID: $BACKEND_PID)"
    else
        print_error "Backend failed to start"
        return 1
    fi
    
    cd "$WORKSPACE_ROOT"
    return 0
}

start_frontend() {
    print_header "Starting Frontend (React)"
    
    print_info "Starting React dev server on http://localhost:3000..."
    cd "$FRONTEND_DIR"
    
    if [ -f "vite.config.js" ]; then
        npm run dev &
    else
        npm start &
    fi
    
    FRONTEND_PID=$!
    sleep 3
    
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_success "Frontend started (PID: $FRONTEND_PID)"
    else
        print_error "Frontend failed to start"
        return 1
    fi
    
    cd "$WORKSPACE_ROOT"
    return 0
}

open_browser() {
    print_info "Opening browser..."
    sleep 2
    
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000 &
    elif command -v open &> /dev/null; then
        open http://localhost:3000 &
    else
        print_info "Could not auto-open browser. Visit http://localhost:3000 manually"
    fi
}

# Main execution
main() {
    print_header "🚀 Blockchain ML - Complete Startup"
    
    # Cleanup function
    cleanup() {
        print_header "Shutting Down"
        print_info "Stopping services..."
        
        if [ ! -z "$BACKEND_PID" ]; then
            kill $BACKEND_PID 2>/dev/null || true
        fi
        
        if [ ! -z "$FRONTEND_PID" ]; then
            kill $FRONTEND_PID 2>/dev/null || true
        fi
        
        print_success "All services stopped"
        exit 0
    }
    
    # Set trap to cleanup on exit
    trap cleanup EXIT INT TERM
    
    # Run startup steps
    check_requirements || exit 1
    setup_environment || exit 1
    install_frontend_deps || exit 1
    start_backend || exit 1
    start_frontend || exit 1
    open_browser
    
    # Print summary
    print_header "✅ All Services Running"
    echo -e "${GREEN}Backend:  ${NC}http://localhost:5000"
    echo -e "${GREEN}Frontend: ${NC}http://localhost:3000"
    echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}\n"
    
    # Wait indefinitely
    wait
}

# Run main function
main
