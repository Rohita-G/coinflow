# CoinFlow - Database Lock Fix

## The Problem

DuckDB only allows **one write connection** at a time. When the Streamlit dashboard is running, it holds a connection to the database, preventing the ingestion pipeline from writing new data.

## The Solution

### Option 1: Stop Dashboard Before Refreshing (Current Workaround)

```bash
# Stop the dashboard
pkill -f "streamlit run"

# Run the pipeline
make run-pipeline && make dbt-run

# Restart dashboard
make run-dashboard
```

### Option 2: Use the Dashboard Refresh Button (Recommended)

The dashboard now properly releases the database lock before running the pipeline:

1. Click **" Refresh Data"** in the dashboard
2. The dashboard clears all connections
3. Pipeline runs successfully
4. Dashboard reloads with fresh data

### Option 3: Run Pipeline in Separate Terminal

If the dashboard is running, you can still update data by:

1. Keep dashboard running
2. In a new terminal: `pkill -f streamlit` (stop dashboard temporarily)
3. Run: `make run-pipeline && make dbt-run`
4. Dashboard will auto-restart or manually restart it

## Technical Details

**Why does this happen?**
- DuckDB uses file-level locking for write operations
- Streamlit dashboard connects in read-only mode BUT the connection pool may still hold a lock
- The ingestion pipeline needs write access to add new data

**What I fixed:**
- Dashboard now uses `read_only=True` explicitly
- Refresh button clears ALL caches (`st.cache_resource.clear()`) to release connections
- Added timeouts to prevent hanging

## Best Practice

**For daily automation (cron):**
- The cron job runs when you're not using the dashboard
- No conflicts at 9:00 AM when it auto-updates

**For manual updates:**
- Use the dashboard refresh button
- Or stop dashboard → run pipeline → restart dashboard

## Verification

After the fix, the refresh button should work without errors. If you still see lock errors:

```bash
# Find the process holding the lock
lsof /Users/rohita/nyc_taxi_jan_2025_pipeline/coinflow.duckdb

# Kill it
kill -9 <PID>
```
