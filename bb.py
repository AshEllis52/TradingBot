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
   end = date.today(df['Close'])
   df = web.DataReader('BA', 'stooq', start, end)
   upper, mid, lower = talib.BBANDS(df['Close'], nbdevup=2, nbdevdn=2, timeperiod = 20)
   upper.to_numpy()
   mid.to_numpy()
   lower.to_numpy()
  
  
   if((mid.values[19]) > (upper.values[24])): #if SMA(mid) today is above what upper was 5 days ago stock is overbought 
    print("Stock is above mean value, selling position")
    api.submit_order(symbol='BA', qty=10, side='sell')
    
   elif (mid.values[19] < lower.values[24]):
    print("Stock is below mean value, buying position") #if SMA(mid) today is below what lower was 5 days ago stock is underbought  
    api.submit_order(symbol='BA', qty=10, side='buy')
    
   elif [((mid.values[19]) > lower.values[24]) & ((mid.values[19] < upper.values[24])]: 
    print("Stock is within mean value, holding position") #if SMA(mid) today is between  lower & upper 5 days ago stock is at mean value  
       
bb = BB()
bb.run()
