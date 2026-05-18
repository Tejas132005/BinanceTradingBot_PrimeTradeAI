"""
Command Line Interface (CLI) for the Trading Bot.
Enables execution of MARKET, LIMIT, and STOP orders directly from the terminal.
"""

import sys
import argparse
from bot.orders import place_order
from bot.exceptions import TradingBotException, ValidationException, AuthenticationException, BinanceAPIExceptionWrapper
from bot.logging_config import setup_logger

logger = setup_logger("cli.main")

def main():
    """Parses CLI arguments and executes the trading order."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--symbol", required=True, type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, type=str, choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("--type", required=True, type=str, choices=["MARKET", "LIMIT", "STOP"], help="Order type: MARKET, LIMIT, or STOP")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity (e.g., 0.001)")
    parser.add_argument("--price", type=float, help="Order price (Required for LIMIT and STOP orders)")
    parser.add_argument("--stop-price", type=float, help="Stop price (Required for STOP orders)")

    args = parser.parse_args()

    logger.info(f"CLI execution started with arguments: {args}")

    try:
        result = place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        
        # Print the exact formatted summary required by project specifications
        print("\n" + result["formatted_summary"] + "\n")
        logger.info("CLI order execution completed successfully.")
        sys.exit(0)

    except ValidationException as e:
        logger.warning(f"CLI Validation Error: {e.message}")
        print(f"\n[VALIDATION ERROR] {e.message}\n")
        sys.exit(1)

    except AuthenticationException as e:
        logger.error(f"CLI Authentication Error: {e.message}")
        print(f"\n[AUTHENTICATION ERROR] {e.message}\n")
        sys.exit(1)

    except BinanceAPIExceptionWrapper as e:
        logger.error(f"CLI Binance API Error: {str(e)}")
        print(f"\n[BINANCE API ERROR] {str(e)}\n")
        sys.exit(1)

    except TradingBotException as e:
        logger.error(f"CLI Trading Bot Error: {e.message}")
        print(f"\n[TRADING BOT ERROR] {e.message}\n")
        sys.exit(1)

    except Exception as e:
        logger.critical(f"CLI Unexpected System Error: {str(e)}", exc_info=True)
        print(f"\n[SYSTEM ERROR] An unexpected error occurred: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
