import yfinance as yf
import pandas as pd
from datetime import datetime


def fetch_ohlcv(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch OHLCV data from Yahoo Finance.
    
    Args:
        ticker: Asset symbol (ex: 'AAPL', 'BTC-USD', 'MSFT')
        period: Data period ('1mo', '3mo', '6mo', '1y', '2y')
        interval: Candle interval ('1d', '1h', '15m')
    
    Returns:
        DataFrame with OHLCV data
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching {ticker} | period={period} | interval={interval}")
    
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    
    if df.empty:
        raise ValueError(f"No data found for ticker '{ticker}'")

    df.columns = [col.lower() if isinstance(col, str) else col[0].lower() for col in df.columns]
    df.index.name = "date"
    
    print(f"✓ {len(df)} candles fetched | from {df.index[0].date()} to {df.index[-1].date()}")
    
    return df


if __name__ == "__main__":
    df = fetch_ohlcv("BTC-USD", period="3mo", interval="1d")
    print(df.tail())