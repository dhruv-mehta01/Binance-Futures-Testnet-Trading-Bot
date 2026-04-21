# 📈 Binance Pro Trading Bot & Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Binance](https://img.shields.io/badge/Binance-Testnet-F3BA2F.svg)

> **A professional-grade Python backend and web dashboard for trading on the Binance Futures Testnet.**

Hey there! 👋 I built this project to dive deep into algorithmic trading infrastructure and frontend design. It started as a simple Python CLI assignment to place Market and Limit orders on the Binance Testnet, but I ended up taking it a step further. I built a full "Bloomberg Terminal"-style web dashboard with live TradingView charts, real-time balance tracking, and order management.

It's designed to be clean, responsive, and completely runnable locally without much hassle. Enjoy!

## ✨ Features

* **Advanced Web Dashboard**: A slick, dark-mode Pro interface built with CSS Grid and vanilla JS (no heavy frontend frameworks required!).
* **Live TradingView Charts**: Dynamic candlestick charts that auto-sync when you switch market symbols (e.g., `BTCUSDT` to `ETHUSDT`).
* **Robust CLI Interface**: Powered by `Typer` and `Rich` for gorgeous terminal outputs and quick manual trades.
* **REST API Backend**: A lightning-fast `FastAPI` server that acts as a secure bridge between the frontend and the Binance API.
* **Order Management**: Place `MARKET` and `LIMIT` orders, view open orders, and cancel them instantly.
* **Secure Authentication**: Proper implementation of Binance's strict HMAC-SHA256 signature protocol.

---

## 🛠️ Project Architecture

```text
binance/
├── src/                   # Main source code directory
│   ├── bot/               # Core Python logic
│   │   ├── client.py      # HMAC-SHA256 signing and HTTP wrapper
│   │   ├── orders.py      # Trading operations (balances, orders)
│   │   ├── validators.py  # Input validation logic
│   │   └── logging_config.py
│   ├── dashboard/         # Web App
│   │   ├── backend.py     # FastAPI application bridging UI & Bot
│   │   └── static/        # Frontend (HTML, CSS, Vanilla JS)
│   └── cli.py             # The Typer CLI entrypoint
├── tests/                 # Unit and API tests
├── logs/                  # Where all API interaction logs live
├── requirements.txt       # Dependencies
└── README.md              # You are here!
```

---

## 🚀 How to Run It Locally

### 1. Setup your environment
Clone the repo, create a virtual environment, and install dependencies.
```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Configure your keys
Get your Testnet API keys from [Binance Futures Testnet](https://testnet.binancefuture.com) and add them to a `.env` file in the root directory:
```env
BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_SECRET=your_secret_here
```

### 3. Launch the Web Dashboard (Recommended!)
Start the FastAPI server:
```bash
uvicorn src.dashboard.backend:app --host 127.0.0.1 --port 8000
```
Then open your browser to **http://localhost:8000** to see the magic. 🪄

### 4. Or use the CLI
If you prefer the terminal:
```bash
# Place a 0.01 BTC Market Buy order
python src/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Place a Limit Sell order
python src/cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3200.50
```

---

## � Lessons Learned
- **HMAC Signatures are tricky**: Getting the URL query parameters properly signed and ordered exactly the way Binance expects was a great lesson in secure API integrations.
- **CSS Grid is a superpower**: Building the dense Pro layout was surprisingly smooth once I mapped out the grid areas. It beats flexbox when creating rigid, complex application layouts.
- **Decoupling is key**: By separating the `bot/` logic from the `cli.py` handler, it was incredibly easy to slap a `FastAPI` wrapper on top of it later without rewriting any of the core trading engine.

Feel free to fork this and build your own automated strategies on top of it!
