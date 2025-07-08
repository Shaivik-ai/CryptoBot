from bot.core import TradingBot

bot = TradingBot()

print("=== Welcome to CryptoBot CLI ===")
symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
side = input("Enter side (BUY / SELL): ").upper()
order_type = input("Enter order type (MARKET / LIMIT / STOP_MARKET): ").upper()
quantity = input("Enter quantity: ")

if order_type == "MARKET":
    res = bot.place_market_order(symbol, side, quantity)
elif order_type == "LIMIT":
    price = input("Enter limit price: ")
    res = bot.place_limit_order(symbol, side, quantity, price)
elif order_type == "STOP_MARKET":
    stop_price = input("Enter stop price: ")
    res = bot.place_stop_market_order(symbol, side, quantity, stop_price)
else:
    print("Invalid order type.")
    exit()

print(" Order Placed:", res)

check = input("Do you want to check order status? (y/n): ")
if check.lower() == "y":
    order_id = input("Enter order ID: ")
    status = bot.check_order_status(symbol, order_id)
    print(" Order Status:", status)
