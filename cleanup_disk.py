#!/usr/bin/env python3
"""
Standalone disk cleanup utility script
Can be run manually or scheduled via cron
"""
import sys
import os
import argparse
from datetime import datetime

# Add to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src/backend'))

from src.backend.utils.disk_cleanup import DiskCleanupManager

def main():
    parser = argparse.ArgumentParser(description='Disk Cleanup Utility')
    parser.add_argument('--threshold', type=int, default=20, 
                      help='Trigger cleanup if free space below this % (default: 20)')
    parser.add_argument('--cleanup-now', action='store_true',
                      help='Run cleanup immediately regardless of space usage')
    parser.add_argument('--status', action='store_true',
                      help='Show disk status only')
    
    args = parser.parse_args()
    
    manager = DiskCleanupManager(threshold_percent=args.threshold)
    
    print(f"\n{'='*60}")
    print(f"🧹 Disk Cleanup Utility - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Show status
    usage = manager.get_disk_usage()
    if usage:
        print(f"📊 Disk Status:")
        print(f"   Total: {usage['total']:.2f}GB")
        print(f"   Used:  {usage['used']:.2f}GB ({usage['used']/usage['total']*100:.1f}%)")
        print(f"   Free:  {usage['free']:.2f}GB ({usage['free_percent']:.1f}%)")
        print(f"   Threshold: {args.threshold}%\n")
        
        if args.status:
            print("✅ Status check complete. Exiting.\n")
            return 0
        
        # Decide whether to cleanup
        should_cleanup = manager.should_cleanup() or args.cleanup_now
        
        if should_cleanup:
            if args.cleanup_now:
                print("🔧 Force cleanup requested. Running cleanup...\n")
            else:
                print(f"⚠️  Disk space low ({usage['free_percent']:.1f}% free). Running cleanup...\n")
            
            manager.perform_cleanup()
            print(f"\n✨ Cleanup complete!\n")
        else:
            print(f"✅ Disk space is healthy. No cleanup needed.\n")
        
        return 0
    else:
        print("❌ Error: Could not determine disk usage\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
