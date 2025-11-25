# CoinFlow Auto-Update Quick Guide

## 🔄 Three Ways to Keep Data Fresh

### 1. Dashboard Button (Easiest)
- Open dashboard: http://localhost:8501
- Click **"🔄 Refresh Data"** button
- Wait ~30 seconds for pipeline to run
- Dashboard auto-reloads with fresh data

### 2. Automated Daily Updates (Set & Forget)
```bash
cd /Users/rohita/nyc_taxi_jan_2025_pipeline/coinflow
./setup_cron.sh
```
- Runs automatically every day at 9:00 AM
- Logs saved to `logs/` folder
- No manual intervention needed

### 3. Manual Command Line
```bash
cd /Users/rohita/nyc_taxi_jan_2025_pipeline/coinflow
make run-pipeline && make dbt-run
```

## 📅 Data Freshness Indicator

The dashboard shows:
- **"Data last updated: 2025-11-24"** - Data is current
- **"No data found"** - Run refresh to fetch initial data

## 🔍 Checking Cron Status

```bash
# View all cron jobs
crontab -l

# View logs
tail -f ~/nyc_taxi_jan_2025_pipeline/coinflow/logs/pipeline.log
tail -f ~/nyc_taxi_jan_2025_pipeline/coinflow/logs/dbt.log
```

## 🗑️ Remove Cron Job

```bash
crontab -e
# Delete the line containing "coinflow"
```

## ⚙️ How It Works

1. **Refresh Button** → Runs `make run-pipeline` + `make dbt-run` → Clears cache → Reloads dashboard
2. **Cron Job** → Scheduled task runs commands daily → Logs output
3. **Dashboard Cache** → Refreshes every 5 minutes automatically

## 💡 Pro Tips

- **First time?** Click "🔄 Refresh Data" to fetch initial data
- **Daily updates?** Run `./setup_cron.sh` once and forget about it
- **Manual control?** Use the dashboard button anytime
- **Check freshness** Look at the timestamp at the top of the dashboard
