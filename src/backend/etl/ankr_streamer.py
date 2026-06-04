"""
Ankr Streaming Service
Real-time blockchain data streaming using Ankr's free API
Runs independently without affecting batch processing
"""
import json
import logging
import threading
import time
from datetime import datetime
from typing import Callable, Dict, Any, Optional
from web3 import Web3
from collections import defaultdict

from config import cfg
from etl.transform import transform_data
from etl.storage import persist_transformed_transactions

logger = logging.getLogger(__name__)

# Configuration from centralized config
ANKR_RPC_URL = cfg.ANKR_RPC_URL
POLLING_INTERVAL = cfg.ANKR_POLLING_INTERVAL
BATCH_SIZE = cfg.ANKR_BATCH_SIZE
STREAMING_ENABLED = cfg.STREAMING_ENABLED


class AnkrBlockchainStreamer:
    """
    Stream real-time Ethereum data using Ankr's free RPC endpoint.
    Completely independent from batch processing.
    """
    
    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize Ankr streamer.
        
        Args:
            callback: Function to call for each new block (optional)
        """
        self.w3 = None
        self.last_block = 0
        self.callback = callback
        self.is_running = False
        self.stats = {
            'blocks_streamed': 0,
            'transactions_streamed': 0,
            'transactions_persisted': 0,
            'start_time': None,
            'last_update': None,
            'errors': 0
        }
        self.stream_thread = None
        self.block_buffer = []
        self.buffer_lock = threading.Lock()
        
    def connect(self) -> bool:
        """Initialize connection to Ankr RPC"""
        try:
            logger.info(f"🔗 Connecting to Ankr: {ANKR_RPC_URL}")
            
            # Use HTTP Provider (Ankr doesn't support WebSocket on free tier)
            self.w3 = Web3(Web3.HTTPProvider(
                ANKR_RPC_URL,
                request_kwargs={'timeout': 30}
            ))
            
            if not self.w3.is_connected():
                logger.error("❌ Failed to connect to Ankr")
                return False
                
            self.last_block = self.w3.eth.block_number
            logger.info(f"✅ Connected to Ankr - Current block: {self.last_block}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def get_block_data(self, block_number: int) -> Optional[Dict]:
        """
        Fetch block data from Ankr.
        
        Args:
            block_number: Block number to fetch
            
        Returns:
            Block data dictionary or None
        """
        try:
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            
            # Extract key data
            block_data = {
                'block_number': block.number,
                'block_hash': block.hash.hex() if block.hash else None,
                'timestamp': block.timestamp,
                'miner': block.miner,
                'gas_used': block.gasUsed,
                'gas_limit': block.gasLimit,
                'transaction_count': len(block.transactions),
                'transactions': []
            }
            
            # Extract transaction data
            total_value = 0
            for tx in block.transactions:
                try:
                    receipt = self.w3.eth.get_transaction_receipt(tx.hash)
                    
                    tx_data = {
                        'hash': tx.hash.hex(),
                        'from': tx['from'],
                        'to': tx.to,
                        'value': float(tx.value / 1e18),  # Convert to ETH
                        'gas_price': float(tx.gasPrice / 1e9),  # Convert to Gwei
                        'gas_used': receipt.gasUsed if receipt else None,
                        'status': receipt.status if receipt else None,
                        'timestamp': block.timestamp
                    }
                    
                    block_data['transactions'].append(tx_data)
                    total_value += tx_data['value']
                    
                except Exception as e:
                    logger.debug(f"Error processing transaction: {e}")
                    continue
            
            block_data['total_eth_value'] = total_value
            return block_data
            
        except Exception as e:
            logger.error(f"Error fetching block {block_number}: {e}")
            self.stats['errors'] += 1
            return None
    
    def process_block(self, block_data: Dict) -> None:
        """
        Process a single block of data.
        
        Args:
            block_data: Block data dictionary
        """
        try:
            self.stats['blocks_streamed'] += 1
            self.stats['transactions_streamed'] += block_data['transaction_count']
            self.stats['last_update'] = datetime.now().isoformat()
            
            should_flush = False
            with self.buffer_lock:
                self.block_buffer.append(block_data)
                should_flush = len(self.block_buffer) >= BATCH_SIZE

            # Flush outside the buffer lock because DB writes can be slow.
            if should_flush:
                self._flush_buffer()
            
            # Call user callback if provided
            if self.callback:
                self.callback(block_data)
                
        except Exception as e:
            logger.error(f"Error processing block: {e}")
            self.stats['errors'] += 1
    
    def _flush_buffer(self) -> None:
        """Flush buffered blocks"""
        with self.buffer_lock:
            if not self.block_buffer:
                return
            batch = self.block_buffer.copy()
            self.block_buffer.clear()

        try:
            logger.info(f"📦 Flushing {len(batch)} blocks to storage")
            
            # Flatten block-level data into transaction-level rows
            # transform_data() expects a list of transaction dicts, not block dicts
            tx_rows = []
            for block_data in batch:
                for tx_index, tx in enumerate(block_data.get('transactions', [])):
                    tx_rows.append({
                        'block_number': block_data['block_number'],
                        'block_hash': block_data.get('block_hash'),
                        'timestamp': block_data.get('timestamp'),
                        'tx_hash': tx.get('hash'),
                        'transaction_index': tx_index,
                        'from_address': tx.get('from'),
                        'to_address': tx.get('to'),
                        'value_eth': tx.get('value', 0),
                        'gas': 0,
                        'gas_price_gwei': tx.get('gas_price', 0),
                        'gas_used': tx.get('gas_used', 0),
                        'cumulative_gas_used': 0,
                        'status': tx.get('status', 1),
                        'contract_address': None,
                        'effective_gas_price': 0,
                    })
            
            if tx_rows:
                transformed_data = transform_data(tx_rows)
                persisted = persist_transformed_transactions(transformed_data)
                self.stats['transactions_persisted'] += persisted
                logger.info(
                    "Transformed %s streamed transaction(s); persisted %s",
                    len(transformed_data),
                    persisted,
                )
            
        except Exception as e:
            logger.error(f"Error flushing buffer: {e}")
            self.stats['errors'] += 1
    
    def stream(self, continuous: bool = True) -> None:
        """
        Stream blocks indefinitely.
        
        Args:
            continuous: Keep streaming forever
        """
        if not self.w3:
            logger.error("❌ Not connected. Call connect() first.")
            return
        
        self.is_running = True
        self.stats['start_time'] = datetime.now().isoformat()
        
        logger.info(f"🚀 Starting Ankr streaming (interval: {POLLING_INTERVAL}s)")
        logger.info(f"📊 Poll Interval: {POLLING_INTERVAL}s | Batch Size: {BATCH_SIZE}")
        
        try:
            while continuous and self.is_running:
                try:
                    current_block = self.w3.eth.block_number
                    
                    # Process new blocks
                    if current_block > self.last_block:
                        blocks_to_process = current_block - self.last_block
                        logger.info(f"📦 Found {blocks_to_process} new block(s)")
                        
                        for block_num in range(self.last_block + 1, current_block + 1):
                            logger.debug(f"Fetching block {block_num}...")
                            block_data = self.get_block_data(block_num)
                            
                            if block_data:
                                self.process_block(block_data)
                                logger.info(
                                    f"✅ Block {block_num}: "
                                    f"{block_data['transaction_count']} txs, "
                                    f"{block_data['total_eth_value']:.4f} ETH"
                                )
                        
                        self.last_block = current_block
                    else:
                        logger.debug(f"No new blocks. Latest: {current_block}")
                    
                    # Wait before next poll
                    time.sleep(POLLING_INTERVAL)
                    
                except Exception as e:
                    logger.error(f"❌ Streaming error: {e}")
                    self.stats['errors'] += 1
                    time.sleep(5)  # Wait before retry
                    
        except KeyboardInterrupt:
            logger.info("⏹️  Streaming stopped by user")
        except Exception as e:
            logger.error(f"❌ Streaming failed: {e}")
        finally:
            self._flush_buffer()  # Flush remaining data
            self.is_running = False
            logger.info("✅ Streamer stopped")
    
    def start_background(self) -> threading.Thread:
        """Start streaming in background thread"""
        if self.stream_thread and self.stream_thread.is_alive():
            logger.warning("⚠️  Streamer already running")
            return self.stream_thread
        
        self.stream_thread = threading.Thread(
            target=self.stream,
            daemon=True,
            name="AnkrStreamer"
        )
        self.stream_thread.start()
        logger.info("✅ Ankr streamer started in background")
        return self.stream_thread
    
    def stop(self) -> None:
        """Stop streaming"""
        self.is_running = False
        if self.stream_thread:
            self.stream_thread.join(timeout=10)
        logger.info("✅ Streamer stopped")
    
    def get_stats(self) -> Dict:
        """Get streaming statistics"""
        return {
            **self.stats,
            'buffer_size': len(self.block_buffer),
            'running': self.is_running
        }
    
    def print_stats(self) -> None:
        """Print formatted statistics"""
        stats = self.get_stats()
        
        logger.info(
            f"\n"
            f"╔════════════════════════════════════════════╗\n"
            f"║  📊 ANKR STREAMING STATISTICS             ║\n"
            f"╠════════════════════════════════════════════╣\n"
            f"║ Blocks Streamed:    {stats['blocks_streamed']:<20} ║\n"
            f"║ Transactions:       {stats['transactions_streamed']:<20} ║\n"
            f"║ Errors:             {stats['errors']:<20} ║\n"
            f"║ Buffer Size:        {stats['buffer_size']:<20} ║\n"
            f"║ Running:            {str(stats['running']):<20} ║\n"
            f"║ Last Update:        {str(stats['last_update']):<20} ║\n"
            f"╚════════════════════════════════════════════╝\n"
        )


# Standalone usage
if __name__ == "__main__":
    # Custom callback function
    def on_block(block_data: Dict):
        """Called for each new block"""
        logger.info(
            f"🔗 Block {block_data['block_number']}: "
            f"{block_data['transaction_count']} txs, "
            f"{block_data['total_eth_value']:.4f} ETH"
        )
    
    # Initialize and start streamer
    streamer = AnkrBlockchainStreamer(callback=on_block)
    
    if streamer.connect():
        try:
            streamer.stream(continuous=True)
        except KeyboardInterrupt:
            logger.info("Stopping...")
            streamer.stop()
    else:
        logger.error("Failed to connect to Ankr")
