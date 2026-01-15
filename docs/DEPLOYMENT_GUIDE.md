# Deployment Guide - Blockchain ETL Pipeline

## 🚀 Ready for Deployment

Your complete blockchain ETL pipeline is ready to deploy to production.

---

## Pre-Deployment Checklist

- [x] All code files created and tested
- [x] Docker configuration complete
- [x] PostgreSQL schema designed
- [x] Error handling implemented
- [x] Logging configured
- [x] Documentation complete
- [x] Test suite included
- [x] Environment variables configured

---

## Deployment Option 1: Docker (Recommended)

### Quick Start (60 seconds)

```bash
cd /home/sugangokul/Desktop/blockchain-ml

# Start all services
docker-compose up --build

# Monitor logs
docker-compose logs -f app
```

### What Happens

1. **Build Phase** (~2-3 minutes)
   - Creates Python 3.11-slim image
   - Installs dependencies from requirements.txt
   - Compiles system packages for PostgreSQL

2. **Startup Phase** (~30 seconds)
   - PostgreSQL starts and initializes
   - Creates blockchain_db database
   - Python app connects and creates tables

3. **Processing Phase**
   - Extracts latest block transactions
   - Transforms data with Pandas
   - Loads into PostgreSQL
   - Updates pipeline state
   - Logs completion

### Verify It Works

```bash
# Check app is running
docker-compose ps

# View real-time logs
docker-compose logs -f app

# Expected output:
# Connected to PostgreSQL via SQLAlchemy
# Connected to Web3
# Processing block: 24237712
# Extracted 711 transactions
# Transformed 711 rows
# LOAD: Successfully inserted 711 rows
# Updated pipeline_state: last_block = 24237712
```

### Connect to Database

```bash
# Access PostgreSQL CLI
docker-compose exec postgres psql -U user -d blockchain_db

# Useful queries:
SELECT COUNT(*) FROM transaction_receipts;
SELECT * FROM pipeline_state;
SELECT status, COUNT(*) FROM transaction_receipts GROUP BY status;
```

### Stop Services

```bash
# Stop without removing data
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove everything (including data)
docker-compose down -v
```

---

## Deployment Option 2: Local Development

### Prerequisites

```bash
# Python 3.11+
python3 --version

# PostgreSQL 15+
psql --version

# Install Python dependencies
pip install -r requirements.txt
```

### Setup PostgreSQL

```bash
# Create database and user
psql -U postgres -c "CREATE DATABASE blockchain_db;"
psql -U postgres -c "CREATE USER user WITH PASSWORD 'password';"
psql -U postgres -c "ALTER ROLE user WITH CREATEDB;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE blockchain_db TO user;"
```

### Run Application

```bash
# Single block processing
python fetch_and_store.py

# Or batch processing
python main_etl.py

# Or continuous processing (run in cron/systemd)
while true; do
    python main_etl.py
    sleep 3600  # Run every hour
done
```

---

## Deployment Option 3: Cloud (AWS/Azure/GCP)

### Option 3A: AWS ECS + RDS

**Architecture:**
- ECS Task: Runs Python Docker image
- RDS: Managed PostgreSQL
- CloudWatch: Logs aggregation
- EventBridge: Triggers (hourly, etc.)

**Steps:**
1. Push Docker image to ECR: `docker tag blockchainml:latest <account>.dkr.ecr.us-east-1.amazonaws.com/blockchainml:latest && docker push ...`
2. Create ECS Task Definition with image
3. Create RDS PostgreSQL instance
4. Create EventBridge rule to trigger every hour
5. Configure IAM roles for RDS access

### Option 3B: Azure Container Instances + Azure Database for PostgreSQL

**Steps:**
1. Push image to Azure Container Registry
2. Create Azure Database for PostgreSQL
3. Create Container Instance with image
4. Configure environment variables
5. Set up Logic Apps for scheduling

### Option 3C: Google Cloud Run + Cloud SQL

**Steps:**
1. Push image to Google Cloud Registry
2. Create Cloud SQL PostgreSQL instance
3. Deploy to Cloud Run with image
4. Configure Cloud Scheduler for triggers
5. Set environment variables via Cloud Run console

---

## Production Configuration

### Environment Variables

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@your-host:5432/blockchain_db

# Ethereum RPC (get your own key from Alchemy/Infura)
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Processing
BATCH_SIZE=10  # Blocks per run (adjust for memory/speed)
```

### Performance Tuning

| Parameter | Value | Effect |
|-----------|-------|--------|
| BATCH_SIZE | 10 | Processes 10 blocks = ~7k txns = 50MB memory |
| BATCH_SIZE | 5 | Smaller batches, slower overall, lower memory |
| BATCH_SIZE | 20 | Larger batches, faster, higher memory (100MB+) |

### Data Retention Policy

```bash
# Default (implemented in code):
- Keep 5 days of data
- Emergency cleanup if disk < 1GB
- Delete local receipts/ directory

# To modify, edit fetch_and_store.py:
five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)  # ← Change this
```

### Scheduling

#### Option 1: Docker with Cron
```bash
# Edit crontab: crontab -e
# Run every hour
0 * * * * cd /path/to/blockchain-ml && docker-compose exec app python main_etl.py
```

#### Option 2: Systemd Timer
```bash
# Create /etc/systemd/system/etl.service
[Unit]
Description=Blockchain ETL Pipeline
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/sugangokul/Desktop/blockchain-ml
ExecStart=/usr/bin/docker-compose exec app python main_etl.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

# Then: sudo systemctl enable etl.timer && sudo systemctl start etl.timer
```

#### Option 3: Cloud Scheduler
- **AWS**: EventBridge rule → ECS task
- **Azure**: Logic Apps → Container Instance
- **GCP**: Cloud Scheduler → Cloud Run

---

## Monitoring & Alerts

### Check Status

```bash
# Docker
docker-compose ps

# Database
SELECT COUNT(*) FROM transaction_receipts;
SELECT MAX(last_block) FROM pipeline_state;

# Recent errors
docker-compose logs app | grep ERROR

# Performance
docker-compose stats
```

### Set Up Alerting

**Option 1: Docker Logs Aggregation**
```bash
# ELK Stack (Elasticsearch, Logstash, Kibana)
# Fluentd to centralized logging
# Prometheus metrics export
```

**Option 2: Database Monitoring**
```sql
-- Alert if no data for 24 hours
SELECT CASE 
  WHEN EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) > 86400 
  THEN 'ALERT: No data for 24 hours'
  ELSE 'OK'
END
FROM transaction_receipts;

-- Alert if last_block stalled
SELECT CASE
  WHEN EXTRACT(EPOCH FROM (NOW() - updated_at)) > 3600 
  THEN 'ALERT: Pipeline stalled'
  ELSE 'OK'
END
FROM pipeline_state;
```

### Health Check

```bash
# Script: health_check.sh
#!/bin/bash

DB_COUNT=$(psql -h localhost -U user -d blockchain_db -c "SELECT COUNT(*) FROM transaction_receipts;" | tail -1)

if [ "$DB_COUNT" -gt 0 ]; then
    echo "✓ Pipeline healthy: $DB_COUNT transactions"
    exit 0
else
    echo "✗ Pipeline unhealthy: No data"
    exit 1
fi
```

---

## Scaling Considerations

### Horizontal Scaling
- Add multiple app containers with load balancer
- Each processes different block ranges
- Use database write-ahead logs for sync

### Vertical Scaling
- Increase BATCH_SIZE for faster processing
- Increase PostgreSQL memory/CPU
- Increase RPC provider tier for better rate limits

### Data Archival
```sql
-- Archive old data to separate table
CREATE TABLE transaction_receipts_archive AS 
SELECT * FROM transaction_receipts 
WHERE created_at < NOW() - INTERVAL '30 days';

DELETE FROM transaction_receipts 
WHERE created_at < NOW() - INTERVAL '30 days';
```

---

## Disaster Recovery

### Backup Strategy

```bash
# Docker volume backup
docker-compose exec postgres pg_dump -U user blockchain_db > backup_$(date +%Y%m%d).sql

# Or use PostgreSQL built-in
docker-compose exec postgres pg_dump -U user blockchain_db | gzip > backup.sql.gz

# Restore from backup
gunzip < backup.sql.gz | docker-compose exec -T postgres psql -U user blockchain_db
```

### Failure Scenarios

**Scenario 1: Database Crashes**
- Tables are recreated automatically on restart
- Data retained in Docker volume
- No action needed - just restart

**Scenario 2: RPC Provider Down**
- Pipeline fails with clear error
- State saved (last_block preserved)
- Resumes automatically when RPC recovers
- Switch RPC_URL if provider offline

**Scenario 3: Disk Full**
- Emergency cleanup runs automatically
- Deletes all except today's data
- Creates space for new data
- Review cleanup logs for action

**Scenario 4: Data Corruption**
- Restore from backup using procedure above
- Reset pipeline_state to last known good block
- Resume processing from that point

---

## Maintenance Tasks

### Daily
- Monitor logs for errors: `docker-compose logs app`
- Check record count: `SELECT COUNT(*) FROM transaction_receipts;`
- Verify pipeline state: `SELECT last_block FROM pipeline_state;`

### Weekly
- Review disk usage: `df -h`
- Check database size: `SELECT pg_size_pretty(pg_database_size('blockchain_db'));`
- Backup database: `pg_dump ...`

### Monthly
- Archive old data (>30 days)
- Review and update BATCH_SIZE if needed
- Check for code updates
- Rotate logs if using log aggregation

---

## Security Considerations

### Before Production Deployment

- [ ] Change default PostgreSQL password
- [ ] Store credentials in secure vault (AWS Secrets, Azure KeyVault)
- [ ] Use VPN/private network for database
- [ ] Enable SSL for database connections
- [ ] Restrict RPC endpoint usage (API keys)
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates

### Secure Credentials

```bash
# Option 1: Environment variables (Docker Secrets)
docker secret create db_password -
echo 'your-password' | docker secret create db_password -

# Option 2: AWS Secrets Manager
aws secretsmanager create-secret --name blockchain-etl --secret-string '{...}'

# Option 3: .env file (local only, not in production)
# Never commit .env to git
echo "DATABASE_URL=..." > .env
echo ".env" >> .gitignore
```

---

## Support & Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `psql: connection refused` | PostgreSQL not running - check `docker-compose ps` |
| `Web3 connection failed` | RPC endpoint issue - verify `RPC_URL` and API key |
| `Duplicate key error` | Normal - already processed - check `pipeline_state` |
| `Out of memory` | Reduce `BATCH_SIZE` environment variable |
| `Disk full` | Automatic cleanup runs, review logs |

### Debug Mode

```bash
# Add verbose logging
export LOG_LEVEL=DEBUG

# Run with console output
docker-compose up --build (no -d flag for foreground)

# Check logs
docker-compose logs app --tail=100
```

### Get Help

1. Check [README.md](README.md) - Overview
2. Check [QUICKSTART.md](QUICKSTART.md) - Quick reference
3. Check [ETL_PIPELINE.md](ETL_PIPELINE.md) - Technical details
4. Run [test_etl.py](test_etl.py) - Validation suite
5. Check logs - `docker-compose logs -f app`

---

## Deployment Checklist

Before going live:

- [ ] Docker builds successfully
- [ ] All services start without errors
- [ ] PostgreSQL connected
- [ ] Web3 connected
- [ ] First ETL cycle completes
- [ ] Data appears in database
- [ ] test_etl.py passes all tests
- [ ] Credentials stored securely
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Runbooks documented
- [ ] Team trained on operation

---

## Post-Deployment

### First 24 Hours
1. Monitor logs continuously
2. Verify data insertion rate
3. Check for errors or warnings
4. Validate database growth
5. Test failover procedures

### First Week
1. Collect baseline metrics
2. Fine-tune BATCH_SIZE if needed
3. Adjust scheduling if needed
4. Review and document any issues
5. Train team on monitoring

### Ongoing
1. Monthly backups
2. Quarterly security review
3. Annual capacity planning
4. Continuous improvement

---

## Success Criteria

✅ **Deployment is successful when:**
- Docker containers running without restarts
- ETL cycles complete every scheduled interval
- Transactions appear in database
- pipeline_state tracking works
- Logs show no errors
- Performance within acceptable range
- Backups working
- Team trained and confident

---

**🚀 Ready to deploy!**

Next step: `docker-compose up --build`

Questions? See [ETL_PIPELINE.md](ETL_PIPELINE.md) for detailed documentation.
