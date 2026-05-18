"""
Flask Web Application Backend for the Trading Bot.
Provides routes for rendering the trading dashboard and processing order submissions.
"""

from flask import Flask, render_template, request, jsonify
from bot.exceptions import TradingBotException, ValidationException, AuthenticationException, BinanceAPIExceptionWrapper
from bot.orders import place_order
from bot.logging_config import setup_logger

logger = setup_logger("flask.app")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Renders the main trading dashboard UI."""
    logger.info("Accessing main trading dashboard page.")
    return render_template("index.html")


@app.route("/place-order", methods=["POST"])
def handle_place_order():
    """
    Handles order submissions from the web UI.
    Accepts JSON or Form data, validates inputs, executes the order on Binance Futures Testnet,
    and returns a formatted JSON response.
    """
    logger.info("Received POST request at /place-order")

    # Support both JSON payload and standard Form submission
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    symbol = data.get("symbol", "").strip()
    side = data.get("side", "").strip()
    order_type = data.get("order_type", "").strip()
    quantity = data.get("quantity", "").strip()
    price = data.get("price", "").strip() if data.get("price") else None
    stop_price = data.get("stop_price", "").strip() if data.get("stop_price") else None

    try:
        # Execute order placement (validation happens inside)
        result = place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        logger.info(f"Order successfully processed for {symbol} ({side} {order_type})")
        return jsonify({
            "success": True,
            "message": "Order placed successfully!",
            "formatted_summary": result["formatted_summary"],
            "data": result["data"]
        }), 200

    except ValidationException as e:
        logger.warning(f"Validation failure on order submission: {e.message}")
        return jsonify({
            "success": False,
            "message": f"Validation Error: {e.message}",
            "error_type": "ValidationException"
        }), 400

    except AuthenticationException as e:
        logger.error(f"Authentication failure: {e.message}")
        return jsonify({
            "success": False,
            "message": f"Authentication Error: {e.message}",
            "error_type": "AuthenticationException"
        }), 401

    except BinanceAPIExceptionWrapper as e:
        logger.error(f"Binance API Error: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e),
            "error_type": "BinanceAPIException"
        }), 400

    except TradingBotException as e:
        logger.error(f"Trading Bot Error: {e.message}")
        return jsonify({
            "success": False,
            "message": f"Trading Bot Error: {e.message}",
            "error_type": "TradingBotException"
        }), 400

    except Exception as e:
        logger.critical(f"Unexpected system error in /place-order: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": f"An unexpected system error occurred: {str(e)}",
            "error_type": "SystemException"
        }), 500


if __name__ == "__main__":
    logger.info("Starting Flask Trading Bot server on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
