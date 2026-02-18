# 📈 Trading Bot — Algorithmic Trading System

> Automated trading bot using technical analysis indicators to generate buy/sell signals on financial markets.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=flat-square&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3D4A8A?style=flat-square&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎯 Overview

This project implements a **full algorithmic trading pipeline** — from raw market data ingestion to backtesting and interactive visualization. Built with a professional 4-layer architecture designed to be extended with Machine Learning models.

### Backtest Results (BTC-USD, 6 months)
| Strategy | Return |
|---|---|
| 🤖 Bot (DCA + RSI/Bollinger) | -16.23% |
| 📊 Buy & Hold | -45.98% |
| ✅ Outperformance | **+29.75%** |

> On a 6-month bear market, the bot limited losses by 30 percentage points vs a passive strategy.

---

## 🏗️ Architecture
```
trading-bot/
├── src/
│   ├── data/               # Layer 1 — Data Ingestion
│   │   └── fetcher.py      # Yahoo Finance API wrapper
│   ├── features/           # Layer 2 — Feature Engineering
│   │   └── indicators.py   # RSI, EMA, MACD, Bollinger Bands
│   ├── engine/             # Layer 3 — Decision Engine
│   │   ├── strategy.py     # Signal generation (Heuristic-based)
│   │   └── backtest.py     # DCA backtesting engine
│   └── visualization/      # Layer 4 — Reporting
│       └── chart.py        # Interactive Plotly dashboard
```

---

## ⚙️ How It Works

### Layer 1 — Data Ingestion
Fetches real OHLCV market data (Open, High, Low, Close, Volume) from Yahoo Finance. Supports any ticker: stocks, crypto, ETFs.

### Layer 2 — Feature Engineering
Transforms raw prices into actionable indicators:
- **RSI (14)** — Detects overbought/oversold market conditions
- **EMA 20/50** — Short and long term trend direction
- **Bollinger Bands** — Price volatility and extremes
- **MACD** — Momentum and trend reversal signals

### Layer 3 — Decision Engine
Heuristic-based signal generator. Triggers a **BUY** when:
- RSI < 30 (oversold market)
- Price near lower Bollinger Band (price extreme)
- MACD showing momentum reversal

Triggers a **SELL** when:
- RSI > 70 (overbought market)
- Price near upper Bollinger Band
- MACD crossing down

Uses a **DCA strategy** (Dollar Cost Averaging) — splits capital across multiple signals to reduce risk exposure.

### Layer 4 — Visualization
Interactive Plotly dashboard with candlestick chart, indicators overlay, buy/sell signals, RSI and MACD subplots.

---

## 🚀 Getting Started
```bash
git clone https://github.com/mballuais/trading-bot.git
cd trading-bot

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python -m src.visualization.chart
```

---

## 🔬 Tech Stack

| Tool | Usage |
|---|---|
| `yfinance` | Market data ingestion |
| `pandas` | Data manipulation |
| `ta` | Technical indicators |
| `plotly` | Interactive visualization |

---

## 🔮 Roadmap

- [ ] Machine Learning layer (Random Forest / LSTM)
- [ ] Live trading mode with paper trading
- [ ] Multi-asset portfolio support
- [ ] Risk management module (Stop Loss / Take Profit)
- [ ] REST API to expose signals

---

## 📄 License

MIT License — free to use and modify.