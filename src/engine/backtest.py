import pandas as pd


def run_backtest(df: pd.DataFrame, initial_capital: float = 10000.0) -> dict:
    """
    Backtest with DCA strategy — splits capital across multiple BUY signals.
    """
    capital  = initial_capital
    btc_held = 0.0
    trades   = []

    buy_signals  = (df["signal"] == 1).sum()
    capital_per_buy = initial_capital / buy_signals if buy_signals > 0 else initial_capital

    for i, row in df.iterrows():
        price  = row["close"]
        signal = row["signal"]

        if signal == 1 and capital >= capital_per_buy:
            btc_bought = capital_per_buy / price
            btc_held  += btc_bought
            capital   -= capital_per_buy
            trades.append({
                "date"  : i,
                "action": "BUY",
                "price" : price,
                "btc"   : btc_bought,
                "spent" : capital_per_buy
            })

        elif signal == -1 and btc_held > 0:
            earned   = btc_held * price
            capital += earned
            trades.append({
                "date"    : i,
                "action"  : "SELL",
                "price"   : price,
                "capital" : capital
            })
            btc_held = 0.0

    final_price = df["close"].iloc[-1]
    if btc_held > 0:
        capital += btc_held * final_price

    total_return    = ((capital - initial_capital) / initial_capital) * 100
    buy_hold_return = ((final_price - df["close"].iloc[0]) / df["close"].iloc[0]) * 100

    results = {
        "initial_capital" : initial_capital,
        "final_capital"   : round(capital, 2),
        "total_return_pct": round(total_return, 2),
        "buy_hold_pct"    : round(buy_hold_return, 2),
        "num_trades"      : len(trades),
        "trades"          : trades
    }

    return results


if __name__ == "__main__":
    from src.data.fetcher import fetch_ohlcv
    from src.features.indicators import add_indicators
    from src.engine.strategy import generate_signals

    df = fetch_ohlcv("BTC-USD", period="6mo", interval="1d")
    df = add_indicators(df)
    df = generate_signals(df)

    results = run_backtest(df, initial_capital=10000)

    print("\n===== BACKTEST RESULTS (DCA) =====")
    print(f"Capital initial  : ${results['initial_capital']:,.0f}")
    print(f"Capital final    : ${results['final_capital']:,.2f}")
    print(f"Performance bot  : {results['total_return_pct']}%")
    print(f"Buy & Hold       : {results['buy_hold_pct']}%")
    print(f"Nombre de trades : {results['num_trades']}")
    print("==================================\n")

    print("Détail des trades :")
    for t in results["trades"]:
        if t["action"] == "BUY":
            print(f"  🟢 BUY  {t['date'].date()} @ ${t['price']:,.0f} | dépensé ${t['spent']:,.0f}")
        else:
            print(f"  🔴 SELL {t['date'].date()} @ ${t['price']:,.0f} → capital ${t['capital']:,.2f}")