import pandas as pd
import ta


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw OHLCV data into meaningful features.
    
    Indicators:
        - RSI: Detects overbought/oversold conditions
        - EMA 20/50: Short and long term trend
        - Bollinger Bands: Volatility & price extremes
        - MACD: Momentum and trend direction
    """
    df = df.copy()

    # RSI (Relative Strength Index)
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()

    # EMA - Exponential Moving Averages
    df["ema_20"] = ta.trend.EMAIndicator(close=df["close"], window=20).ema_indicator()
    df["ema_50"] = ta.trend.EMAIndicator(close=df["close"], window=50).ema_indicator()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_mid"]   = bb.bollinger_mavg()

    # MACD
    macd = ta.trend.MACD(close=df["close"])
    df["macd"]        = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    # Drop NaN rows (indicators need warmup candles)
    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    from src.data.fetcher import fetch_ohlcv

    df = fetch_ohlcv("BTC-USD", period="6mo", interval="1d")
    df = add_indicators(df)

    print(df[["close", "rsi", "ema_20", "ema_50", "macd"]].tail(10))