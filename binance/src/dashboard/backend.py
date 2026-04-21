from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
from dotenv import load_dotenv

# Initialize dotenv so credentials are loaded
load_dotenv()

import os
import sys

# Inject the src/ folder into sys.path to allow absolute imports from 'bot'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.orders import (
    get_account_balance,
    get_open_orders,
    place_market_order,
    place_limit_order,
    cancel_order,
)
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price

app = FastAPI(title="Binance Bot Dashboard")

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class TradeRequest(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: float | None = None

@app.get("/")
def serve_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/balance")
def get_balance():
    try:
        balance = get_account_balance()
        return {"balance": balance}
    except Exception as e:
        logging.exception("Error fetching balance")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orders")
def fetch_orders():
    try:
        orders = get_open_orders()
        return {"orders": orders}
    except Exception as e:
        logging.exception("Error fetching orders")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/trade")
def place_trade(req: TradeRequest):
    try:
        symbol = validate_symbol(req.symbol)
        side = validate_side(req.side)
        
        # We manually check the inputs here to raise FastApi 400s instead of crashing
        if req.order_type not in ["MARKET", "LIMIT"]:
            raise HTTPException(status_code=400, detail="Type must be MARKET or LIMIT")
            
        qty = validate_quantity(req.quantity)
        
        if req.order_type == "MARKET":
            result = place_market_order(symbol, side, qty)
        else:
            price = validate_price(req.price, req.order_type)
            result = place_limit_order(symbol, side, qty, price)
            
        return {"success": True, "result": result}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.exception("Error placing trade")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/orders/{symbol}/{order_id}")
def delete_order(symbol: str, order_id: int):
    try:
        result = cancel_order(symbol.upper(), order_id)
        return {"success": True, "result": result}
    except Exception as e:
        logging.exception("Error canceling order")
        raise HTTPException(status_code=500, detail=str(e))
