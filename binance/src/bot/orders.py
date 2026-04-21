from bot.client import signed_post, signed_get, signed_delete
from bot.logging_config import setup_logger

logger = setup_logger(__name__)

ORDER_ENDPOINT = "/fapi/v1/order"
OPEN_ORDERS_ENDPOINT = "/fapi/v1/openOrders"
BALANCE_ENDPOINT = "/fapi/v2/balance"


def get_account_balance() -> float:
    logger.info("Fetching USDT account balance")
    result = signed_get(BALANCE_ENDPOINT)
    for asset in result:
        if asset.get("asset") == "USDT":
            # return the cross wallet balance for USDT
            return float(asset.get("balance", 0.0))
    return 0.0


def get_open_orders(symbol: str = None) -> list:
    logger.info(f"Fetching open orders (symbol={symbol or 'ALL'})")
    params = {"symbol": symbol} if symbol else {}
    result = signed_get(OPEN_ORDERS_ENDPOINT, params)
    return result


def cancel_order(symbol: str, order_id: int) -> dict:
    logger.info(f"Canceling order {order_id} for {symbol}")
    params = {
        "symbol": symbol,
        "orderId": order_id,
    }
    result = signed_delete(ORDER_ENDPOINT, params)
    logger.info(f"Order canceled | status={result.get('status')}")
    return result


def place_market_order(symbol: str, side: str, quantity: float) -> dict:
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    logger.info(f"Placing MARKET order | {side} {quantity} {symbol}")
    result = signed_post(ORDER_ENDPOINT, params)
    logger.info(f"Order placed successfully | orderId={result.get('orderId')} status={result.get('status')}")
    return result


def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC",  # Good Till Cancelled
    }
    logger.info(f"Placing LIMIT order | {side} {quantity} {symbol} @ {price}")
    result = signed_post(ORDER_ENDPOINT, params)
    logger.info(f"Order placed successfully | orderId={result.get('orderId')} status={result.get('status')}")
    return result


def format_order_result(order: dict) -> str:
    order_id = order.get("orderId", "N/A")
    status = order.get("status", "N/A")
    exec_qty = order.get("executedQty", "0")
    avg_price = order.get("avgPrice") or order.get("price", "N/A")
    symbol = order.get("symbol", "")
    side = order.get("side", "")
    order_type = order.get("type", "")

    lines = [
        "",
        "  ✅ Order Submitted Successfully",
        f"  ┌─ Order ID   : {order_id}",
        f"  ├─ Symbol     : {symbol}",
        f"  ├─ Side       : {side}",
        f"  ├─ Type       : {order_type}",
        f"  ├─ Status     : {status}",
        f"  ├─ Executed   : {exec_qty}",
        f"  └─ Avg Price  : {avg_price}",
        "",
    ]
    return "\n".join(lines)
