from bot.logging_config import setup_logger

logger = setup_logger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}

# just the most common futures pairs — not an exhaustive list
KNOWN_SYMBOLS = {
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "MATICUSDT", "LTCUSDT", "DOTUSDT",
}


def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if symbol not in KNOWN_SYMBOLS:
        # warn but don't hard block — testnet supports other pairs too
        logger.warning(f"Symbol '{symbol}' not in known list, proceeding anyway")
    return symbol


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT.")
    return order_type


def validate_quantity(qty: float) -> float:
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {qty}.")
    if qty > 1000:
        # sanity check — shouldn't be placing 1000 BTC orders on testnet accidentally
        logger.warning(f"Large quantity detected: {qty}. Double-check before proceeding.")
    return qty


def validate_price(price: float | None, order_type: str) -> float | None:
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price is required and must be > 0 for LIMIT orders.")
        return price
    if price is not None:
        logger.warning("Price provided for MARKET order — it will be ignored.")
    return None
