import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def plot_backtest(df: pd.DataFrame, results: dict, ticker: str = "BTC-USD"):
    """
    Generate interactive backtest chart with:
        - Candlestick price chart
        - Bollinger Bands
        - EMA 20 / EMA 50
        - Buy signals
        - RSI subplot
        - MACD subplot
    """

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=[
            f"{ticker} — Prix & Signaux",
            "RSI (14)",
            "MACD"
        ]
    )

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"], high=df["high"],
        low=df["low"],   close=df["close"],
        name="Prix",
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["bb_upper"],
        name="BB Upper", line=dict(color="rgba(100,100,255,0.4)", dash="dash")
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["bb_lower"],
        name="BB Lower", line=dict(color="rgba(100,100,255,0.4)", dash="dash"),
        fill="tonexty", fillcolor="rgba(100,100,255,0.05)"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["ema_20"],
        name="EMA 20", line=dict(color="#ff9800", width=1.5)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["ema_50"],
        name="EMA 50", line=dict(color="#9c27b0", width=1.5)
    ), row=1, col=1)

    buys = df[df["signal"] == 1]
    fig.add_trace(go.Scatter(
        x=buys.index, y=buys["low"] * 0.98,
        mode="markers",
        name="BUY",
        marker=dict(symbol="triangle-up", size=14, color="#26a69a")
    ), row=1, col=1)

    sells = df[df["signal"] == -1]
    fig.add_trace(go.Scatter(
        x=sells.index, y=sells["high"] * 1.02,
        mode="markers",
        name="SELL",
        marker=dict(symbol="triangle-down", size=14, color="#ef5350")
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["rsi"],
        name="RSI", line=dict(color="#00bcd4", width=1.5)
    ), row=2, col=1)

    fig.add_hline(y=70, line_dash="dash", line_color="red",   opacity=0.5, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["macd"],
        name="MACD", line=dict(color="#ff9800", width=1.5)
    ), row=3, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["macd_signal"],
        name="Signal", line=dict(color="#9c27b0", width=1.5)
    ), row=3, col=1)

    perf  = results["total_return_pct"]
    bh    = results["buy_hold_pct"]
    color = "green" if perf > bh else "orange"

    fig.update_layout(
        title=dict(
            text=f"<b>Trading Bot — {ticker}</b> | "
                 f"Bot: <span style='color:{color}'>{perf}%</span> | "
                 f"Buy & Hold: {bh}%",
            font=dict(size=18)
        ),
        template="plotly_dark",
        height=900,
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.02)
    )

    fig.write_html("backtest_report.html")
    print("✓ Chart saved → backtest_report.html")
    fig.show()


if __name__ == "__main__":
    from src.data.fetcher import fetch_ohlcv
    from src.features.indicators import add_indicators
    from src.engine.strategy import generate_signals
    from src.engine.backtest import run_backtest

    df      = fetch_ohlcv("BTC-USD", period="6mo", interval="1d")
    df      = add_indicators(df)
    df      = generate_signals(df)
    results = run_backtest(df, initial_capital=10000)

    plot_backtest(df, results, ticker="BTC-USD")