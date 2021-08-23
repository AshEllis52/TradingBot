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
   upper, mid, lower = talib.BBANDS(df['Close'], nbdevup=2, nbdevdn=2, timeperiod = 20)
   todayPrice = df['Close']
   todayPrice.to_numpy()
   upper.to_numpy()
   mid.to_numpy()
   lower.to_numpy()
  
  
   if((todayPrice.values[0]) > (upper.values[19])): 
    print("Stock is above mean value, selling position")
    api.submit_order(symbol='BA', qty=10, side='sell')
    
   elif((todayPrice.values[0]) < (lower.values[19])):
    print("Stock is below mean value, buying position") 
    api.submit_order(symbol='BA', qty=10, side='buy')
    
   elif [((todayPrice.values[0]) < (upper.values[19])) & ((todayPrice.values[0]) > (lower.values[19]))]: 
    print("Stock is within mean value, holding position")  
       
bb = BB()
bb.run()
