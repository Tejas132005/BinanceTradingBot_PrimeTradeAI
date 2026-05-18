"""
Binance Client initialization module.
Manages secure loading of API credentials and configures the python-binance
Client specifically for Binance Futures Testnet (USDT-M) with automatic time synchronization.
"""

import os
import time
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException
from .exceptions import AuthenticationException, BinanceAPIExceptionWrapper, NetworkException
from .logging_config import setup_logger

logger = setup_logger("bot.client")

def get_binance_client() -> Client:
    """
    Initializes and returns a configured Binance Client for Futures Testnet.
    Automatically synchronizes local machine timestamp with Binance server time.
    
    Raises:
        AuthenticationException: If API keys are missing or invalid.
        BinanceAPIExceptionWrapper: If Binance API rejects credentials upon test.
        NetworkException: If connection fails.
    """
    # Ensure environment variables are loaded
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")

    if not api_key or not secret_key:
        logger.error("API credentials missing from environment variables.")
        raise AuthenticationException(
            "BINANCE_API_KEY and BINANCE_SECRET_KEY must be set in the .env file."
        )

    # Clean whitespace just in case of formatting issues in .env
    api_key = api_key.strip()
    secret_key = secret_key.strip()

    try:
        logger.info("Initializing Binance Client with testnet=True...")
        client = Client(api_key, secret_key, testnet=True)
        
        # Explicitly ensure Futures Testnet base URL is configured correctly
        # This guarantees compatibility across different python-binance versions
        client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        
        # Synchronize client timestamp with Binance Futures server time to prevent -1021 errors
        logger.info("Synchronizing local timestamp with Binance Futures server time...")
        server_time = client.futures_time()['serverTime']
        local_time = int(time.time() * 1000)
        client.timestamp_offset = server_time - local_time
        logger.info(f"Time synchronization complete. Offset: {client.timestamp_offset}ms")

        # Verify connection and credentials using futures_account
        logger.info("Verifying Futures Testnet connection and credentials...")
        client.futures_account()
        logger.info("Binance Futures Testnet client authenticated successfully.")
        return client

    except BinanceAPIException as e:
        logger.error(f"Binance API authentication error: {e.message} (Code: {e.code})")
        raise BinanceAPIExceptionWrapper(
            message=f"Binance API Error: {e.message}",
            status_code=e.status_code,
            error_code=e.code
        )
    except Exception as e:
        logger.error(f"Unexpected network or initialization error: {str(e)}")
        raise NetworkException(f"Failed to connect to Binance Futures Testnet: {str(e)}")
