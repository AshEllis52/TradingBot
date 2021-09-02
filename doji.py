import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class DOJI:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('SPY', 'google', start, end)
   df_d = talib.CDLDOJISTAR(df['Open'], df['High'], df['Low'], df['Close']) 
   print(df_d)
    
doji = DOJI()
doji.run()
