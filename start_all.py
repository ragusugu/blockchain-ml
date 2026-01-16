#!/usr/bin/env python3
"""
One-Command Startup Script
Starts both frontend and backend automatically
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

WORKSPACE_ROOT = Path(__file__).parent
BACKEND_DIR = WORKSPACE_ROOT / 'src' / 'backend'
FRONTEND_DIR = WORKSPACE_ROOT / 'src' / 'frontend'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

def check_requirements():
    """Check if required tools/packages are installed"""
    print_header("Checking Requirements")
    
    # Check Python
    try:
        import flask
        print_success("Python & Flask installed")
    except ImportError:
        print_error("Flask not found. Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print_success(f"Node.js installed: {result.stdout.strip()}")
    except FileNotFoundError:
        print_error("Node.js not found. Install from https://nodejs.org/")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print_success(f"npm installed: {result.stdout.strip()}")
    except FileNotFoundError:
        print_error("npm not found")
        return False
    
    return True

def setup_environment():
    """Setup environment variables"""
    print_header("Setting Up Environment")
    
    env_file = WORKSPACE_ROOT / '.env'
    if env_file.exists():
        print_success(f"Found .env file")
    else:
        print_info("No .env file found. Using defaults.")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    # When running from backend dir, use relative module path
    os.environ['FLASK_APP'] = 'api/ai_dashboard.py'
    os.environ['RPC_URL'] = os.getenv('RPC_URL', 'https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu')
    os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/blockchain_db')
    os.environ['POLLING_INTERVAL'] = '10'
    os.environ['MAX_WORKERS'] = '5'
    
    print_success("Environment variables configured")
    return True

def install_frontend_deps():
    """Install frontend dependencies if needed"""
    print_header("Setting Up Frontend")
    
    node_modules = FRONTEND_DIR / 'node_modules'
    package_lock = FRONTEND_DIR / 'package-lock.json'
    
    if node_modules.exists():
        print_success("node_modules already exists")
    else:
        print_info("Installing npm packages...")
        result = subprocess.run(
            ['npm', 'install'],
            cwd=FRONTEND_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("npm dependencies installed")
        else:
            print_error(f"npm install failed: {result.stderr}")
            return False
    
    return True

def start_backend():
    """Start Flask backend server"""
    print_header("Starting Backend (Flask)")
    
    try:
        print_info("Starting Flask server on http://localhost:5000...")
        # Use python -m flask run for better compatibility
        process = subprocess.Popen(
            [sys.executable, '-m', 'flask', 'run', '--host=0.0.0.0', '--port=5000'],
            cwd=BACKEND_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        if process.poll() is None:
            print_success("Backend started (PID: {})".format(process.pid))
            return process
        else:
            stdout, stderr = process.communicate()
            print_error(f"Backend failed to start:\n{stderr}")
            return None
    except Exception as e:
        print_error(f"Failed to start backend: {e}")
        return None

def start_frontend():
    """Start React dev server"""
    print_header("Starting Frontend (React)")
    
    try:
        print_info("Starting React dev server on http://localhost:3000...")
        # Check for vite config
        vite_config = FRONTEND_DIR / 'vite.config.js'
        
        if vite_config.exists():
            # Use Vite
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=FRONTEND_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        else:
            # Use Create React App
            process = subprocess.Popen(
                ['npm', 'start'],
                cwd=FRONTEND_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        
        time.sleep(3)
        
        if process.poll() is None:
            print_success("Frontend started (PID: {})".format(process.pid))
            return process
        else:
            stdout, stderr = process.communicate()
            print_error(f"Frontend failed to start:\n{stderr}")
            return None
    except Exception as e:
        print_error(f"Failed to start frontend: {e}")
        return None

def open_browser():
    """Open browser to the application"""
    print_info("Opening browser...")
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:3000')
        print_success("Browser opened at http://localhost:3000")
    except Exception as e:
        print_info(f"Could not auto-open browser. Visit http://localhost:3000 manually")

def main():
    print_header("🚀 Blockchain ML - Complete Startup")
    
    # Check requirements
    if not check_requirements():
        print_error("Please install missing requirements and try again")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print_error("Environment setup failed")
        sys.exit(1)
    
    # Install frontend deps
    if not install_frontend_deps():
        print_error("Frontend setup failed")
        sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print_error("Could not start backend. Check logs above.")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print_error("Could not start frontend. Check logs above.")
        backend_process.terminate()
        sys.exit(1)
    
    # Open browser
    open_browser()
    
    # Print summary
    print_header("✅ All Services Running")
    print(f"{GREEN}Backend:  {RESET}http://localhost:5000")
    print(f"{GREEN}Frontend: {RESET}http://localhost:3000")
    print(f"\n{YELLOW}Press Ctrl+C to stop all services{RESET}\n")
    
    # Wait for processes
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print_error("Backend process died")
                break
            if frontend_process.poll() is not None:
                print_error("Frontend process died")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print_header("Shutting Down")
        print_info("Stopping backend...")
        backend_process.terminate()
        print_info("Stopping frontend...")
        frontend_process.terminate()
        
        # Wait for graceful shutdown
        time.sleep(2)
        
        # Force kill if needed
        if backend_process.poll() is None:
            backend_process.kill()
        if frontend_process.poll() is None:
            frontend_process.kill()
        
        print_success("All services stopped")
        sys.exit(0)

if __name__ == '__main__':
    main()
