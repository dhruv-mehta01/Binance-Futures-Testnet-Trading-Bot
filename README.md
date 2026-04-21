# Binance Futures Testnet Trading Bot

This project is a Python-based trading bot that allows placing MARKET and LIMIT orders on the Binance USDT-M Futures Testnet.

It was built as part of an internship assignment with a focus on clean structure, proper logging, and usability. The project includes both a command-line interface (CLI) and a simple dashboard for interacting with the bot.

---

## 🚀 Features

* Place **MARKET** and **LIMIT** orders
* Supports both **BUY** and **SELL**
* CLI-based execution using command-line arguments
* Lightweight dashboard for visual interaction
* Input validation before sending requests
* Logging of API requests, responses, and errors
* Modular and readable code structure

---

## 📁 Project Structure

```id="structurefinal"
binance/
├── bot/
│   ├── __init__.py
│   ├── client.py           # Handles Binance API communication
│   ├── orders.py           # Order execution logic
│   ├── validators.py       # Input validation
│   ├── logging_config.py   # Logging setup
│
├── dashboard/
│   ├── backend.py          # Backend for dashboard
│   ├── static/
│   │   ├── index.html
│   │   ├── app.js
│   │   └── style.css
│
├── logs/
│   └── trading_bot.log     # Log file
│
├── cli.py                  # CLI entry point
├── test_api.py             # API test script
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Create a virtual environment

```bash id="setupa"
python -m venv venv
venv\Scripts\activate
```

---

### 2. Install dependencies

```bash id="setupb"
pip install -r requirements.txt
```

---

### 3. Get Binance Testnet API Keys

Go to:
👉 https://testnet.binancefuture.com

* Login / Register
* Go to **API Management**
* Create API key (System Generated)
* Enable Futures trading

---

### 4. Configure environment variables

Create a `.env` file:

```env id="envsetup"
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
```

---

## ▶️ Usage

### 🔹 CLI

Check available commands:

```bash id="cmdhelp"
python cli.py --help
```

---

### 🟢 Place MARKET Order

```bash id="cmdmarket"
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

---

### 🔵 Place LIMIT Order

```bash id="cmdlimit"
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

---

## 🖥️ Dashboard

A lightweight dashboard is included for easier interaction with the bot.

Run the backend:

```bash id="rundash"
python dashboard/backend.py
```

Then open:

```id="dashopen"
dashboard/static/index.html
```

in your browser.

### Dashboard Features:

* Input fields for symbol, side, order type, quantity, and price
* Buttons to place BUY/SELL orders
* Displays order responses
* Simple and clean UI

---

## 🧾 Logging

Logs are stored in:

```id="logfile"
logs/trading_bot.log
```

Logs include:

* API requests
* responses
* error messages

---

## 🧪 Testing

To test API connectivity:

```bash id="testcmd"
python test_api.py
```

---

## ⚠️ Notes

* Uses Binance **Futures Testnet** (no real funds involved)
* Testnet data may reset periodically
* API keys must be generated from testnet
* Quantity precision may vary by symbol

---

## 📌 Assumptions

* Only USDT-M futures pairs are supported
* LIMIT orders use default settings (GTC)
* Basic validation is implemented for inputs

---

## 🚀 Future Improvements

* Add advanced order types (Stop-Limit, etc.)
* Improve dashboard UI/UX
* Add order history tracking

---

## 🙌 Final Note

This project demonstrates a practical approach to building a trading bot using Python. It focuses on functionality, structure, and ease of use, making it simple to understand and extend.
