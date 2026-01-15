"""
Real-Time Blockchain Data Processor
Process Ethereum data in real-time WITHOUT storage
3 output modes: Console, JSON file, or Custom webhook
"""
import os
import json
import logging
import time
import pandas as pd
from datetime import datetime
from web3 import Web3
from backend.etl.extract import extract_blocks
from backend.etl.transform import transform_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
RPC_URL = os.getenv('RPC_URL', "https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu")
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '5'))
OUTPUT_MODE = os.getenv('OUTPUT_MODE', 'console')  # console, json, csv, webhook
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')


class RealtimeBlockchainProcessor:
    """Process blockchain data in real-time without storage"""
    
    def __init__(self):
        self.w3 = None
        self.last_block = None
        self.stats = {
            'blocks_processed': 0,
            'transactions_processed': 0,
            'total_eth_value': 0.0
        }
    
    def initialize(self):
        """Initialize Web3 connection"""
        try:
            self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
            if not self.w3.is_connected():
                logger.error("Web3 connection failed")
                return False
            self.last_block = self.w3.eth.block_number
            logger.info(f"✅ Connected to Ethereum - Current block: {self.last_block}")
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return False
    
    def process_realtime(self, continuous=True, interval=60):
        """
        Process blocks in real-time
        
        Args:
            continuous: Keep processing forever
            interval: Seconds to wait between checks
        """
        logger.info(f"🚀 Starting real-time processor (Output: {OUTPUT_MODE})")
        
        try:
            while True:
                current_block = self.w3.eth.block_number
                
                # New blocks arrived
                if current_block > self.last_block:
                    start_block = self.last_block + 1
                    end_block = min(current_block, start_block + BATCH_SIZE - 1)
                    
                    logger.info(f"\n📦 Processing blocks {start_block}-{end_block}...")
                    
                    # Extract and transform
                    raw_data = extract_blocks(start_block, end_block, self.w3)
                    processed_data = transform_data(raw_data)
                    
                    if not processed_data.empty:
                        # Process in real-time
                        self._output_data(processed_data)
                        
                        # Update stats
                        self.stats['blocks_processed'] += (end_block - start_block + 1)
                        self.stats['transactions_processed'] += len(processed_data)
                        self.stats['total_eth_value'] += processed_data['value_eth'].sum()
                        
                        logger.info(f"✅ Processed {len(processed_data)} transactions")
                        logger.info(f"📊 Stats: {self.stats['transactions_processed']} total, "
                                  f"{self.stats['total_eth_value']:.2f} ETH total")
                    
                    self.last_block = end_block
                else:
                    logger.debug("⏳ No new blocks yet...")
                
                if not continuous:
                    break
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("\n⛔ Stopped by user")
            self._print_summary()
        except Exception as e:
            logger.error(f"Error: {e}")
    
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
            print(f"""
Transaction #{idx + 1}:
  Block: {row['block_number']}
  From: {row['from_address'][:10]}...
  To:   {row['to_address'][:10] if pd.notna(row['to_address']) else 'Contract Creation'}...
  Value: {row['value_eth']} ETH
  Gas Used: {row['gas_used']}
  Status: {'✅ Success' if row['status'] == 1 else '❌ Failed'}
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
            
            # Aggregate data
            summary = {
                'timestamp': datetime.now().isoformat(),
                'transactions': len(df),
                'total_eth': float(df['value_eth'].sum()),
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
    processor.process_realtime(continuous=True, interval=30)


if __name__ == "__main__":
    main()
