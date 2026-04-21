#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
CLI entry point — uses Typer for clean argument parsing
"""
import os
import sys
from typing import Optional

# Ensure that 'src/' is in path so absolute imports from bot work smoothly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from bot.logging_config import setup_logger
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.orders import place_market_order, place_limit_order, format_order_result

app = typer.Typer(
    name="trading-bot",
    help="Binance Futures Testnet CLI — place market and limit orders",
    add_completion=False,
)
console = Console()
logger = setup_logger("cli")


def print_order_summary(symbol, side, order_type, quantity, price=None):
    summary_lines = [
        f"[bold]Symbol:[/bold]     {symbol}",
        f"[bold]Side:[/bold]       {side}",
        f"[bold]Type:[/bold]       {order_type}",
        f"[bold]Quantity:[/bold]   {quantity}",
    ]
    if price:
        summary_lines.append(f"[bold]Price:[/bold]      {price}")

    summary_text = "\n".join(summary_lines)
    console.print(Panel(summary_text, title="📋 Order Request", border_style="blue"))


@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair, e.g. BTCUSDT"),
    side: str = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Amount to buy/sell"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (required for LIMIT orders)"),
):
    """Place a futures order on Binance Testnet."""

    logger.info(f"New order request | symbol={symbol} side={side} type={order_type} qty={quantity} price={price}")

    # validate all inputs before touching the API
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(price, order_type)
    except ValueError as e:
        console.print(f"[red]❌ Validation error:[/red] {e}")
        logger.error(f"Validation failed: {e}")
        raise typer.Exit(code=1)

    # show summary before sending
    print_order_summary(symbol, side, order_type, quantity, price)

    console.print("[yellow]⏳ Sending order to Binance Testnet...[/yellow]")

    try:
        if order_type == "MARKET":
            result = place_market_order(symbol, side, quantity)
        else:
            result = place_limit_order(symbol, side, quantity, price)

        console.print(format_order_result(result))

    except EnvironmentError as e:
        console.print(f"[red]❌ Config error:[/red] {e}")
        logger.error(f"Environment error: {e}")
        raise typer.Exit(code=1)

    except (ConnectionError, TimeoutError) as e:
        console.print(f"[red]❌ Network error:[/red] {e}")
        logger.error(f"Network error: {e}")
        raise typer.Exit(code=1)

    except RuntimeError as e:
        console.print(f"[red]❌ API error:[/red] {e}")
        logger.error(f"API error: {e}")
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[red]❌ Unexpected error:[/red] {e}")
        logger.exception(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
