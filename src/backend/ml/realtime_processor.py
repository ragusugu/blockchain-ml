"""
Real-Time Blockchain Data Processor (Optimized)
Process Ethereum data in real-time with parallel execution
3 output modes: Console, JSON file, or Custom webhook
Performance: ~1000 tx/sec on modern hardware
"""
import json
import logging
import time
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from config import cfg
from connections import get_web3
from logging_config import setup_logging
from etl.extract import extract_blocks
from etl.transform import transform_data

setup_logging()
logger = logging.getLogger(__name__)

# Configuration from centralized config
BATCH_SIZE = cfg.BATCH_SIZE
POLLING_INTERVAL = cfg.POLLING_INTERVAL
MAX_WORKERS = cfg.MAX_WORKERS
OUTPUT_MODE = cfg.OUTPUT_MODE
WEBHOOK_URL = cfg.WEBHOOK_URL


class RealtimeBlockchainProcessor:
    """Process blockchain data in real-time with parallel optimization"""
    
    def __init__(self):
        self.w3 = None
        self.last_block = None
        self.stats = {
            'blocks_processed': 0,
            'transactions_processed': 0,
            'total_eth_value': 0.0,
            'total_time': 0.0,
            'avg_time_per_block': 0.0
        }
        self.output_executor = ThreadPoolExecutor(max_workers=1)  # Single thread for I/O
    
    def initialize(self):
        """Initialize Web3 connection via shared factory"""
        self.w3 = get_web3()
        if not self.w3:
            logger.error("❌ Failed to connect to Web3")
            return False
        
        self.last_block = self.w3.eth.block_number
        logger.info(f"✅ Connected — block: {self.last_block}, polling: {POLLING_INTERVAL}s, workers: {MAX_WORKERS}")
        return True
        return False
    
    def process_realtime(self, continuous=True, interval=None):
        """
        Process blocks in real-time with parallel extraction.
        
        Args:
            continuous: Keep processing forever
            interval: Seconds to wait between checks (uses POLLING_INTERVAL env var if None)
        """
        if interval is None:
            interval = POLLING_INTERVAL
            
        logger.info(f"🚀 Starting real-time processor (Output: {OUTPUT_MODE})")
        
        try:
            while True:
                batch_start = time.time()
                current_block = self.w3.eth.block_number
                
                # New blocks arrived
                if current_block > self.last_block:
                    start_block = self.last_block + 1
                    end_block = min(current_block, start_block + BATCH_SIZE - 1)
                    
                    logger.info(f"\n📦 Processing blocks {start_block}-{end_block} (Current: {current_block})")
                    
                    # Extract and transform with parallel processing
                    raw_data = extract_blocks(start_block, end_block, self.w3, parallel=True, max_workers=MAX_WORKERS)
                    
                    if raw_data:
                        transform_start = time.time()
                        processed_data = transform_data(raw_data)
                        transform_time = time.time() - transform_start
                        
                        if not processed_data.empty:
                            # Process in real-time (non-blocking output)
                            self.output_executor.submit(self._output_data, processed_data)
                            
                            # Update stats
                            self.stats['blocks_processed'] += (end_block - start_block + 1)
                            self.stats['transactions_processed'] += len(processed_data)
                            # Handle both 'value_eth' and 'value' column names
                            value_col = 'value' if 'value' in processed_data.columns else 'value_eth'
                            self.stats['total_eth_value'] += processed_data[value_col].sum()
                            
                            batch_time = time.time() - batch_start
                            self.stats['total_time'] += batch_time
                            self.stats['avg_time_per_block'] = self.stats['total_time'] / self.stats['blocks_processed']
                            
                            logger.info(f"✅ Processed {len(processed_data)} transactions in {batch_time:.2f}s")
                            logger.info(f"📊 Transform: {transform_time:.3f}s | Total batch: {batch_time:.2f}s")
                            logger.info(f"📈 Avg: {self.stats['avg_time_per_block']:.2f}s/block")
                    
                    self.last_block = end_block
                else:
                    logger.debug(f"⏳ No new blocks (Last: {self.last_block}, Current: {current_block})")
                
                if not continuous:
                    break
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("\n⛔ Stopped by user")
            self._print_summary()
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            self.output_executor.shutdown(wait=True)
    
    def _output_data(self, df):
        """Output processed data based on mode"""
        if OUTPUT_MODE == 'console':
            self._output_console(df)
        elif OUTPUT_MODE == 'json':
            self._output_json(df)
        elif OUTPUT_MODE == 'csv':
            self._output_csv(df)
        elif OUTPUT_MODE == 'webhook':
            self._output_webhook(df)
    
    def _output_console(self, df):
        """Print to console (streaming view)"""
        print("\n" + "="*100)
        for idx, row in df.iterrows():
            # Handle both column naming conventions
            block_num = row.get('block_number', row.get('block_number'))
            from_addr = row.get('from_addr', row.get('from_address', ''))
            to_addr = row.get('to_addr', row.get('to_address', ''))
            value = row.get('value', row.get('value_eth', 0))
            gas = row.get('gas_used', 0)
            status = row.get('status', 0)
            
            print(f"""
Transaction #{idx + 1}:
  Block: {block_num}
  From: {from_addr[:10]}...
  To:   {to_addr[:10] if to_addr else 'Contract Creation'}...
  Value: {value} ETH
  Gas Used: {gas}
  Status: {'✅ Success' if status == 1 else '❌ Failed'}
            """)
        print("="*100)
    
    def _output_json(self, df):
        """Append to JSON file (streaming)"""
        filename = f"realtime_data_{datetime.now().strftime('%Y%m%d')}.json"
        
        records = json.loads(df.to_json(orient='records'))
        
        # Append to file
        try:
            with open(filename, 'r') as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []
        
        existing.extend(records)
        
        with open(filename, 'w') as f:
            json.dump(existing, f, indent=2)
        
        logger.info(f"💾 Saved {len(records)} records to {filename}")
    
    def _output_csv(self, df):
        """Append to CSV file (streaming)"""
        filename = f"realtime_data_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Append mode
        mode = 'a' if os.path.exists(filename) else 'w'
        df.to_csv(filename, mode=mode, header=(mode == 'w'), index=False)
        
        logger.info(f"💾 Saved {len(df)} records to {filename}")
    
    def _output_webhook(self, df):
        """Send to webhook (e.g., Discord, Slack, custom API)"""
        if not WEBHOOK_URL:
            logger.warning("⚠️ No WEBHOOK_URL configured")
            return
        
        try:
            import requests
            
            # Handle both column naming conventions
            value_col = 'value' if 'value' in df.columns else 'value_eth'
            
            # Aggregate data
            summary = {
                'timestamp': datetime.now().isoformat(),
                'transactions': len(df),
                'total_eth': float(df[value_col].sum()),
                'data': json.loads(df.to_json(orient='records'))
            }
            
            response = requests.post(WEBHOOK_URL, json=summary, timeout=5)
            logger.info(f"✅ Webhook sent (status: {response.status_code})")
        except Exception as e:
            logger.warning(f"⚠️ Webhook failed: {e}")
    
    def _print_summary(self):
        """Print final statistics"""
        print("\n" + "="*50)
        print("📊 REALTIME PROCESSOR SUMMARY")
        print("="*50)
        print(f"Blocks processed: {self.stats['blocks_processed']}")
        print(f"Transactions processed: {self.stats['transactions_processed']}")
        print(f"Total ETH value: {self.stats['total_eth_value']:.2f}")
        print("="*50)


def main():
    """Run real-time processor"""
    processor = RealtimeBlockchainProcessor()
    
    if not processor.initialize():
        return
    
    # Process continuously (Ctrl+C to stop)
    processor.process_realtime(continuous=True)


if __name__ == "__main__":
    main()
