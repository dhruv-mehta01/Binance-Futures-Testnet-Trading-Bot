import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

from bot.logging_config import setup_logger

logger = setup_logger(__name__)

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


def _get_credentials() -> tuple[str, str]:
    api_key = os.getenv("BINANCE_TESTNET_API_KEY", "").strip()
    secret = os.getenv("BINANCE_TESTNET_SECRET", "").strip()

    if not api_key or not secret:
        raise EnvironmentError(
            "Missing API credentials. Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET env vars."
        )
    return api_key, secret


def _sign_payload(params: dict, secret: str) -> str:
    query_string = urlencode(params)
    signature = hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return signature


def get_session() -> requests.Session:
    api_key, _ = _get_credentials()
    session = requests.Session()
    session.headers.update({
        "X-MBX-APIKEY": api_key,
    })
    return session


def _handle_request(method: str, url: str) -> dict:
    try:
        session = get_session()
        resp = session.request(method, url, timeout=10)
        resp.raise_for_status()
        response_data = resp.json()
        logger.debug(f"Response [{resp.status_code}]: {response_data}")
        return response_data

    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to Binance testnet. Check your internet connection.")
        raise ConnectionError("Failed to reach testnet.binancefuture.com — are you online?")

    except requests.exceptions.Timeout:
        logger.error("Request timed out after 10 seconds.")
        raise TimeoutError("Binance API request timed out.")

    except requests.exceptions.HTTPError as e:
        error_body = {}
        try:
            error_body = resp.json()
        except Exception:
            pass
        logger.error(f"HTTP error {resp.status_code}: {error_body}")
        raise RuntimeError(
            f"API error {resp.status_code}: {error_body.get('msg', str(e))}"
        )


def _build_signed_url(endpoint: str, params: dict) -> tuple[str, str]:
    api_key, secret = _get_credentials()
    url = f"{TESTNET_BASE_URL}{endpoint}"

    params["timestamp"] = int(time.time() * 1000)
    params["recvWindow"] = 5000

    query_string = urlencode(params)
    signature = _sign_payload(params, secret)
    full_url = f"{url}?{query_string}&signature={signature}"
    return full_url, url


def signed_post(endpoint: str, params: dict) -> dict:
    full_url, base_url = _build_signed_url(endpoint, params)
    logger.debug(f"POST {base_url} | params: { {k: v for k, v in params.items() if k != 'signature'} }")
    return _handle_request("POST", full_url)


def signed_get(endpoint: str, params: dict = None) -> dict:
    if params is None:
        params = {}
    full_url, base_url = _build_signed_url(endpoint, params)
    logger.debug(f"GET {base_url} | params: { {k: v for k, v in params.items() if k != 'signature'} }")
    return _handle_request("GET", full_url)


def signed_delete(endpoint: str, params: dict) -> dict:
    full_url, base_url = _build_signed_url(endpoint, params)
    logger.debug(f"DELETE {base_url} | params: { {k: v for k, v in params.items() if k != 'signature'} }")
    return _handle_request("DELETE", full_url)

