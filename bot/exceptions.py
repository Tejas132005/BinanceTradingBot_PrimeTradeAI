"""
Custom exception definitions for the Trading Bot.
Provides clear separation of error types for robust handling and logging.
"""

class TradingBotException(Exception):
    """Base exception class for all custom trading bot exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationException(TradingBotException):
    """Raised when user input or order parameters fail validation."""
    pass


class AuthenticationException(TradingBotException):
    """Raised when API credentials are missing or invalid."""
    pass


class BinanceAPIExceptionWrapper(TradingBotException):
    """
    Wrapper for exceptions raised by the Binance API.
    Captures status code, error code, and error message.
    """
    def __init__(self, message: str, status_code: int = None, error_code: int = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self):
        err_details = []
        if self.status_code:
            err_details.append(f"HTTP {self.status_code}")
        if self.error_code:
            err_details.append(f"Code {self.error_code}")
        prefix = f"[{', '.join(err_details)}] " if err_details else ""
        return f"{prefix}{self.message}"


class NetworkException(TradingBotException):
    """Raised when network connection issues or timeouts occur."""
    pass
