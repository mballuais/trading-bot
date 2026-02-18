import pandas as pd


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Decision Engine — Heuristic-based strategy.
    
    Buy signal when:
        - RSI < 30 (oversold)
        - EMA 20 < EMA 50 but price touches lower Bollinger Band (potential reversal)
        - MACD crossing up (momentum shift)
    
    Sell signal when:
        - RSI > 70 (overbought)
        - Price above upper Bollinger Band
        - MACD crossing down
    """
    df = df.copy()
    df["signal"] = 0  # 0 = hold, 1 = buy, -1 = sell

    for i in range(1, len(df)):
        rsi        = df["rsi"].iloc[i]
        macd       = df["macd"].iloc[i]
        macd_prev  = df["macd"].iloc[i - 1]
        macd_sig   = df["macd_signal"].iloc[i]
        macd_prev_sig = df["macd_signal"].iloc[i - 1]
        close      = df["close"].iloc[i]
        bb_lower   = df["bb_lower"].iloc[i]
        bb_upper   = df["bb_upper"].iloc[i]

        # BUY conditions
        macd_cross_up = (macd_prev < macd_prev_sig) and (macd > macd_sig)
        price_at_low  = close <= bb_lower * 1.02  # within 2% of lower band

        if rsi < 30 and (macd_cross_up or price_at_low):
            df.at[df.index[i], "signal"] = 1

        # SELL conditions
        macd_cross_down = (macd_prev > macd_prev_sig) and (macd < macd_sig)
        price_at_high   = close >= bb_upper * 0.98  # within 2% of upper band

        if rsi > 70 and (macd_cross_down or price_at_high):
            df.at[df.index[i], "signal"] = -1

    return df


if __name__ == "__main__":
    from src.data.fetcher import fetch_ohlcv
    from src.features.indicators import add_indicators

    df = fetch_ohlcv("BTC-USD", period="6mo", interval="1d")
    df = add_indicators(df)
    df = generate_signals(df)

    # Show only rows where bot took a decision
    signals = df[df["signal"] != 0][["close", "rsi", "macd", "signal"]]
    signals["action"] = signals["signal"].map({1: "🟢 BUY", -1: "🔴 SELL"})

    print(f"\n{len(signals)} signals generated:\n")
    print(signals[["close", "rsi", "action"]])