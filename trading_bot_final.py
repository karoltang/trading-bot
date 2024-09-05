from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca_trade_api import REST, TimeFrame
import talib as ta
import time
from datetime import datetime, timedelta
import pytz

api_key = "api_key" #replace w own
secret_key = "secret_key"
trading_client = TradingClient(api_key, secret_key, paper=True, url_override = "https://paper-api.alpaca.markets")
rest_api = REST(api_key, secret_key, base_url="https://paper-api.alpaca.markets")

# Define the symbol and time frame
symbol = "AAPL"  
timeframe = TimeFrame.Day #can use other symbols and time frames

# Function to get the latest price data
def get_latest_data(symbol):
    # Fetch historical data
    today = (datetime.now(pytz.timezone('America/New_York')) - timedelta(hours=1)).date()
    ten_days_ago = today - timedelta(days=10)
    barset = rest_api.get_bars(symbol, timeframe, start=ten_days_ago.isoformat(), end=today.isoformat()).df
    return barset

# Function for placing order
def place_order(side, qty):
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=TimeInForce.DAY #?
    )
    trading_client.submit_order(order)

# Tests conditions and executes trade
def trading_bot():
    while True:
        try:
            # Fetch latest data
            data = get_latest_data(symbol)

            # Calculate momentum and RSI
            data['momentum'] = ta.MOM(data['close'], timeperiod=10)
            data['rsi'] = ta.RSI(data['close'], timeperiod=14)

            # Get the latest values - latest data is at the bottom
            latest_momentum = data['momentum'].iloc[-1]
            previous_momentum = data['momentum'].iloc[-2]
            latest_rsi = data['rsi'].iloc[-1]

            # Buy signal: Momentum crosses 0 upwards and RSI <= 30
            if previous_momentum < 0 and latest_momentum > 0 and latest_rsi <= 30:
                print("Buy Signal Detected")
                place_order(OrderSide.BUY, 1)  # Adjust quantity as needed if wanted

            # Sell signal: Momentum crosses 0 downwards and RSI >= 70
            elif previous_momentum > 0 and latest_momentum < 0 and latest_rsi >= 70:
                print("Sell Signal Detected")
                place_order(OrderSide.SELL, 1)

        except Exception as e:
            print(f"Error: {e}")
            exit()

        # Sleep to avoid hitting API rate limits
        time.sleep(60)

# Run the bot
trading_bot()

