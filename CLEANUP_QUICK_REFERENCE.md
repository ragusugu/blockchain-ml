# 🧹 Automatic Disk Cleanup - Quick Reference

## Status Check (No Cleanup)

```bash
./cleanup.sh --status
```

Shows current disk usage and threshold status.

## Force Cleanup Now

```bash
./cleanup.sh --cleanup-now
```

Runs cleanup regardless of current space usage.

## Custom Threshold

```bash
./cleanup.sh --cleanup-now --threshold 30
```

Sets custom threshold (30% in this example).

## What Gets Cleaned?

- ✅ Old log files (>7 days)
- ✅ Temporary files in `/tmp` and `/var/tmp`
- ✅ Unused Docker images
- ✅ Docker build cache
- ✅ Dangling volumes

## Automatic Monitoring

The Flask backend **automatically** monitors disk space:

- **Interval**: Every 60 minutes
- **Threshold**: 20% free space
- **Trigger**: On API requests when threshold reached
- **Action**: Cleanup runs in background

No manual intervention needed - just start the backend!

## Quick Commands

```bash
# Check status
./cleanup.sh --status

# Force cleanup
./cleanup.sh --cleanup-now

# Check disk usage
df -h

# Check Docker space
docker system df

# View backend logs (Kubernetes)
kubectl logs -n blockchain-ml -l app=backend | grep -i cleanup
```

## Default Settings

- **Threshold**: 20% free space
- **Monitor Interval**: 60 minutes
- **Log Retention**: 7 days
- **Cleanup on**: Every `/api/transactions` request (if needed)

## Configuration

Settings in [ai_dashboard.py](src/backend/api/ai_dashboard.py):

```python
cleanup_manager = DiskCleanupManager(threshold_percent=20)
monitor_disk_health(interval_minutes=60)
```

## Need Help?

📖 Full documentation: [AUTOMATIC_CLEANUP.md](documentation/AUTOMATIC_CLEANUP.md)

## Example Output

```
============================================================
🧹 Disk Cleanup Utility - 2026-01-16 12:55:19
============================================================

📊 Disk Status:
   Total: 195.80GB
   Used:  65.84GB (33.6%)
   Free:  119.94GB (61.3%)
   Threshold: 20%

✅ Status check complete. Exiting.
```

When cleanup is triggered:
```
⚠️  Disk space low (19.2% free). Running cleanup...

🗑️  Deleted: /tmp/old_log.log (50.5MB)
✅ Cleaned /tmp: 512.5MB
🧹 Running docker system prune...
✅ Docker cleanup successful

📊 Disk usage after cleanup: 66.00GB / 196.00GB (33.7%)
✨ Total space freed: 25.26GB
```
