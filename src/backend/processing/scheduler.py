"""
Lightweight ETL Scheduler using APScheduler
Runs the blockchain ETL pipeline on a schedule (cron-like)
"""

import logging
import sys
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import main_etl for execution
try:
    from backend.etl.main_etl import BlockchainETL
except ImportError:
    logger.error("Failed to import main_etl. Ensure main_etl.py is in the correct location.")
    sys.exit(1)


def run_etl():
    """Execute the ETL pipeline"""
    logger.info("="*60)
    logger.info("Starting ETL Pipeline Execution")
    logger.info("="*60)
    
    try:
        etl = BlockchainETL()
        
        if not etl.initialize():
            logger.error("Failed to initialize ETL")
            return False
        
        if not etl.process_blocks():
            logger.error("ETL pipeline failed")
            return False
        
        etl.print_summary()
        logger.info("ETL Pipeline completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Unexpected error in ETL execution: {e}", exc_info=True)
        return False


def main():
    """Main scheduler entry point"""
    logger.info("Starting Blockchain ETL Scheduler")
    
    # Create scheduler
    scheduler = BlockingScheduler()
    
    # Get schedule from environment or use defaults
    schedule_hour = os.getenv('ETL_SCHEDULE_HOUR', '0')  # Default: midnight
    schedule_minute = os.getenv('ETL_SCHEDULE_MINUTE', '0')
    
    # Parse schedule
    try:
        hour = int(schedule_hour)
        minute = int(schedule_minute)
        logger.info(f"ETL scheduled for {hour:02d}:{minute:02d} daily")
    except ValueError:
        logger.error("Invalid ETL_SCHEDULE_HOUR or ETL_SCHEDULE_MINUTE")
        logger.info("Using default: 00:00 (midnight)")
        hour, minute = 0, 0
    
    # Schedule job
    scheduler.add_job(
        run_etl,
        CronTrigger(hour=hour, minute=minute),
        id='etl_pipeline',
        name='Blockchain ETL Pipeline',
        misfire_grace_time=600  # 10 minute grace period
    )
    
    # Also run on startup
    logger.info("Running ETL on startup...")
    run_etl()
    
    logger.info("Scheduler started. Waiting for next scheduled run...")
    logger.info("Press Ctrl+C to stop the scheduler")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
