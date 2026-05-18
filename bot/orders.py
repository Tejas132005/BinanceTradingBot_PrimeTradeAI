"""
Order placement and formatting module for the Trading Bot.
Manages execution of MARKET, LIMIT, and STOP (Stop-Limit) orders on Binance Futures Testnet.
"""

from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceOrderException
from .client import get_binance_client
from .validators import validate_order_input
from .exceptions import BinanceAPIExceptionWrapper, TradingBotException
from .logging_config import setup_logger

logger = setup_logger("bot.orders")

def format_order_summary(request_params: Dict[str, Any], response_data: Dict[str, Any]) -> str:
    """
    Formats the order request and response into the exact structured string
    required by the project specification.
    """
    symbol = request_params.get("symbol", "N/A")
    side = request_params.get("side", "N/A")
    order_type = request_params.get("order_type", "N/A")
    quantity = request_params.get("quantity", "N/A")
    price = request_params.get("price")
    stop_price = request_params.get("stop_price")

    price_str = f"{price}" if price is not None else "N/A"
    if stop_price is not None:
        price_str += f" (Stop Price: {stop_price})"

    order_id = response_data.get("orderId", "N/A")
    status = response_data.get("status", "N/A")
    executed_qty = response_data.get("executedQty", "0")
    avg_price = response_data.get("avgPrice", "0")

    summary = (
        "====================================\n"
        "ORDER REQUEST\n"
        "====================================\n\n"
        f"Symbol: {symbol}\n"
        f"Side: {side}\n"
        f"Type: {order_type}\n"
        f"Quantity: {quantity}\n"
        f"Price: {price_str}\n\n"
        "====================================\n"
        "ORDER RESPONSE\n"
        "====================================\n\n"
        f"Order ID: {order_id}\n"
        f"Status: {status}\n"
        f"Executed Qty: {executed_qty}\n"
        f"Avg Price: {avg_price}\n\n"
        "SUCCESS: Order placed successfully"
    )
    return summary


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Any,
    price: Optional[Any] = None,
    stop_price: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Validates input and places an order on Binance Futures Testnet.
    
    Returns:
        Dict containing:
            - success (bool)
            - data (raw Binance response dict)
            - formatted_summary (str)
            
    Raises:
        TradingBotException: For validation, auth, API, or network errors.
    """
    logger.info(f"Received order request: {symbol}, {side}, {order_type}, Qty: {quantity}, Price: {price}, Stop: {stop_price}")
    
    # 1. Validate inputs
    sym, sde, o_type, qty, prc, stp_prc = validate_order_input(
        symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price, stop_price=stop_price
    )

    # 2. Prepare API parameters with expanded recvWindow to handle network latency
    api_params = {
        "symbol": sym,
        "side": sde,
        "type": o_type,
        "quantity": qty,
        "recvWindow": 60000
    }

    if o_type == "LIMIT":
        api_params["price"] = prc
        api_params["timeInForce"] = "GTC"
    elif o_type == "STOP":
        api_params["price"] = prc
        api_params["stopPrice"] = stp_prc
        api_params["timeInForce"] = "GTC"

    # Save request params for formatting later
    request_params = {
        "symbol": sym,
        "side": sde,
        "order_type": o_type,
        "quantity": qty,
        "price": prc,
        "stop_price": stp_prc
    }

    # 3. Get Client and Execute Order
    try:
        client = get_binance_client()
        logger.info(f"Sending order to Binance Futures Testnet: {api_params}")
        
        response = client.futures_create_order(**api_params)
        logger.info(f"Order executed successfully. Response: {response}")

        order_id = response.get("orderId")
        if order_id and o_type == "MARKET":
            # For MARKET orders, wait briefly and fetch updated order status to get actual fill price and executed quantity
            import time
            time.sleep(0.5) # Allow Binance matching engine 500ms to settle the trade
            try:
                updated_order = client.futures_get_order(symbol=sym, orderId=order_id)
                logger.info(f"Fetched updated order status: {updated_order}")
                # Merge updated fields into response so format_order_summary displays actual filled values
                response.update(updated_order)
            except Exception as ex:
                logger.warning(f"Could not fetch updated order status: {ex}")

        formatted_summary = format_order_summary(request_params, response)
        
        return {
            "success": True,
            "data": response,
            "formatted_summary": formatted_summary
        }

    except (BinanceAPIException, BinanceOrderException) as e:
        logger.error(f"Binance API/Order Error: {e.message} (Code: {e.code})")
        custom_msg = e.message
        
        # Intercept specific exchange filter rejections to provide actionable user tips
        if e.code == -4013:
            custom_msg += " (Tip: Your Limit Price is too far below the current market price. Binance Futures restricts orders placed excessively far from the current Mark Price. E.g., for BTCUSDT, please enter a price closer to current market price, e.g. $60,000+)."
        elif e.code == -4014:
            custom_msg += " (Tip: Your Limit Price is too far above the current market price. Binance Futures restricts orders placed excessively far from the current Mark Price)."
        elif e.code == -4120:
            custom_msg += " (Note: Binance Futures Testnet restricts advanced conditional orders like STOP/TAKE_PROFIT to dedicated Algo Order API endpoints. For paper trading testing, please use MARKET or LIMIT orders)."
            
        raise BinanceAPIExceptionWrapper(
            message=f"Binance API Error: {custom_msg}",
            status_code=getattr(e, 'status_code', None),
            error_code=e.code
        )
    except TradingBotException:
        raise # Re-raise known bot exceptions directly
    except Exception as e:
        logger.error(f"Unexpected error during order placement: {str(e)}")
        raise TradingBotException(f"Unexpected error executing order: {str(e)}")
