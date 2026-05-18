"""
Automated Test Suite for Binance Futures Testnet Trading Bot.
Executes 10 distinct test cases covering valid orders, validation failures,
and exchange filter rejections, displaying a clean ASCII terminal report.
"""

import sys
import time
from typing import Dict, Any, Tuple
from bot.orders import place_order
from bot.exceptions import TradingBotException, ValidationException, BinanceAPIExceptionWrapper

# ANSI color codes for premium terminal formatting
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def run_test_case(test_num: int, name: str, params: Dict[str, Any], expected_success: bool) -> Tuple[bool, str]:
    """
    Executes a single test case and evaluates the result against expectations.
    """
    print(f"\n{BOLD}{CYAN}[Test {test_num}] {name}{RESET}")
    print(f"   Parameters: {params}")
    print("   Executing order...", end="", flush=True)

    try:
        # Call core bot placement logic
        result = place_order(**params)
        print("\r   Executing order... Done.   ")
        
        if expected_success:
            order_id = result.get("data", {}).get("orderId", "N/A")
            msg = f"{GREEN}SUCCESS [PASS]{RESET} (Order ID: {order_id})"
            print(f"   --> Result: {msg}")
            return True, f"SUCCESS (Order ID: {order_id})"
        else:
            msg = f"{RED}UNEXPECTED SUCCESS [FAIL]{RESET} (Order should have failed!)"
            print(f"   --> Result: {msg}")
            return False, "UNEXPECTED SUCCESS"

    except (ValidationException, BinanceAPIExceptionWrapper, TradingBotException) as e:
        print("\r   Executing order... Done.   ")
        error_msg = str(e)
        
        if not expected_success:
            msg = f"{YELLOW}UNSUCCESSFUL (Expected Failure Caught) [PASS]{RESET}\n       Reason: {error_msg}"
            print(f"   --> Result: {msg}")
            return True, f"UNSUCCESSFUL (Expected Failure: {error_msg.split('(')[0].strip()})"
        else:
            msg = f"{RED}UNSUCCESSFUL (Unexpected Failure) [FAIL]{RESET}\n       Reason: {error_msg}"
            print(f"   --> Result: {msg}")
            return False, f"UNEXPECTED FAILURE ({error_msg})"
    except Exception as e:
        print("\r   Executing order... Done.   ")
        msg = f"{RED}CRITICAL FAILURE [FAIL]{RESET} ({str(e)})"
        print(f"   --> Result: {msg}")
        return False, f"CRITICAL FAILURE ({str(e)})"


def main():
    print(f"\n{BOLD}{YELLOW}================================================================================{RESET}")
    print(f"{BOLD}{GREEN}BINANCE FUTURES TESTNET - 10 AUTOMATED TEST CASES{RESET}")
    print(f"{BOLD}{YELLOW}================================================================================{RESET}")
    print("Executing automated test suite across valid orders, validation rules, and exchange filters...\n")

    test_cases = [
        # --- Valid Test Cases (Expected: SUCCESS) ---
        {
            "num": 1, "name": "Valid Market Buy (Long Entry)", "expected": True,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "MARKET", "quantity": 0.001}
        },
        {
            "num": 2, "name": "Valid Market Sell (Short Entry / Close)", "expected": True,
            "params": {"symbol": "BTCUSDT", "side": "SELL", "order_type": "MARKET", "quantity": 0.001}
        },
        {
            "num": 3, "name": "Valid Limit Buy (Dip Buying)", "expected": True,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "LIMIT", "quantity": 0.001, "price": 64000}
        },
        {
            "num": 4, "name": "Stop-Limit Buy (Exchange Algo Restriction)", "expected": False,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "STOP", "quantity": 0.001, "price": 66050, "stop_price": 66000}
        },
        
        # --- Invalid Test Cases (Expected: UNSUCCESSFUL / EXPECTED FAILURE) ---
        {
            "num": 5, "name": "Invalid Symbol Format", "expected": False,
            "params": {"symbol": "INVALID@PAIR", "side": "BUY", "order_type": "MARKET", "quantity": 0.001}
        },
        {
            "num": 6, "name": "Invalid Negative Quantity", "expected": False,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "MARKET", "quantity": -0.005}
        },
        {
            "num": 7, "name": "Invalid Order Type", "expected": False,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "UNKNOWN_TYPE", "quantity": 0.001}
        },
        {
            "num": 8, "name": "Missing Limit Price on LIMIT Order", "expected": False,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "LIMIT", "quantity": 0.001, "price": None}
        },
        {
            "num": 9, "name": "Price Outside Exchange Filter Band (Code -4013)", "expected": False,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "LIMIT", "quantity": 0.001, "price": 100}
        },
        {
            "num": 10, "name": "Exceeding Max Quantity / Insufficient Margin", "expected": False,
            "params": {"symbol": "BTCUSDT", "side": "BUY", "order_type": "MARKET", "quantity": 5000}
        }
    ]

    results_summary = []
    passed_count = 0

    for tc in test_cases:
        passed, summary_text = run_test_case(tc["num"], tc["name"], tc["params"], tc["expected"])
        results_summary.append((tc["num"], tc["name"], passed, summary_text))
        if passed:
            passed_count += 1
        time.sleep(1) # Brief pause between API calls to prevent rate-limiting

    print(f"\n{BOLD}{YELLOW}================================================================================{RESET}")
    print(f"{BOLD}{GREEN}TEST EXECUTION SUMMARY: {passed_count} / 10 Tests Passed{RESET}")
    print(f"{BOLD}{YELLOW}================================================================================{RESET}\n")

    print(f"{BOLD}{'#':<4} {'Test Case Name':<45} {'Status':<15} {'Details':<30}{RESET}")
    print("-" * 100)
    for num, name, passed, details in results_summary:
        status_str = f"{GREEN}PASSED{RESET}" if passed else f"{RED}FAILED{RESET}"
        print(f"{num:<4} {name:<45} {status_str:<15} {details:<30}")
    print("\n")

if __name__ == "__main__":
    main()
