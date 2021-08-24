import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class BC:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('ATVI', 'stooq', start, end)
   bc = talib.PLUS_DI(df['High'], df['Low'], df['Close'])
   bc1 = talib.PLUS_DM(df['High'], df['Low'], df['Close'])
   print(bc)
   print(bc1)
  
  
bc3 = BC()
bc3.run()
