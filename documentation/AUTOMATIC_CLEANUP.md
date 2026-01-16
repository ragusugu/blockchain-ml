# Automatic Disk Cleanup System

## Overview

The blockchain-ml application now includes an **automatic disk cleanup system** that monitors disk space and cleans up old files when space runs low.

## Features

✅ **Automatic Monitoring** - Background thread checks disk every 60 minutes
✅ **Threshold-Based Cleanup** - Triggered when free space drops below 20%
✅ **Intelligent Cleanup** - Removes old logs, temp files, and unused Docker images
✅ **Manual Control** - Can be triggered manually via CLI
✅ **Kubernetes Integration** - Scheduled cleanup via CronJob
✅ **No Service Disruption** - Cleanup runs without affecting running services

## How It Works

### 1. Automatic Background Monitoring

The Flask backend automatically starts disk monitoring on initialization:

```python
# Runs every 60 minutes
monitor_disk_health(interval_minutes=60)
```

**Cleanup Trigger Points:**
- On every `/api/transactions` request (checks if cleanup needed)
- Background monitoring thread (every 60 minutes)

### 2. Cleanup Actions

When triggered, the cleanup performs:

1. **Remove Old Logs** (>7 days old)
   - `/tmp/*.log`
   - `/tmp/tunnel*`
   - `/var/tmp` files

2. **Docker System Cleanup**
   - Prune unused images
   - Remove dangling containers
   - Clean build cache
   - Clean volumes

3. **Typical Freed Space**
   - 1-5 GB per cleanup (depends on accumulation)
   - Full system prune can free 25+ GB

## Usage

### Automatic (Default)

Just run the Flask backend normally - monitoring starts automatically:

```bash
python src/backend/api/ai_dashboard.py
```

Check logs for cleanup messages:
```
✅ Automatic disk monitoring started (checking every 60 minutes)
📊 Current disk usage: 66.00GB / 196.00GB (33.7% used, 66.3% free)
```

### Manual Cleanup - Check Status

```bash
python cleanup_disk.py --status
```

Output:
```
📊 Disk Status:
   Total: 196.00GB
   Used:  66.00GB (33.7%)
   Free:  120.00GB (61.2%)
   Threshold: 20%

✅ Disk space is healthy. No cleanup needed.
```

### Manual Cleanup - Force Now

```bash
python cleanup_disk.py --cleanup-now
```

Output:
```
📊 Disk Status:
   Total: 196.00GB
   Used:  102.00GB (52.0%)
   Free:  94.00GB (48.0%)
   Threshold: 20%

🔧 Force cleanup requested. Running cleanup...

🗑️  Deleted: /tmp/old_log.log (50.5MB)
✅ Cleaned /tmp: 512.5MB
✅ Cleaned /var/tmp: 256.3MB
🧹 Running docker system prune...
✅ Docker cleanup successful

📊 Disk usage after cleanup: 66.00GB / 196.00GB (33.7%)
✨ Total space freed: 25.26GB
```

### Manual Cleanup - Custom Threshold

```bash
python cleanup_disk.py --cleanup-now --threshold 30
```

Cleanup triggered if free space is below 30%.

## Kubernetes Integration

### Deploy Cleanup CronJob

```bash
kubectl apply -f k8s-cleanup-job.yaml
```

This creates:
1. **CronJob** - Runs cleanup daily at 2 AM (UTC)
2. **Manual Job** - For immediate cleanup testing

### Check Cleanup Status

```bash
# View CronJob
kubectl get cronjobs -n blockchain-ml
kubectl describe cronjob disk-cleanup-job -n blockchain-ml

# View Job runs
kubectl get jobs -n blockchain-ml
kubectl logs -n blockchain-ml job/disk-cleanup-immediate
```

### Manual Cleanup in Kubernetes

```bash
# Trigger cleanup job now
kubectl create job --from=cronjob/disk-cleanup-job manual-cleanup -n blockchain-ml

# View status
kubectl get jobs -n blockchain-ml -w
```

## Configuration

### Environment Variables

Add to `.env` or docker-compose.yml:

```bash
# Disk cleanup threshold (%)
DISK_CLEANUP_THRESHOLD=20

# Monitoring interval (minutes)
DISK_CLEANUP_INTERVAL=60

# Max log age (days)
LOG_RETENTION_DAYS=7
```

### Code Configuration

In `src/backend/api/ai_dashboard.py`:

```python
# Initialize with custom threshold
cleanup_manager = DiskCleanupManager(threshold_percent=25)

# Start monitoring with custom interval
monitor_disk_health(interval_minutes=120)
```

## Monitoring & Logging

### Check Cleanup Logs

```bash
# Docker logs
docker logs <backend-container> | grep -i cleanup

# Kubernetes logs
kubectl logs -n blockchain-ml -l app=backend | grep -i cleanup

# Follow logs in real-time
kubectl logs -n blockchain-ml -l app=backend -f | grep -i cleanup
```

### Cleanup Events

Look for these log messages:

```
✅ Automatic disk monitoring started (checking every 60 minutes)
📊 Current disk usage: X.XXGB / X.XXGB (X.X% used, X.X% free)
✅ Disk space is healthy.
⚠️  Disk space low (19.2% free). Triggering cleanup...
🗑️  Deleted: /tmp/file.log (50.5MB)
✅ Cleaned /tmp: 512.5MB
🧹 Running docker system prune...
✨ Total space freed: 25.26GB
```

## Troubleshooting

### Cleanup Not Running

1. **Check if monitoring started:**
   ```bash
   docker logs <backend> | grep "disk monitoring started"
   ```

2. **Force manual cleanup:**
   ```bash
   python cleanup_disk.py --cleanup-now
   ```

3. **Check permissions:**
   - Backend container needs `CAP_SYS_ADMIN` for Docker operations
   - Check Dockerfile includes `docker` CLI

### Cleanup Taking Too Long

- Cleanup runs in background, doesn't block API
- Docker prune can take 30-60 seconds
- Large volumes increase cleanup time

### Low Disk Space Warning Still Shows

- Threshold set too high (default 20%)
- Reduce threshold: `--threshold 10`
- Or run more frequent cleanup: `interval_minutes=30`

## Performance Impact

- **Monitoring Check**: <100ms per request
- **Cleanup Duration**: 30-120 seconds (runs asynchronously)
- **API Response Time**: Not affected (cleanup runs in background)

## Best Practices

1. **Set Appropriate Threshold**
   - Default 20% works for most cases
   - Reduce to 15% for aggressive cleanup
   - Increase to 25% for conservative approach

2. **Monitoring Interval**
   - Default 60 minutes is adequate
   - Reduce to 30 minutes if disk fills quickly
   - Increase to 120 minutes for stable systems

3. **Manual Checks**
   - Check status weekly: `python cleanup_disk.py --status`
   - Review logs for cleanup events
   - Monitor available disk space trends

4. **Production Deployment**
   - Enable CronJob for automated cleanup
   - Set up alerting if free space < 10%
   - Review disk space capacity planning

## Related Commands

```bash
# Check current disk usage
df -h

# Docker space breakdown
docker system df

# Check logs directory size
du -sh /home/sugangokul/Desktop/blockchain-ml/logs

# List old files (>7 days)
find /tmp -type f -mtime +7

# Manual Docker cleanup (not recommended, use utility instead)
docker system prune -af --volumes
```

## Architecture

```
┌─────────────────────────────────┐
│   Flask Backend (ai_dashboard)  │
└──────────────┬──────────────────┘
               │ imports
               ▼
┌──────────────────────────────────┐
│  DiskCleanupManager              │
│  (src/backend/utils/disk_cleanup)│
├──────────────────────────────────┤
│  • monitor_disk_health()         │
│  • should_cleanup()              │
│  • perform_cleanup()             │
│  • cleanup_directory()           │
│  • cleanup_docker_system()       │
└────────┬──────────────┬──────────┘
         │              │
    ┌────▼─────┐   ┌───▼──────┐
    │ Async    │   │  Called  │
    │ Monitor  │   │  per API │
    │ Thread   │   │  request │
    │ (60min)  │   │  (check) │
    └──────────┘   └──────────┘
```

## API Endpoints (Automatic)

All endpoints automatically trigger disk space check:

- `POST /api/transactions` - Checks before processing
- Other endpoints - Can also be added

No explicit disk cleanup API endpoint (for security), but manual triggers via:
- CLI: `python cleanup_disk.py`
- K8s Job: `kubectl create job ...`
- Cron: Scheduled CronJob

## Support & Issues

For issues with automatic cleanup:

1. **Check backend logs**: `kubectl logs -n blockchain-ml -l app=backend`
2. **Test manually**: `python cleanup_disk.py --cleanup-now`
3. **Verify Docker access**: Backend container needs Docker socket mount
4. **Check K8s permissions**: ServiceAccount needs appropriate RBAC

---

**Last Updated**: 2026-01-16
**Version**: 1.0
