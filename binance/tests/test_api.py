import os
import time
import requests
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv

def test_api():
    load_dotenv()
    api_key = os.getenv("BINANCE_TESTNET_API_KEY", "").strip()
    secret = os.getenv("BINANCE_TESTNET_SECRET", "").strip()
    
    if not api_key or not secret:
        print("Missing keys!")
        return
        
    print(f"API Key: {api_key[:10]}... length: {len(api_key)}")
    print(f"Secret: {secret[:10]}... length: {len(secret)}")
    print(f"Secret ends with quote? {secret.endswith(chr(34))} or {secret.endswith(chr(39))}")
    
    url = "https://testnet.binancefuture.com/fapi/v1/order"
    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 0.01,
        "timestamp": int(time.time() * 1000),
        "recvWindow": 5000
    }
    
    query_string = urlencode(params)
    signature = hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    
    print(f"Query string: {query_string}")
    print(f"Signature: {signature}")
    
    # Let's try 3 methods:
    # 1. request dict directly (often fails if requests re-encodes differently)
    print("\n--- Try 1: requests normal data dict ---")
    d1 = params.copy()
    d1["signature"] = signature
    session = requests.Session()
    session.headers.update({"X-MBX-APIKEY": api_key})
    try:
        r1 = session.post(url, data=d1, timeout=5)
        print(f"HTTP {r1.status_code}: {r1.text}")
    except Exception as e:
        print(e)
        
    # 2. direct body string
    print("\n--- Try 2: direct body string ---")
    body_str = f"{query_string}&signature={signature}"
    try:
        r2 = session.post(url, data=body_str, timeout=5)
        print(f"HTTP {r2.status_code}: {r2.text}")
    except Exception as e:
        print(e)
        
    # 3. URL params
    print("\n--- Try 3: url params ---")
    full_url = f"{url}?{query_string}&signature={signature}"
    try:
        r3 = session.post(full_url, timeout=5)
        print(f"HTTP {r3.status_code}: {r3.text}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test_api()
