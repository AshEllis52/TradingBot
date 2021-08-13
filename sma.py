import alpaca_trade_api as tradeapi
import threading
import time
import datetime
import datetime as dt
import bt 
import pandas 
import pandas_datareader.data as web
import talib

API_Key = 'PKZMPG3T5B4KNAFUTRF3'
API_Secret = 'JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN'
API_End = 'https://paper-api.alpaca.markets'


class EmaSma:
  def __init__(self):
    self.alpaca = tradeapi.REST(API_Key, API_Secret, API_End, 'v2')

  def run(self):  
   start = dt.datetime(2000, 1, 1)
   end = dt.datetime(2021,12,31)
   df = web.DataReader('TSLA', 'stooq', start, end)
   # Calculate the EMA
   #sma = df.rolling(20).mean()
   #ema = df.rolling(20).mean()
   sma = talib.SMA(df['Close'], timeperiod = 20)
   ema = talib.EMA(df['Close'], timeperiod = 20 )
   
    
   
   if(sma > ema): 
    print('SMA has crossed EMA')
    order = api.submit_order(symbol='TSLA', qty=1, side='buy')
    print(order)
   
   else:
      pass 

es = EmaSma()
es.run()













