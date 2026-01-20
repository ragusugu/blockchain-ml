"""
Standalone Ankr Streaming Service
Runs independently from batch ETL processing
Start this separately or in a different container
"""
import os
import sys
import logging
import time
import signal
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.streaming_manager import initialize_streaming, start_streaming_service, stop_streaming_service, get_streaming_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [StreamingService] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnkrStreamingService:
    """Standalone service for Ankr blockchain streaming"""
    
    def __init__(self):
        self.running = False
        self.setup_signal_handlers()
        
    def setup_signal_handlers(self):
        """Setup graceful shutdown on signals"""
        def signal_handler(sig, frame):
            logger.info("⏹️  Received shutdown signal")
            self.shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def on_new_block(self, block_data: Dict[str, Any]) -> None:
        """Callback for each new block"""
        try:
            tx_count = block_data.get('transaction_count', 0)
            eth_value = block_data.get('total_eth_value', 0)
            
            logger.info(
                f"📦 Block #{block_data['block_number']}: "
                f"{tx_count} transactions, {eth_value:.4f} ETH"
            )
            
            # You can add custom processing here
            # e.g., send to webhook, store in cache, etc.
            
        except Exception as e:
            logger.error(f"Error in callback: {e}")
    
    def run(self):
        """Run the streaming service"""
        logger.info("=" * 60)
        logger.info("🚀 ANKR BLOCKCHAIN STREAMING SERVICE")
        logger.info("=" * 60)
        
        try:
            # Initialize with callback
            if not initialize_streaming(callback=self.on_new_block):
                logger.error("❌ Failed to initialize streaming")
                return False
            
            # Start streaming in background
            if not start_streaming_service(background=True):
                logger.error("❌ Failed to start streaming")
                return False
            
            self.running = True
            logger.info("✅ Streaming service running...")
            logger.info("Press Ctrl+C to stop")
            logger.info("=" * 60)
            
            # Keep the service running
            try:
                while self.running:
                    time.sleep(5)
                    
                    # Periodically print stats
                    stats = get_streaming_stats()
                    if stats.get('last_update'):
                        logger.info(
                            f"📊 Status - Blocks: {stats['blocks_streamed']}, "
                            f"Txs: {stats['transactions_streamed']}, "
                            f"Errors: {stats['errors']}"
                        )
                        
            except KeyboardInterrupt:
                logger.info("⏹️  Keyboard interrupt received")
                
        except Exception as e:
            logger.error(f"❌ Service error: {e}", exc_info=True)
            return False
        finally:
            self.shutdown()
        
        return True
    
    def shutdown(self):
        """Gracefully shutdown the service"""
        logger.info("🛑 Shutting down streaming service...")
        self.running = False
        stop_streaming_service()
        logger.info("✅ Service stopped")


if __name__ == "__main__":
    service = AnkrStreamingService()
    success = service.run()
    
    if not success:
        sys.exit(1)
