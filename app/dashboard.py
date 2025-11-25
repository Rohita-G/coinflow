import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import subprocess
import os
import sys

# Page config
st.set_page_config(
    page_title="CoinFlow - Crypto Analytics",
    page_icon="",
    layout="wide"
)

# Connect to DuckDB
@st.cache_resource
def get_connection():
    # Use read_only to avoid locking the database
    # Use relative path for portability (works locally and on Streamlit Cloud)
    import os
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'coinflow.duckdb')
    
    # Check if database exists
    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}. Please run the ingestion pipeline first.")
        return None
    
    return duckdb.connect(db_path, read_only=True)

# Get last updated timestamp
@st.cache_data(ttl=60)
def get_last_updated():
    conn = get_connection()
    if conn is None:
        return None
    try:
        result = conn.execute("""
            SELECT MAX(metric_date) as last_date
            FROM main.crypto_daily_metrics
        """).fetchone()
        return result[0] if result else None
    except:
        return None

# Load data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    conn = get_connection()
    if conn is None:
        return None
    df = conn.execute("""
        SELECT 
            symbol,
            metric_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            daily_return_pct,
            day_over_day_change_pct,
            ma_7day,
            ma_30day
        FROM main.crypto_daily_metrics
        ORDER BY symbol, metric_date
    """).df()
    return df

# Function to refresh data
def refresh_data():
    """Run the data pipeline and dbt transformations"""
    import os
    project_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Clear all caches and close connections to release database lock
    st.cache_data.clear()
    st.cache_resource.clear()
    
    with st.spinner(' Fetching latest crypto data...'):
        # Run ingestion pipeline
        result1 = subprocess.run(
            ['make', 'run-pipeline'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result1.returncode != 0:
            st.error(f"Pipeline failed: {result1.stderr}")
            return False
    
    with st.spinner(' Running dbt transformations...'):
        # Run dbt
        result2 = subprocess.run(
            ['make', 'dbt-run'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout
        )
        
        if result2.returncode != 0:
            st.error(f"dbt failed: {result2.stderr}")
            return False
    
    return True

# Main app
st.title(" CoinFlow: Crypto Market Analytics")
st.markdown("Real-time cryptocurrency price tracking and analytics powered by Yahoo Finance")

# Top bar with refresh button and last updated
col_left, col_right = st.columns([3, 1])

with col_left:
    last_updated = get_last_updated()
    if last_updated:
        st.info(f" **Data last updated:** {last_updated}")
    else:
        st.warning(" No data found. Click 'Refresh Data' to fetch latest prices.")

with col_right:
    if st.button(" Refresh Data", type="primary", use_container_width=True):
        if refresh_data():
            st.success(" Data refreshed successfully!")
            st.rerun()
        else:
            st.error(" Failed to refresh data. Check logs.")

st.divider()

# Load data
try:
    df = load_data()
    
    if df is None:
        st.error("Unable to connect to database. Please ensure the database file exists.")
        st.info("Run the following commands to set up the database:")
        st.code("""
make run-pipeline
make dbt-run
        """)
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    symbols = df['symbol'].unique()
    selected_symbol = st.sidebar.selectbox("Select Cryptocurrency", symbols, index=0)
    
    st.sidebar.divider()
    st.sidebar.subheader(" Data Info")
    st.sidebar.metric("Total Records", len(df))
    st.sidebar.metric("Cryptocurrencies", len(symbols))
    st.sidebar.metric("Date Range", f"{len(df[df['symbol'] == symbols[0]])} days")
    
    # Filter data for selected symbol
    symbol_df = df[df['symbol'] == selected_symbol].copy()
    symbol_df['metric_date'] = pd.to_datetime(symbol_df['metric_date'])
    
    # Key metrics
    latest = symbol_df.iloc[-1]
    prev = symbol_df.iloc[-2] if len(symbol_df) > 1 else latest
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"${latest['close_price']:.2f}",
            f"{latest['day_over_day_change_pct']:.2f}%" if pd.notna(latest['day_over_day_change_pct']) else "N/A"
        )
    
    with col2:
        st.metric(
            "24h High",
            f"${latest['high_price']:.2f}"
        )
    
    with col3:
        st.metric(
            "24h Low",
            f"${latest['low_price']:.2f}"
        )
    
    with col4:
        st.metric(
            "Volume",
            f"{latest['volume']:,.0f}"
        )
    
    # Price chart with moving averages
    st.subheader(f"{selected_symbol} Price History")
    
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=symbol_df['metric_date'],
        open=symbol_df['open_price'],
        high=symbol_df['high_price'],
        low=symbol_df['low_price'],
        close=symbol_df['close_price'],
        name='Price'
    ))
    
    # Moving averages
    fig.add_trace(go.Scatter(
        x=symbol_df['metric_date'],
        y=symbol_df['ma_7day'],
        name='7-Day MA',
        line=dict(color='orange', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=symbol_df['metric_date'],
        y=symbol_df['ma_30day'],
        name='30-Day MA',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily returns chart
    st.subheader("Daily Returns (%)")
    
    fig_returns = px.bar(
        symbol_df,
        x='metric_date',
        y='daily_return_pct',
        color='daily_return_pct',
        color_continuous_scale=['red', 'yellow', 'green'],
        color_continuous_midpoint=0
    )
    
    fig_returns.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily Return (%)",
        height=300
    )
    
    st.plotly_chart(fig_returns, use_container_width=True)
    
    # Data table
    st.subheader("Recent Data")
    st.dataframe(
        symbol_df[['metric_date', 'close_price', 'volume', 'daily_return_pct', 'day_over_day_change_pct']]
        .tail(10)
        .sort_values('metric_date', ascending=False),
        use_container_width=True
    )
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure you've run the ingestion pipeline and dbt models first!")
    
    if st.button(" Run Initial Setup", type="primary"):
        if refresh_data():
            st.success(" Setup complete! Reloading...")
            st.rerun()
