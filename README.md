# CoinFlow: Crypto Data Lakehouse 

A production-grade Data Engineering pipeline for cryptocurrency market analysis, built with the Modern Data Stack (MDS).

##  Project Overview

CoinFlow demonstrates a complete end-to-end data pipeline:
- **Ingestion**: Fetch real-time crypto data from Yahoo Finance using `dlt`
- **Storage**: Store data in DuckDB (local analytical database)
- **Transformation**: Clean and model data using `dbt`
- **Visualization**: Interactive dashboard built with Streamlit

##  Architecture

```
Yahoo Finance API
       ↓
   dlt (Extract & Load)
       ↓
   DuckDB (Storage)
       ↓
   dbt (Transform)
       ↓
   Streamlit (Visualize)
```

##  Tech Stack

All tools are **100% free and open-source**:

| Layer | Tool | Purpose |
|-------|------|---------|
| **Ingestion** | `dlt` (Data Load Tool) | Automated data extraction and loading |
| **Storage** | DuckDB | Fast, embedded analytical database |
| **Transformation** | dbt | SQL-based data modeling and testing |
| **Visualization** | Streamlit | Interactive web dashboard |
| **Data Source** | yfinance | Free Yahoo Finance API wrapper |

##  Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Install dependencies
make setup

# Or manually:
pip install -r requirements.txt
```

##  Usage

### 1. Run the Ingestion Pipeline

Fetch the latest crypto data from Yahoo Finance:

```bash
make run-pipeline
```

This will:
- Fetch data for BTC, ETH, SOL, XRP, and DOGE
- Load OHLCV (Open, High, Low, Close, Volume) data into DuckDB
- Store data in `coinflow.duckdb`

### 2. Run dbt Transformations

Transform raw data into analytical models:

```bash
make dbt-run
```

This creates:
- **Staging**: `stg_crypto_ohlcv` - Cleaned and standardized data
- **Marts**: `crypto_daily_metrics` - Daily returns, moving averages, price changes

### 3. Launch the Dashboard

Start the Streamlit dashboard:

```bash
make run-dashboard
```

Then open http://localhost:8501 in your browser.

##  Dashboard Features

- **Real-time Price Tracking**: Current price with 24h change
- **Candlestick Charts**: Interactive price visualization
- **Moving Averages**: 7-day and 30-day trends
- **Daily Returns**: Bar chart showing daily performance
- **Historical Data Table**: Recent price history
- ** One-Click Refresh**: Manual data update button
- ** Data Freshness**: Shows last update timestamp
- ** Auto-Updates**: Optional daily automation via cron

##  Keeping Data Fresh

### Option 1: Manual Refresh (In Dashboard)

Click the **" Refresh Data"** button in the dashboard to fetch the latest prices. This will:
1. Run the ingestion pipeline
2. Execute dbt transformations
3. Reload the dashboard with fresh data

### Option 2: Automated Daily Updates (Recommended)

Set up a cron job to automatically refresh data every day:

```bash
# Run the setup script
./setup_cron.sh
```

This will:
- Schedule daily updates at 9:00 AM
- Log output to `logs/pipeline.log` and `logs/dbt.log`
- Keep your dashboard always up-to-date

**Manual cron setup** (if you prefer):
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /Users/rohita/nyc_taxi_jan_2025_pipeline/coinflow && make run-pipeline && make dbt-run
```

### Option 3: Manual Command Line

```bash
cd coinflow
make run-pipeline  # Fetch latest data
make dbt-run       # Transform data
# Dashboard auto-refreshes after 5 minutes
```

##  Project Structure

```
coinflow/
├── pipelines/
│   └── crypto_source.py      # dlt ingestion pipeline
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_crypto_ohlcv.sql
│   │   └── marts/
│   │       └── crypto_daily_metrics.sql
│   ├── dbt_project.yml
│   └── profiles.yml
├── app/
│   └── dashboard.py          # Streamlit dashboard
├── requirements.txt
├── Makefile
└── README.md
```

##  Complete Workflow

Run the entire pipeline from scratch:

```bash
# 1. Ingest data
make run-pipeline

# 2. Transform data
make dbt-run

# 3. Launch dashboard
make run-dashboard
```

##  Data Models

### Staging Layer

**`stg_crypto_ohlcv`**: Cleaned OHLCV data
- Standardized column names
- Type casting
- Date formatting

### Marts Layer

**`crypto_daily_metrics`**: Analytical metrics
- Daily return percentage
- Day-over-day change
- 7-day moving average
- 30-day moving average
- Daily price range

## 🎓 Learning Outcomes

This project demonstrates:

1. **Modern Data Stack (MDS)** patterns
2. **ELT** (Extract, Load, Transform) vs traditional ETL
3. **Incremental data loading** with dlt
4. **SQL-based transformations** with dbt
5. **Analytical database** usage (DuckDB)
6. **Data visualization** best practices

##  Upgrade from NYC Taxi Project

| Feature | NYC Taxi | CoinFlow |
|---------|----------|----------|
| Data Source | Static CSV | Live API |
| Ingestion | Manual pandas | Automated dlt |
| Storage | MySQL | DuckDB |
| Transformation | Python scripts | dbt (SQL) |
| Orchestration | None | Makefile |
| Schema Evolution | Manual | Automatic |
| Data Quality | None | dbt tests |

##  Future Enhancements

- [ ] Add real-time WebSocket streaming
- [ ] Implement data quality tests (dbt tests)
- [ ] Add more cryptocurrencies
- [ ] Deploy to cloud (DuckDB → Snowflake/BigQuery)
- [ ] Add Airflow/Dagster orchestration
- [ ] Implement alerting (price thresholds)

##  Notes

- **Data Freshness**: Run `make run-pipeline` daily to get latest data
- **Free Tier**: All tools are free with no API limits
- **Local First**: Everything runs on your machine, no cloud required
- **Portable**: Can easily move to cloud databases later

##  Contributing

This is a learning project! Feel free to:
- Add more cryptocurrencies
- Implement additional metrics
- Improve the dashboard UI
- Add data quality tests

##  License

MIT License - Feel free to use this for learning and portfolio projects!

---

**Built with  as a Modern Data Stack learning project**
