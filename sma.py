import alpaca_trade_api as api
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
signal = signal


class RSI:
  def __init__(self):
    self.alpaca = api.REST(API_Key, API_Secret, API_End, 'v2')

  def run(self):  
   start = dt.datetime(2000, 1, 1)
   end = dt.datetime(2021,12,31)
   df = web.DataReader('TSLA', 'stooq', start, end)
   signal = 0
   df['RSI'] = talib.RSI(df['Close'])
    if (df['RSI'] > 70):
      signal = 1
    elif (df['RSI'] < 30):
      signal = 2
    elif (df['RSI'] <= 70) & (df['RSI'] >= 30)]:
      signal = 3
   
   
   if(signal == 1): 
    print('1')
    #order = api.submit_order(symbol='TSLA', qty=1, side='buy')
    #rint(order)
   elif(signal == 2)
    print('2')
   elif(signal == 3)
    print('3')
    
    
    
   
   #signal[df['RSI'] > 70] = -1
   #signal[df['RSI'] < 30] = 1
   #signal[(df['RSI'] <= 70) & (df['RSI'] >= 30)] = 0

RSI = rsi()
rsi.run()













