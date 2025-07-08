import time
import hmac
import hashlib
import requests

API_KEY = "b19521c4dba7435ac890c5b621309d97cd0d69ebe023892525d5ae23849dd3ec"
API_SECRET = "9ce822bfedb2216c5a375030936f644a059a7212216dbd9386a9dc3065688010"
BASE_URL = "https://testnet.binancefuture.com"

def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def log_response(response_data):
    with open("logs.txt", "a", encoding="utf-8") as f:  
        f.write(f"{time.ctime()} -> {response_data}\n\n")


def place_market_order(symbol, side, quantity):
    endpoint = '/fapi/v1/order'
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}&recvWindow=5000"
    signature = create_signature(params, API_SECRET)
    url = f"{BASE_URL}{endpoint}?{params}&signature={signature}"

    headers = {'X-MBX-APIKEY': API_KEY}
    res = requests.post(url, headers=headers)
    log_response(res.json())
    print(" Market Order Response:", res.json())

def place_limit_order(symbol, side, quantity, price):
    endpoint = '/fapi/v1/order'
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&side={side}&type=LIMIT&quantity={quantity}&price={price}&timeInForce=GTC&timestamp={timestamp}&recvWindow=5000"
    signature = create_signature(params, API_SECRET)
    url = f"{BASE_URL}{endpoint}?{params}&signature={signature}"

    headers = {'X-MBX-APIKEY': API_KEY}
    res = requests.post(url, headers=headers)
    log_response(res.json())
    print(" Limit Order Response:", res.json())

def place_stop_market_order(symbol, side, quantity, stop_price):
    endpoint = '/fapi/v1/order'
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&side={side}&type=STOP_MARKET&stopPrice={stop_price}&quantity={quantity}&timeInForce=GTC&timestamp={timestamp}&recvWindow=5000"
    signature = create_signature(params, API_SECRET)
    url = f"{BASE_URL}{endpoint}?{params}&signature={signature}"

    headers = {'X-MBX-APIKEY': API_KEY}
    res = requests.post(url, headers=headers)
    log_response(res.json())
    print(" Stop Market Order Response:", res.json())

def check_order_status(symbol, order_id):
    endpoint = "/fapi/v1/order"
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&orderId={order_id}&timestamp={timestamp}&recvWindow=5000"
    signature = create_signature(params, API_SECRET)
    url = f"{BASE_URL}{endpoint}?{params}&signature={signature}"

    headers = {'X-MBX-APIKEY': API_KEY}
    res = requests.get(url, headers=headers)
    print(" Order Status Response:", res.json())
    log_response(res.json())

# ======== CLI Starts Here =========

if __name__ == "__main__":
    print("=== Welcome to CryptoBot CLI ===")
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter side (BUY / SELL): ").upper()
    order_type = input("Enter order type (MARKET / LIMIT / STOP_MARKET): ").upper()
    quantity = input("Enter quantity: ")

    if order_type == "MARKET":
        place_market_order(symbol, side, quantity)

    elif order_type == "LIMIT":
        price = input("Enter price: ")
        place_limit_order(symbol, side, quantity, price)

    elif order_type == "STOP_MARKET":
        stop_price = input("Enter stop price: ")
        place_stop_market_order(symbol, side, quantity, stop_price)

    else:
        print(" Unsupported order type!")

    # Ask if user wants to check order status
    check = input("\n Do you want to check an order status? (y/n): ")
    if check.lower() == 'y':
        order_id = input("Enter order ID: ")
        check_order_status(symbol, order_id)
