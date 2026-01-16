"""
Automatic Disk Space Cleanup Utility
Monitors disk space and cleans up old files/data when space runs low
"""
import os
import shutil
import logging
import psutil
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiskCleanupManager:
    """Manages automatic disk cleanup when space is low"""
    
    def __init__(self, threshold_percent=20, cleanup_dirs=None):
        """
        Initialize cleanup manager
        
        Args:
            threshold_percent: Trigger cleanup if free space below this % (default: 20%)
            cleanup_dirs: List of directories to clean up
        """
        self.threshold_percent = threshold_percent
        self.cleanup_dirs = cleanup_dirs or [
            '/tmp',
            '/home/*/Desktop/blockchain-ml/logs',
            '/home/*/Desktop/blockchain-ml/data/cache',
        ]
    
    def get_disk_usage(self, path='/'):
        """Get disk usage info for a path"""
        try:
            usage = psutil.disk_usage(path)
            free_percent = (usage.free / usage.total) * 100
            return {
                'total': usage.total / (1024**3),  # Convert to GB
                'used': usage.used / (1024**3),
                'free': usage.free / (1024**3),
                'free_percent': free_percent
            }
        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            return None
    
    def should_cleanup(self, path='/'):
        """Check if cleanup should be triggered"""
        usage = self.get_disk_usage(path)
        if not usage:
            return False
        
        return usage['free_percent'] < self.threshold_percent
    
    def cleanup_directory(self, directory, max_age_days=7):
        """
        Clean up old files in a directory
        
        Args:
            directory: Directory to clean
            max_age_days: Delete files older than this many days
        """
        if not os.path.exists(directory):
            return 0
        
        cleaned_size = 0
        try:
            cutoff_time = datetime.now() - timedelta(days=max_age_days)
            
            for item in Path(directory).glob('**/*'):
                try:
                    if item.is_file():
                        item_time = datetime.fromtimestamp(item.stat().st_mtime)
                        
                        if item_time < cutoff_time:
                            size = item.stat().st_size
                            item.unlink()
                            cleaned_size += size
                            logger.info(f"🗑️  Deleted: {item} ({size / (1024**2):.2f}MB)")
                except Exception as e:
                    logger.warning(f"Could not delete {item}: {e}")
        
        except Exception as e:
            logger.error(f"Error cleaning {directory}: {e}")
        
        return cleaned_size
    
    def cleanup_temp_files(self):
        """Clean up temporary files and logs"""
        total_cleaned = 0
        
        # Clean /tmp
        temp_dirs = ['/tmp', '/var/tmp']
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                cleaned = self.cleanup_directory(temp_dir, max_age_days=1)
                total_cleaned += cleaned
                logger.info(f"✅ Cleaned {temp_dir}: {cleaned / (1024**2):.2f}MB")
        
        return total_cleaned
    
    def cleanup_docker_system(self):
        """Run docker system prune to clean up unused images/containers"""
        import subprocess
        
        try:
            logger.info("🧹 Running docker system prune...")
            result = subprocess.run(
                ['docker', 'system', 'prune', '-af', '--volumes'],
                capture_output=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Docker cleanup successful")
                # Parse output to get cleaned size
                output = result.stdout.decode()
                if 'Total reclaimed' in output:
                    logger.info(f"Docker output: {output.split('Total reclaimed')[1].strip()}")
            else:
                logger.warning(f"Docker cleanup failed: {result.stderr.decode()}")
        
        except Exception as e:
            logger.error(f"Error running docker cleanup: {e}")
    
    def cleanup_old_logs(self, log_dir='/home/sugangokul/Desktop/blockchain-ml/logs', max_age_days=7):
        """Clean up old log files"""
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            return 0
        
        return self.cleanup_directory(log_dir, max_age_days=max_age_days)
    
    def perform_cleanup(self):
        """Perform full cleanup routine"""
        usage_before = self.get_disk_usage()
        logger.info(f"📊 Disk usage before cleanup: {usage_before['used']:.2f}GB / {usage_before['total']:.2f}GB ({usage_before['used']/usage_before['total']*100:.1f}%)")
        
        total_cleaned = 0
        
        # Clean temporary files
        total_cleaned += self.cleanup_temp_files()
        
        # Clean old logs
        total_cleaned += self.cleanup_old_logs()
        
        # Run docker cleanup
        self.cleanup_docker_system()
        
        usage_after = self.get_disk_usage()
        logger.info(f"📊 Disk usage after cleanup: {usage_after['used']:.2f}GB / {usage_after['total']:.2f}GB ({usage_after['used']/usage_after['total']*100:.1f}%)")
        logger.info(f"✨ Total space freed: {total_cleaned / (1024**3):.2f}GB")
        
        return total_cleaned
    
    def monitor_and_cleanup(self):
        """Monitor disk space and trigger cleanup if needed"""
        usage = self.get_disk_usage()
        
        if not usage:
            return False
        
        logger.info(f"📊 Current disk usage: {usage['used']:.2f}GB / {usage['total']:.2f}GB ({usage['used']/usage['total']*100:.1f}% used, {usage['free_percent']:.1f}% free)")
        
        if self.should_cleanup():
            logger.warning(f"⚠️  Disk space low ({usage['free_percent']:.1f}% free). Triggering cleanup...")
            self.perform_cleanup()
            return True
        
        return False


# Background monitoring function
def monitor_disk_health(interval_minutes=60):
    """
    Run background disk health monitoring
    
    Args:
        interval_minutes: Check interval in minutes
    """
    import time
    from threading import Thread
    
    manager = DiskCleanupManager(threshold_percent=20)
    
    def monitoring_loop():
        while True:
            try:
                manager.monitor_and_cleanup()
                time.sleep(interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Retry after 1 minute on error
    
    # Start monitoring in background thread
    monitor_thread = Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    logger.info(f"✅ Disk health monitoring started (checking every {interval_minutes} minutes)")
    
    return monitor_thread


if __name__ == "__main__":
    # Test the cleanup manager
    manager = DiskCleanupManager(threshold_percent=20)
    
    print("\n📊 Current Disk Status:")
    usage = manager.get_disk_usage()
    print(f"  Total: {usage['total']:.2f}GB")
    print(f"  Used: {usage['used']:.2f}GB ({usage['used']/usage['total']*100:.1f}%)")
    print(f"  Free: {usage['free']:.2f}GB ({usage['free_percent']:.1f}%)")
    
    if manager.should_cleanup():
        print("\n⚠️  Disk space is low! Running cleanup...")
        manager.perform_cleanup()
    else:
        print("\n✅ Disk space is healthy.")
