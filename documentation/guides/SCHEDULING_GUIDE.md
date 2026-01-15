# Automated Scheduling Guide

## Option 1: Using Python Scheduler (Recommended)

### Quick Start
```bash
python scheduler.py
```

This runs the ETL pipeline:
- **Immediately on startup**
- **Daily at 00:00 (midnight)** by default
- **Continuously monitoring** for next scheduled run

### Configure Schedule

```bash
# Run daily at 6 AM
export ETL_SCHEDULE_HOUR=6
export ETL_SCHEDULE_MINUTE=0
python scheduler.py

# Run every 12 hours (noon and midnight)
# You'd need to modify scheduler.py to support multiple times
```

### Docker Integration

```bash
# Run scheduler in background
docker-compose exec app python scheduler.py &

# Or add to docker-compose.yml:
services:
  etl-scheduler:
    build: .
    command: python scheduler.py
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/blockchain_db
      RPC_URL: https://eth-mainnet.g.alchemy.com/v2/...
      ETL_SCHEDULE_HOUR: 6
      ETL_SCHEDULE_MINUTE: 0
    depends_on:
      - postgres
```

---

## Option 2: Using System Cron

### Setup Cron Job

```bash
# Open crontab editor
crontab -e

# Add this line to run daily at 6 AM:
0 6 * * * cd /home/sugangokul/Desktop/blockchain-ml && python main_etl.py >> /var/log/etl.log 2>&1

# Common cron schedules:
# Every hour:
0 * * * * ...

# Every 6 hours:
0 */6 * * * ...

# Daily at midnight:
0 0 * * * ...

# Daily at 6 AM:
0 6 * * * ...

# Every weekday at 8 AM:
0 8 * * 1-5 ...

# Every Sunday at 2 AM:
0 2 * * 0 ...
```

### View Cron Jobs

```bash
# List your cron jobs
crontab -l

# View cron logs
sudo tail -f /var/log/syslog | grep CRON
```

### Remove Cron Job

```bash
# Open crontab
crontab -e

# Delete the line, save and exit

# Or remove all cron jobs:
crontab -r
```

---

## Option 3: Using Docker with Cron

### Create Cron Script

```bash
# Create run_etl.sh
#!/bin/bash
cd /home/sugangokul/Desktop/blockchain-ml
docker-compose exec -T app python main_etl.py
```

### Make Executable

```bash
chmod +x run_etl.sh
```

### Add to Crontab

```bash
crontab -e

# Add:
0 6 * * * /home/sugangokul/Desktop/blockchain-ml/run_etl.sh >> /var/log/etl.log 2>&1
```

---

## Option 4: Using Systemd Timer (Linux)

### Create Service File

```bash
sudo nano /etc/systemd/system/blockchain-etl.service
```

```ini
[Unit]
Description=Blockchain ETL Pipeline
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=sugangokul
WorkingDirectory=/home/sugangokul/Desktop/blockchain-ml
ExecStart=/usr/bin/python3 /home/sugangokul/Desktop/blockchain-ml/main_etl.py
Restart=on-failure
RestartSec=300

[Install]
WantedBy=multi-user.target
```

### Create Timer File

```bash
sudo nano /etc/systemd/system/blockchain-etl.timer
```

```ini
[Unit]
Description=Blockchain ETL Pipeline Timer
Requires=blockchain-etl.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

### Enable Timer

```bash
sudo systemctl daemon-reload
sudo systemctl enable blockchain-etl.timer
sudo systemctl start blockchain-etl.timer

# Check status
sudo systemctl status blockchain-etl.timer

# View logs
journalctl -u blockchain-etl.service -f
```

---

## Monitoring Scheduled Runs

### Python Scheduler Logs

```bash
# Real-time logs
docker-compose logs -f app

# Filter for ETL runs
docker-compose logs app | grep "Starting ETL Pipeline"
```

### Cron Job Logs

```bash
# View all cron activity
sudo tail -f /var/log/syslog | grep CRON

# View ETL job output
tail -f /var/log/etl.log
```

### Database Verification

```sql
-- Check last run
SELECT MAX(updated_at) FROM pipeline_state;

-- Check today's data
SELECT COUNT(*) FROM transaction_receipts 
WHERE DATE(created_at) = CURRENT_DATE;

-- Check last block processed
SELECT last_block FROM pipeline_state;
```

---

## Recommended Configuration

| Use Case | Recommendation | Schedule |
|----------|-----------------|----------|
| **Development** | Python Scheduler | Run on startup + hourly |
| **Production** | Systemd Timer | Daily at 6 AM |
| **Cloud** | Cron in container | Daily at midnight UTC |
| **Testing** | Manual runs | As needed |

---

## Quick Setup (Copy-Paste)

### 1. Run Python Scheduler Now
```bash
cd /home/sugangokul/Desktop/blockchain-ml
python scheduler.py
```

### 2. Or Setup Cron (Run at 6 AM daily)
```bash
crontab -e
# Add line: 0 6 * * * cd /home/sugangokul/Desktop/blockchain-ml && python main_etl.py >> /var/log/etl.log 2>&1
```

### 3. Or Run in Docker
```bash
docker-compose up -d  # Start services
docker-compose exec app python scheduler.py &  # Start scheduler in background
docker-compose logs -f app  # Watch logs
```

---

## Troubleshooting

### Cron job not running
```bash
# Check cron daemon is running
sudo systemctl status cron

# Verify crontab is set
crontab -l

# Check permissions
ls -la /var/spool/cron/crontabs/

# Test cron command manually
cd /home/sugangokul/Desktop/blockchain-ml && python main_etl.py
```

### Permission denied
```bash
# Make script executable
chmod +x run_etl.sh
chmod +x scheduler.py
```

### Python not found in cron
```bash
# Use absolute path in crontab
which python3
# /usr/bin/python3

# Update crontab with full path:
0 6 * * * /usr/bin/python3 /home/sugangokul/Desktop/blockchain-ml/main_etl.py
```

### PostgreSQL connection in cron
```bash
# Ensure DATABASE_URL is set in crontab environment
# Add to top of crontab:
DATABASE_URL=postgresql://user:password@localhost:5432/blockchain_db

# Or set in .env file and source it:
0 6 * * * cd /home/sugangokul/Desktop/blockchain-ml && source .env && python main_etl.py
```

---

## Example Schedule Matrix

| Schedule | Cron | Time |
|----------|------|------|
| Every hour | `0 * * * *` | 00:00, 01:00, 02:00... |
| Every 6 hours | `0 */6 * * *` | 00:00, 06:00, 12:00, 18:00 |
| Daily at 6 AM | `0 6 * * *` | 06:00 every day |
| Weekdays at 9 AM | `0 9 * * 1-5` | 09:00 Mon-Fri |
| Weekends at 2 AM | `0 2 * * 0,6` | 02:00 Sat-Sun |
| 1st of month | `0 0 1 * *` | 00:00 on 1st |

---

## Next Steps

1. **Choose scheduling method** (Python scheduler recommended for testing)
2. **Test one run**: `python main_etl.py`
3. **Set up schedule**: `python scheduler.py` or cron job
4. **Monitor logs**: Watch for successful daily executions
5. **Verify data**: Check PostgreSQL for daily inserts

**Your ETL is now automated! 🚀**
