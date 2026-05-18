"""
Input validation module for the Trading Bot.
Validates symbols, order sides, order types, quantities, and prices.
"""

from typing import Dict, Any, Tuple
from .exceptions import ValidationException

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT", "STOP"}

def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Any,
    price: Any = None,
    stop_price: Any = None
) -> Tuple[str, str, str, float, float, float]:
    """
    Validates and sanitizes order inputs.
    
    Returns:
        Tuple of cleaned and converted types: (symbol, side, order_type, quantity, price, stop_price)
        
    Raises:
        ValidationException: If any validation rule fails.
    """
    # 1. Symbol Validation
    if not symbol or not isinstance(symbol, str):
        raise ValidationException("Symbol must be a valid non-empty string (e.g., 'BTCUSDT').")
    
    symbol_clean = symbol.strip().upper()
    if not symbol_clean.isalnum() or len(symbol_clean) < 3:
        raise ValidationException(f"Invalid symbol format: '{symbol}'. Must be alphanumeric (e.g., 'BTCUSDT').")

    # 2. Side Validation
    if not side or not isinstance(side, str):
        raise ValidationException("Order side is required.")
    
    side_clean = side.strip().upper()
    if side_clean not in VALID_SIDES:
        raise ValidationException(f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'.")

    # 3. Order Type Validation
    if not order_type or not isinstance(order_type, str):
        raise ValidationException("Order type is required.")
    
    type_clean = order_type.strip().upper()
    if type_clean not in VALID_TYPES:
        raise ValidationException(
            f"Invalid order type: '{order_type}'. Must be 'MARKET', 'LIMIT', or 'STOP'."
        )

    # 4. Quantity Validation
    try:
        qty_float = float(quantity)
    except (ValueError, TypeError):
        raise ValidationException(f"Quantity must be a valid numeric value, received: '{quantity}'.")

    if qty_float <= 0:
        raise ValidationException(f"Quantity must be greater than 0, received: {qty_float}.")

    # 5. Price Validation (Required for LIMIT and STOP)
    price_float = None
    if type_clean in {"LIMIT", "STOP"}:
        if price is None or price == "":
            raise ValidationException(f"Price is required for {type_clean} orders.")
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            raise ValidationException(f"Price must be a valid numeric value, received: '{price}'.")
            
        if price_float <= 0:
            raise ValidationException(f"Price must be greater than 0, received: {price_float}.")

    # 6. Stop Price Validation (Required for STOP orders)
    stop_price_float = None
    if type_clean == "STOP":
        if stop_price is None or stop_price == "":
            raise ValidationException("Stop Price is required for STOP (Stop-Limit) orders.")
        try:
            stop_price_float = float(stop_price)
        except (ValueError, TypeError):
            raise ValidationException(f"Stop Price must be a valid numeric value, received: '{stop_price}'.")
            
        if stop_price_float <= 0:
            raise ValidationException(f"Stop Price must be greater than 0, received: {stop_price_float}.")

    return symbol_clean, side_clean, type_clean, qty_float, price_float, stop_price_float
