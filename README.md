# trading-bot

This bot currently trades AAPL stock, but can be replaced with any other symbol. The bot gets data from the past 10 days and calculates momentum and RSI. The bot will buy 1 share if the momentum has crossed 0 upwards and if the RSI is <= 30, indicating price movement upwards (momentum) and that the asset is oversold and might rebound (RSI). Conversely, the bot will sell 1 share if momentum has crossed 0 downwards and RSI is >= 70, indicated price movement downwards and an overbought asset that will come back down. 
