import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class BB:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('BA', 'stooq', start, end)
   upper, mid, lower = talib.BBANDS(df['Close'], nbdevup=2, nbdevdn=2, timeperiod=20)
   upper.to_numpy()
   mid.to_numpy()
   lower.to_numpy()
   print(upper.index[20]) 
   print(mid.index[19]) 
   print(lower.index[19]) 
   
    
  
  
  
  
    
    
bb = BB()
bb.run()
