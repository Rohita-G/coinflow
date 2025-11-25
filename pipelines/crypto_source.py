import dlt
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

@dlt.resource(write_disposition="replace")
def coins_list():
    """
    Returns a hardcoded list of top crypto coins to track.
    We use hardcoded list to ensure we get valid Yahoo tickers.
    """
    # Map of Name -> Yahoo Ticker
    top_coins = [
        {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin", "yahoo_ticker": "BTC-USD"},
        {"id": "ethereum", "symbol": "ETH", "name": "Ethereum", "yahoo_ticker": "ETH-USD"},
        {"id": "solana", "symbol": "SOL", "name": "Solana", "yahoo_ticker": "SOL-USD"},
        {"id": "ripple", "symbol": "XRP", "name": "XRP", "yahoo_ticker": "XRP-USD"},
        {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin", "yahoo_ticker": "DOGE-USD"},
    ]
    yield from top_coins

@dlt.transformer(data_from=coins_list, write_disposition="append")
def crypto_ohlcv(coin):
    """
    Fetches OHLCV data from Yahoo Finance for each coin.
    """
    ticker = coin.get("yahoo_ticker")
    print(f"Fetching data for {ticker}...")
    
    try:
        # Fetch last 30 days of data
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        
        if df.empty:
            print(f"No data found for {ticker}")
            return

        # Reset index to get Date as a column
        df = df.reset_index()
        
        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        # Convert to list of dicts
        records = df.to_dict(orient="records")
        
        for record in records:
            # Clean up keys (yfinance returns Title Case columns)
            # And handle Timestamp objects
            yield {
                "symbol": ticker,
                "date": record["Date"], # dlt handles datetime objects
                "open": record["Open"],
                "high": record["High"],
                "low": record["Low"],
                "close": record["Close"],
                "volume": record["Volume"]
            }
            
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")

@dlt.source
def crypto_source():
    return [coins_list, crypto_ohlcv]

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="coinflow",
        destination="duckdb",
        dataset_name="raw_crypto"
    )
    
    # Run the pipeline
    load_info = pipeline.run(crypto_source())
    print(load_info)
