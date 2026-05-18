"""
Binance Futures Testnet Trading Bot Package.
Provides client management, order placement, validation, and logging.
"""

from .exceptions import (
    TradingBotException,
    ValidationException,
    AuthenticationException,
    BinanceAPIExceptionWrapper,
    NetworkException,
)
from .logging_config import setup_logger
from .validators import validate_order_input
from .client import get_binance_client
from .orders import place_order

__all__ = [
    "TradingBotException",
    "ValidationException",
    "AuthenticationException",
    "BinanceAPIExceptionWrapper",
    "NetworkException",
    "setup_logger",
    "validate_order_input",
    "get_binance_client",
    "place_order",
]
