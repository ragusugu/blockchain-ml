"""
Streaming Service Manager
Manages both Ankr streaming and batch processing independently
Keeps batch ETL process untouched
"""
import os
import logging
import threading
import time
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Import both services
from etl.ankr_streamer import AnkrBlockchainStreamer


class StreamingServiceManager:
    """
    Manages Ankr streaming service independently from batch processing.
    Batch ETL (main_etl.py) continues to work as-is.
    """
    
    def __init__(self):
        self.ankr_streamer: Optional[AnkrBlockchainStreamer] = None
        self.is_running = False
        self.manager_thread: Optional[threading.Thread] = None
        self.startup_time = None
        
    def initialize_ankr_streaming(self, callback=None) -> bool:
        """
        Initialize Ankr streaming service.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("🚀 Initializing Ankr streaming service...")
            
            self.ankr_streamer = AnkrBlockchainStreamer(callback=callback)
            
            if self.ankr_streamer.connect():
                logger.info("✅ Ankr streaming service ready")
                return True
            else:
                logger.error("❌ Failed to connect to Ankr")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error initializing Ankr streamer: {e}")
            return False
    
    def start_streaming(self, background: bool = True) -> bool:
        """
        Start the streaming service.
        
        Args:
            background: Run in background thread if True
            
        Returns:
            True if started successfully
        """
        if not self.ankr_streamer:
            logger.error("❌ Streamer not initialized. Call initialize_ankr_streaming() first.")
            return False
        
        if self.is_running:
            logger.warning("⚠️  Streaming already running")
            return False
        
        try:
            self.is_running = True
            self.startup_time = datetime.now()
            
            if background:
                logger.info("🔄 Starting Ankr streaming in background...")
                self.ankr_streamer.start_background()
            else:
                logger.info("🚀 Starting Ankr streaming...")
                self.ankr_streamer.stream(continuous=True)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting streaming: {e}")
            self.is_running = False
            return False
    
    def stop_streaming(self) -> None:
        """Stop the streaming service"""
        if self.ankr_streamer:
            self.ankr_streamer.stop()
        self.is_running = False
        logger.info("✅ Streaming service stopped")
    
    def get_streaming_stats(self) -> Dict[str, Any]:
        """Get current streaming statistics"""
        if not self.ankr_streamer:
            return {'status': 'not_initialized'}
        
        stats = self.ankr_streamer.get_stats()
        stats['uptime'] = str(datetime.now() - self.startup_time) if self.startup_time else None
        
        return stats
    
    def print_streaming_status(self) -> None:
        """Print formatted streaming status"""
        if not self.ankr_streamer:
            logger.info("❌ Streaming service not initialized")
            return
        
        self.ankr_streamer.print_stats()


# Global instance
_streaming_manager: Optional[StreamingServiceManager] = None


def get_streaming_manager() -> StreamingServiceManager:
    """Get or create the global streaming manager"""
    global _streaming_manager
    if _streaming_manager is None:
        _streaming_manager = StreamingServiceManager()
    return _streaming_manager


def initialize_streaming(callback=None) -> bool:
    """
    Initialize the streaming service.
    
    This runs independently and doesn't affect batch processing.
    """
    manager = get_streaming_manager()
    return manager.initialize_ankr_streaming(callback=callback)


def start_streaming_service(background: bool = True) -> bool:
    """
    Start the streaming service.
    
    Args:
        background: Run in background if True
    """
    manager = get_streaming_manager()
    return manager.start_streaming(background=background)


def stop_streaming_service() -> None:
    """Stop the streaming service"""
    manager = get_streaming_manager()
    manager.stop_streaming()


def get_streaming_stats() -> Dict[str, Any]:
    """Get streaming statistics"""
    manager = get_streaming_manager()
    return manager.get_streaming_stats()
