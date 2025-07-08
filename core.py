import time
import requests
from .utils import create_signature, log_response
from config import API_KEY, API_SECRET, BASE_URL

class TradingBot:
    def __init__(self):
        self.headers = {'X-MBX-APIKEY': API_KEY}

    def _send_request(self, method, endpoint, params):
        params['timestamp'] = int(time.time() * 1000)
        params['recvWindow'] = 5000
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = create_signature(query_string, API_SECRET)
        url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
        response = requests.request(method, url, headers=self.headers)
        log_response(response.json())
        return response.json()

    def place_market_order(self, symbol, side, quantity):
        return self._send_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        })

    def place_limit_order(self, symbol, side, quantity, price):
        return self._send_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC"
        })

    def place_stop_market_order(self, symbol, side, quantity, stop_price):
        return self._send_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "STOP_MARKET",
            "stopPrice": stop_price,
            "quantity": quantity,
            "timeInForce": "GTC"
        })

    def check_order_status(self, symbol, order_id):
        return self._send_request("GET", "/fapi/v1/order", {
            "symbol": symbol,
            "orderId": order_id
        })
