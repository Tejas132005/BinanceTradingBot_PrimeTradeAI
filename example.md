# Binance Futures Testnet - Comprehensive Order Examples 📊🚀

This guide provides definitive, interview-quality examples for executing every supported order type (`MARKET`, `LIMIT`, `STOP`) across both `BUY` (Long) and `SELL` (Short) sides using the **Binance Futures Testnet Trading Bot**. E.g., it covers exact CLI commands, Web UI parameter configurations, exchange filter rules, and expected terminal outputs.

---

## 🏛️ Exchange Filter Rules (USDT-M Futures)

Before placing orders, ensure your parameters adhere strictly to Binance Futures exchange rules:

1. **`LOT_SIZE` (Minimum Quantity & Step Size)**:
   - **`BTCUSDT`**: Minimum quantity is `0.001` BTC. Must be increments of `0.001` (e.g., `0.001`, `0.002`, `0.015`). E.g., `0.0005` or `0.00125` will be rejected.
   - **`ETHUSDT`**: Minimum quantity is `0.01` ETH. Must be increments of `0.01`.

2. **`PRICE_FILTER` (Tick Size)**:
   - Prices must be rounded to the correct decimal place (e.g., `0.10` USDT tick size for BTCUSDT means `$65000.10`, not `$65000.12345`).

3. **`PERCENT_PRICE` (Price Band Limit)**:
   - To prevent order book manipulation, Binance Futures rejects Limit orders placed excessively far from the current **Mark Price** (typically restricted to within 5% - 10% of the current market price). E.g., if BTC is trading at `$65,000`, placing a Buy Limit at `$100` will be rejected with `Code -4013 (Price less than min price)`.

---

## 🟢 1. MARKET Orders (Instant Execution)

Market orders execute instantly against the best available price in the order book. E.g., no limit price or stop price is required.

### Example 1A: Market Buy (Long Entry)
* **Scenario**: You want to enter a Long position on Bitcoin instantly at current market price.
* **CLI Command**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  ```
* **Web UI Configuration**:
  - **Symbol**: `BTCUSDT`
  - **Order Side**: `🟢 BUY (Long)`
  - **Order Type**: `Market Order`
  - **Quantity**: `0.001`
  - **Limit Price**: *(Hidden / N/A)*
  - **Stop Price**: *(Hidden / N/A)*

---

### Example 1B: Market Sell (Short Entry / Long Close)
* **Scenario**: You want to enter a Short position on Ethereum instantly at current market price.
* **CLI Command**:
  ```bash
  python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.05
  ```
* **Web UI Configuration**:
  - **Symbol**: `ETHUSDT`
  - **Order Side**: `🔴 SELL (Short)`
  - **Order Type**: `Market Order`
  - **Quantity**: `0.05`

---

## 🟡 2. LIMIT Orders (Good 'Til Cancelled - GTC)

Limit orders are placed in the order book and execute only at your specified price or better. E.g., requires a `price` parameter within the exchange's allowed percentage price band.

### Example 2A: Limit Buy (Buying the Dip)
* **Scenario**: Bitcoin is trading at `$65,000`. You want to buy `0.002` BTC if the price pulls back to `$64,200`.
* **CLI Command**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 64200
  ```
* **Web UI Configuration**:
  - **Symbol**: `BTCUSDT`
  - **Order Side**: `🟢 BUY (Long)`
  - **Order Type**: `Limit Order`
  - **Quantity**: `0.002`
  - **Limit Price**: `64200`

---

### Example 2B: Limit Sell (Selling at Resistance / Shorting)
* **Scenario**: Ethereum is trading at `$3,500`. You want to open a Short position of `0.1` ETH if the price rallies to `$3,650`.
* **CLI Command**:
  ```bash
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3650
  ```
* **Web UI Configuration**:
  - **Symbol**: `ETHUSDT`
  - **Order Side**: `🔴 SELL (Short)`
  - **Order Type**: `Limit Order`
  - **Quantity**: `0.1`
  - **Limit Price**: `3650`

---

## 🟣 3. STOP Orders (Stop-Limit / Conditional Triggers)

A Stop-Limit order requires both a trigger price (`stop-price`) and an order book execution price (`price`). E.g., it is placed as a conditional trigger on Binance Futures.

### Example 3A: Stop Buy (Breakout Long Entry)
* **Scenario**: Bitcoin is trading at `$65,000` below a major resistance at `$66,000`. You want to enter a Long position only if the market breaks above `$66,000`. E.g., once triggered, you want your Limit Buy order placed at `$66,050`.
* **Rule**: For a Stop Buy, `stop-price` must be **ABOVE** the current market price.
* **CLI Command**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.001 --price 66050 --stop-price 66000
  ```
* **Web UI Configuration**:
  - **Symbol**: `BTCUSDT`
  - **Order Side**: `🟢 BUY (Long)`
  - **Order Type**: `Stop-Limit Order`
  - **Quantity**: `0.001`
  - **Limit Price**: `66050`
  - **Stop Price**: `66000`

---

### Example 3B: Stop Sell (Stop-Loss Protection / Breakdown Short)
* **Scenario**: Bitcoin is trading at `$65,000`. You are Long and want to protect your position with a Stop-Loss if the price drops below `$64,000`. E.g., once triggered at `$64,000`, your Limit Sell order is placed at `$63,950`.
* **Rule**: For a Stop Sell, `stop-price` must be **BELOW** the current market price.
* **CLI Command**:
  ```bash
  python cli.py --symbol BTCUSDT --side SELL --type STOP --quantity 0.001 --price 63950 --stop-price 64000
  ```
* **Web UI Configuration**:
  - **Symbol**: `BTCUSDT`
  - **Order Side**: `🔴 SELL (Short)`
  - **Order Type**: `Stop-Limit Order`
  - **Quantity**: `0.001`
  - **Limit Price**: `63950`
  - **Stop Price**: `64000`

---

## 🖥️ Expected Execution Outputs

Whether executing via CLI or the Web UI Execution Terminal, successful orders will return the exact formatted response structure required by the project specifications:

### Successful Order Response Example:

```text
====================================
ORDER REQUEST
====================================

Symbol: BTCUSDT
Side: BUY
Type: LIMIT
Quantity: 0.001
Price: 64500.0

====================================
ORDER RESPONSE
====================================

Order ID: 483920194
Status: NEW
Executed Qty: 0
Avg Price: 0

SUCCESS: Order placed successfully
```

---

## ⚠️ Common Error Scenarios & Troubleshooting

### 1. `[Code -4013] Price less than min price`
* **Cause**: You entered a Limit Price (e.g., `$100`) that is excessively far below the current Mark Price (e.g., `$65,000`). E.g., Binance Futures Testnet rejects orders outside its 10% price band.
* **Solution**: Enter a limit price closer to the current market price (e.g., `$64,000`).

### 2. `[Code -1111] Precision is over the maximum defined for this asset`
* **Cause**: You entered a quantity with too many decimal places (e.g., `0.00125` BTC).
* **Solution**: Ensure your quantity matches the asset's step size (`0.001` for BTCUSDT, `0.01` for ETHUSDT).

### 3. `[Code -2010] Stop price would trigger immediately`
* **Cause**: You placed a Stop Buy order with a stop price *below* the current market price, or a Stop Sell order with a stop price *above* the current market price.
* **Solution**: For `STOP BUY`, ensure `stop_price > current_market_price`. For `STOP SELL`, ensure `stop_price < current_market_price`.
