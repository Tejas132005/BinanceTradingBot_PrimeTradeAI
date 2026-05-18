# Binance Futures Testnet Trading Bot 🚀📊

A professional, interview-quality Python trading bot designed for the **Binance Futures Testnet (USDT-M Futures)**. This project features a robust modular backend built with Flask and `python-binance`, an elegant dark-themed web dashboard powered by Bootstrap 5 and Vanilla JavaScript, and full Command-Line Interface (CLI) support.

---

## 🌟 Project Overview

This trading bot enables automated and manual execution of perpetual futures contracts on the Binance Futures Testnet. Built with strict adherence to clean code principles, modular architecture, and robust exception handling, it demonstrates senior-level Python engineering practices. 

The bot operates strictly in a risk-free simulation environment (`https://testnet.binancefuture.com`), ensuring zero real capital exposure while providing identical market execution dynamics to the live Binance Futures exchange.

---

## ✨ Key Features

- **Multi-Interface Support**: Execute orders seamlessly via a beautiful Web Dashboard or directly from the terminal via CLI.
- **Advanced Order Types**: Support for `MARKET`, `LIMIT` (`GTC`), and **Bonus Feature**: `STOP` (Stop-Limit) orders.
- **Bi-Directional Trading**: Seamless execution of both `BUY` (Long) and `SELL` (Short) positions.
- **Enterprise-Grade Validation**: Strict pre-execution sanitization and validation of symbols, sides, order types, quantities, and prices.
- **Comprehensive Logging**: Automated rotating file logging (`logs/trading.log`) capturing API requests, responses, timestamps, execution statuses, and critical exceptions.
- **Graceful Exception Handling**: Custom exception hierarchy isolating validation, authentication, network, and Binance API errors with user-friendly feedback in both the UI and terminal.
- **Premium Dark UI**: Gorgeous Binance-inspired dark theme featuring glassmorphism cards, dynamic form adaptations, live status indicators, and an embedded Execution Terminal.

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Flask**: Lightweight WSGI web application framework.
- **python-binance**: Official Binance API wrapper.
- **python-dotenv**: Secure environment variable management.

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5**: Modern responsive UI framework.
- **Vanilla JavaScript**: Asynchronous `fetch` API integration and dynamic DOM manipulation.
- **Google Fonts (Inter & JetBrains Mono)** + **FontAwesome 6**.

### System & Utilities
- `logging` (RotatingFileHandler)
- `argparse` (CLI parsing)
- `typing` (Strict type hinting)

---

## 📁 Folder Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package initialization & component exports
│   ├── client.py            # Secure Binance Futures Testnet client initialization
│   ├── orders.py            # Order execution logic & structured formatting
│   ├── validators.py        # Input validation & sanitization rules
│   ├── logging_config.py    # Rotating file logger configuration
│   └── exceptions.py        # Custom exception hierarchy
│
├── templates/
│   └── index.html           # Premium dark-themed trading dashboard UI
│
├── static/
│   ├── style.css            # Custom Binance dark theme & glassmorphism styles
│   └── app.js               # Frontend dynamic state management & API integration
│
├── logs/
│   └── trading.log          # Automated trading activity and error logs
│
├── app.py                   # Flask WSGI application backend
├── cli.py                   # Command-line interface entry point
├── .env.example             # Template for API credentials
├── requirements.txt         # Project dependencies
├── README.md                # Comprehensive documentation
└── .gitignore               # Git exclusion rules
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.9 or higher installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/Tejas132005/BinanceTradingBot_PrimeTradeAI.git
cd BinanceTradingBot_PrimeTradeAI
```

### 3. Virtual Environment Setup
It is highly recommended to isolate project dependencies using a virtual environment.

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. .env Configuration
1. Obtain your Binance Futures Testnet API keys from [Binance Futures Testnet](https://testnet.binancefuture.com).
2. Copy the template file:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and insert your credentials:
   ```env
   BINANCE_API_KEY=your_actual_testnet_api_key_here
   BINANCE_SECRET_KEY=your_actual_testnet_secret_key_here
   ```

---

## 🚀 How to Run the Application

### Option A: Running the Flask Web Dashboard

Start the Flask backend server:
```bash
python app.py
```
Open your web browser and navigate to:
👉 **`http://localhost:5000`**

---

### Option B: Running the Command-Line Interface (CLI)

The CLI provides direct, lightning-fast order execution from your terminal. Use `python cli.py --help` to view all available arguments.

#### Example Commands:

**1. Place a Market Buy Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**2. Place a Limit Sell Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

**3. Place a Stop-Limit Buy Order (Bonus Feature):**
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.001 --price 62000 --stop-price 61500
```

---

## 📸 Example Screenshots

### Web Trading Dashboard & Execution Terminal
*(Representative layout of the premium dark-themed UI)*

```text
+---------------------------------------------------------------------------+
| BINANCE FUTURES TESTNET   [Testnet Active]                      [Refresh] |
+---------------------------------------------------------------------------+
|                                     |                                     |
|  ⚡ Place Order                     |  >_ Execution Terminal              |
|  ---------------------------------  |  ---------------------------------  |
|  Symbol:    [ BTCUSDT            ]  |  =================================  |
|  Side:      [ 🟢 BUY (Long)      ]  |  ORDER REQUEST                      |
|  Type:      [ Limit Order        ]  |  =================================  |
|  Quantity:  [ 0.001       ] [COIN]  |  Symbol: BTCUSDT                    |
|  Price:     [ 65000       ] [USDT]  |  Side: BUY                          |
|                                     |  Type: LIMIT                        |
|  +-------------------------------+  |  Quantity: 0.001                    |
|  |      Execute Limit Buy        |  |  Price: 65000.0                     |
|  +-------------------------------+  |  ...                                |
|                                     |  SUCCESS: Order placed successfully |
+---------------------------------------------------------------------------+
```

---

## 📝 Example Log Output

Below is an extract from `logs/trading.log` illustrating successful order lifecycle logging and API error interception:

```log
2026-05-18 17:00:15 - flask.app - INFO - Received POST request at /place-order
2026-05-18 17:00:15 - bot.orders - INFO - Received order request: BTCUSDT, BUY, LIMIT, Qty: 0.001, Price: 65000, Stop: None
2026-05-18 17:00:15 - bot.client - INFO - Initializing Binance Client with testnet=True...
2026-05-18 17:00:16 - bot.client - INFO - Verifying Futures Testnet connection and credentials...
2026-05-18 17:00:16 - bot.client - INFO - Binance Futures Testnet client authenticated successfully.
2026-05-18 17:00:16 - bot.orders - INFO - Sending order to Binance Futures Testnet: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'LIMIT', 'quantity': 0.001, 'price': 65000.0, 'timeInForce': 'GTC'}
2026-05-18 17:00:17 - bot.orders - INFO - Order executed successfully. Response: {'orderId': 483920183, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'test_order_1', 'price': '65000', 'origQty': '0.001', 'executedQty': '0', 'avgPrice': '0', 'type': 'LIMIT', 'side': 'BUY'}
2026-05-18 17:00:17 - flask.app - INFO - Order successfully processed for BTCUSDT (BUY LIMIT)
```

---

## 📌 Assumptions & Design Decisions

1. **Simulation Environment**: It is assumed that the user intends to trade strictly on the Binance Futures Testnet (`https://testnet.binancefuture.com`). The bot enforces `testnet=True` and overrides base URLs to prevent accidental live market orders.
2. **Time In Force**: In accordance with project requirements, all `LIMIT` and `STOP` orders are automatically configured with `timeInForce="GTC"` (Good 'Til Cancelled).
3. **Stop-Limit Implementation**: For the bonus Stop-Limit feature, the bot uses Binance's `STOP` order type which requires both a limit `price` and a trigger `stopPrice`.
4. **Credential Verification**: To ensure fail-fast behavior, the bot actively verifies API credentials using `client.futures_account()` prior to transmitting order payloads.
5. **Logging Strategy**: To maintain clean CLI output, standard informational logs are directed exclusively to `logs/trading.log`, while critical system errors are surfaced to the console.

---

## ⚖️ License
This project is open-source and available under the [MIT License](LICENSE).

---
*Built with passion for high-performance algorithmic trading systems.* 📈🤖
