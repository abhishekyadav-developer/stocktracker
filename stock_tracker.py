"""Stock Portfolio Tracker - beginner-friendly command-line project.

Prices are hardcoded sample prices for learning purposes. They are not live quotes.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

# Sample prices in USD. Edit this dictionary to change the available stocks.
STOCK_PRICES: dict[str, float] = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 150.00,
    "MSFT": 420.00,
    "AMZN": 190.00,
    "NVDA": 140.00,
}

REPORT_FILE = Path(__file__).with_name("portfolio_report.csv")


def show_available_stocks() -> None:
    """Print the stock symbols and their sample prices."""
    print("\nAvailable stocks (sample prices in USD)")
    print("-" * 42)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol:<10} ${price:,.2f}")


def get_positive_quantity() -> int:
    """Ask until the user enters a positive whole-number quantity."""
    while True:
        raw_quantity = input("Enter quantity: ").strip()
        try:
            quantity = int(raw_quantity)
            if quantity > 0:
                return quantity
            print("Quantity must be greater than zero.")
        except ValueError:
            print("Please enter a valid whole number, such as 5.")


def collect_portfolio() -> dict[str, int]:
    """Collect stock symbols and quantities from the user."""
    portfolio: dict[str, int] = {}
    print("\nEnter a stock symbol, or type DONE to calculate your portfolio.")

    while True:
        symbol = input("\nStock symbol: ").strip().upper()
        if symbol == "DONE":
            break
        if not symbol:
            print("Please enter a stock symbol.")
            continue
        if symbol not in STOCK_PRICES:
            print(f"{symbol} is not in the available stock list.")
            print("Type LIST to see available stocks, or try another symbol.")
            # Allow the user to view the list without losing the current entry.
            if symbol == "LIST":
                show_available_stocks()
            continue

        quantity = get_positive_quantity()
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"Added {quantity} share(s) of {symbol}.")

    return portfolio


def calculate_total(portfolio: dict[str, int]) -> float:
    """Return the total portfolio value using the hardcoded prices."""
    return sum(STOCK_PRICES[symbol] * quantity for symbol, quantity in portfolio.items())


def display_summary(portfolio: dict[str, int]) -> float:
    """Print each holding and the total investment; return the total."""
    print("\n" + "=" * 58)
    print("PORTFOLIO SUMMARY")
    print("=" * 58)

    if not portfolio:
        print("No stocks were added to your portfolio.")
        return 0.0

    print(f"{'STOCK':<10}{'QUANTITY':>10}{'PRICE':>16}{'VALUE':>18}")
    print("-" * 58)
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * quantity
        print(f"{symbol:<10}{quantity:>10}{price:>15,.2f}  {value:>15,.2f}")

    total = calculate_total(portfolio)
    print("-" * 58)
    print(f"TOTAL INVESTMENT: ${total:,.2f}")
    print("\nNote: These are hardcoded sample prices, not live market prices.")
    return total


def save_report(portfolio: dict[str, int], total: float) -> Path | None:
    """Save holdings and total to a CSV file next to this script."""
    if not portfolio:
        return None

    try:
        with REPORT_FILE.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Stock", "Quantity", "Price (USD)", "Investment Value (USD)"])
            for symbol, quantity in portfolio.items():
                price = STOCK_PRICES[symbol]
                writer.writerow([symbol, quantity, f"{price:.2f}", f"{price * quantity:.2f}"])
            writer.writerow([])
            writer.writerow(["Generated at", datetime.now().astimezone().isoformat(timespec="seconds")])
            writer.writerow(["Total investment (USD)", f"{total:.2f}"])
        return REPORT_FILE
    except OSError as error:
        print(f"Could not save the CSV report: {error}")
        return None


def main() -> None:
    print("=" * 58)
    print("             STOCK PORTFOLIO TRACKER")
    print("=" * 58)
    show_available_stocks()
    portfolio = collect_portfolio()
    total = display_summary(portfolio)

    if portfolio:
        saved_path = save_report(portfolio, total)
        if saved_path:
            print(f"\nCSV report saved successfully: {saved_path.name}")

    print("\nThank you for using Stock Portfolio Tracker!")


if __name__ == "__main__":
    main()
