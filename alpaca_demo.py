from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
import config

# TODO: convert to functions to be called

# set up client
client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)
account = dict(client.get_account())


# print account information
for k, v in account.items():
    print(f"{k:30}{v}")


# set up order
order_details = MarketOrderRequest(
    symbol = "SPY",
    qty = 100,
    side = OrderSide.BUY,               # long or short
    time_in_force = TimeInForce.DAY     # how long an order will remain active before it expires
)
# place order
order = client.submit_order(order_data = order_details)


# print trade logs
trades = TradingStream(config.API_KEY, config.SECRET_KEY, paper=True)

async def trade_status(data):
    # trade updates will arrive in our async handler
    print(data)

# subscribe to trade updates and supply the handler as a parameter
trades.subscribe_trade_updates(trade_status)
# start our websocket streaming
trades.run()


# print positions
assets = [asset for asset in client.get_all_positions()]
positions = [(asset.symbol, asset.qty, asset.current_price) for asset in assets]
print("Postions")
print(f"{'Symbol':9}{'Qty':>4}{'Value':>15}")
print("-" * 28)
for position in positions:
    print(f"{position[0]:9}{position[1]:>4}{float(position[1]) * float(position[2]):>15.2f}")


# close all positions
client.close_all_positions(cancel_orders=True)