#!/usr/bin/env python
"""
Test script for Ankr Streaming Setup
Validates connectivity and functionality
"""
import sys
import os
import logging
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Test] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_section(title: str):
    """Print section header"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(msg: str):
    """Print success message"""
    print(f"{GREEN}✅ {msg}{RESET}")


def print_error(msg: str):
    """Print error message"""
    print(f"{RED}❌ {msg}{RESET}")


def print_warning(msg: str):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {msg}{RESET}")


def print_info(msg: str):
    """Print info message"""
    print(f"{BLUE}ℹ️  {msg}{RESET}")


def test_imports() -> bool:
    """Test if all required modules can be imported"""
    print_section("1️⃣  Testing Imports")
    
    modules = [
        ('web3', 'Web3'),
        ('etl.ankr_streamer', 'AnkrBlockchainStreamer'),
        ('etl.streaming_manager', 'StreamingServiceManager'),
    ]
    
    all_ok = True
    for module_name, class_name in modules:
        try:
            if module_name == 'web3':
                from web3 import Web3
                print_success(f"Imported {module_name}")
            else:
                __import__(module_name)
                print_success(f"Imported {module_name}.{class_name}")
        except ImportError as e:
            print_error(f"Failed to import {module_name}: {e}")
            all_ok = False
    
    return all_ok


def test_ankr_connection() -> bool:
    """Test connection to Ankr RPC"""
    print_section("2️⃣  Testing Ankr Connection")
    
    try:
        from web3 import Web3
        
        ankr_url = os.getenv('ANKR_RPC_URL', 'https://rpc.ankr.com/eth')
        print_info(f"Connecting to: {ankr_url}")
        
        w3 = Web3(Web3.HTTPProvider(ankr_url, request_kwargs={'timeout': 10}))
        
        if not w3.is_connected():
            print_error("Failed to connect to Ankr")
            return False
        
        print_success("Connected to Ankr")
        
        # Get latest block
        try:
            block_num = w3.eth.block_number
            print_success(f"Latest block: {block_num}")
            
            # Get block details
            block = w3.eth.get_block(block_num)
            print_info(f"Block timestamp: {block.timestamp}")
            print_info(f"Transactions: {len(block.transactions)}")
            print_info(f"Miner: {block.miner}")
            
            return True
        except Exception as e:
            print_error(f"Error fetching block data: {e}")
            return False
            
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False


def test_streamer_initialization() -> bool:
    """Test streamer initialization"""
    print_section("3️⃣  Testing Streamer Initialization")
    
    try:
        from etl.ankr_streamer import AnkrBlockchainStreamer
        
        print_info("Creating AnkrBlockchainStreamer instance...")
        streamer = AnkrBlockchainStreamer()
        
        print_success("Streamer instance created")
        
        print_info("Testing connection...")
        if streamer.connect():
            print_success("Streamer connected to Ankr")
            print_info(f"Current block: {streamer.last_block}")
            return True
        else:
            print_error("Streamer failed to connect")
            return False
            
    except Exception as e:
        print_error(f"Streamer initialization error: {e}")
        return False


def test_block_processing() -> bool:
    """Test block data processing"""
    print_section("4️⃣  Testing Block Processing")
    
    try:
        from etl.ankr_streamer import AnkrBlockchainStreamer
        
        streamer = AnkrBlockchainStreamer()
        if not streamer.connect():
            print_error("Failed to connect streamer")
            return False
        
        # Get current block
        current_block = streamer.last_block
        print_info(f"Fetching block {current_block}...")
        
        block_data = streamer.get_block_data(current_block)
        
        if not block_data:
            print_error("Failed to fetch block data")
            return False
        
        print_success(f"Block data fetched successfully")
        print_info(f"  Block number: {block_data['block_number']}")
        print_info(f"  Transactions: {block_data['transaction_count']}")
        print_info(f"  Total ETH value: {block_data['total_eth_value']:.4f}")
        print_info(f"  Gas used: {block_data['gas_used']}")
        
        return True
        
    except Exception as e:
        print_error(f"Block processing error: {e}")
        return False


def test_environment() -> Dict[str, str]:
    """Test environment variables"""
    print_section("5️⃣  Environment Variables")
    
    env_vars = {
        'ANKR_RPC_URL': 'https://rpc.ankr.com/eth',
        'ANKR_POLLING_INTERVAL': '12',
        'ANKR_BATCH_SIZE': '10',
        'STREAMING_ENABLED': 'true',
        'DATABASE_URL': '(optional)',
    }
    
    config = {}
    for var_name, default in env_vars.items():
        value = os.getenv(var_name)
        if value:
            print_success(f"{var_name}: {value}")
            config[var_name] = value
        else:
            print_warning(f"{var_name}: Not set (using default: {default})")
            config[var_name] = default
    
    return config


def test_streaming_manager() -> bool:
    """Test streaming manager"""
    print_section("6️⃣  Testing Streaming Manager")
    
    try:
        from etl.streaming_manager import get_streaming_manager
        
        manager = get_streaming_manager()
        print_success("Streaming manager created")
        
        # Try to initialize
        print_info("Initializing streaming...")
        if manager.initialize_ankr_streaming():
            print_success("Streaming initialized successfully")
            
            # Get stats
            stats = manager.get_streaming_stats()
            print_info(f"Status: {stats.get('running', 'unknown')}")
            
            return True
        else:
            print_warning("Streaming initialization returned False")
            return False
            
    except Exception as e:
        print_error(f"Streaming manager error: {e}")
        return False


def main():
    """Run all tests"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}ANKR STREAMING TEST SUITE{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")
    
    results = {}
    
    # Run tests
    tests = [
        ("Imports", test_imports),
        ("Ankr Connection", test_ankr_connection),
        ("Streamer Init", test_streamer_initialization),
        ("Block Processing", test_block_processing),
        ("Streaming Manager", test_streaming_manager),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print_error(f"Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Environment check
    print_section("Environment Check")
    env_config = test_environment()
    
    # Print summary
    print_section("📊 TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print()
    print_info(f"Total: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print_section("🎉 ALL TESTS PASSED!")
        print_success("Your Ankr streaming setup is ready!")
        print()
        print(f"{YELLOW}Next steps:{RESET}")
        print(f"  1. docker-compose --profile streaming up -d")
        print(f"  2. docker-compose logs -f ankr-streamer")
        print()
        return 0
    else:
        print_section("⚠️  SOME TESTS FAILED")
        print_error("Please fix the issues above and try again")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
