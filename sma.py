import alpaca_trade_api as api
import threading
import time
import datetime
import datetime as dt
import bt 
import pandas as pd 
import pandas_datareader.data as web
import talib

API_Key = 'PKZMPG3T5B4KNAFUTRF3'
API_Secret = 'JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN'
API_End = 'https://paper-api.alpaca.markets'



class RSI:
  def __init__(self):
    self.alpaca = api.REST(API_Key, API_Secret, API_End, 'v2')
  def run(self):  
   start = dt.datetime(2000, 1, 1)
   end = dt.datetime(2021,12,31)
   df = web.DataReader('TSLA', 'stooq', start, end)
   df_RSI = talib.RSI(df['Close'])
   signal = df_RSI.values.tolist()
   #signal = df_RSI.copy()
   #signal[df_RSI.isnull()] = 0
   #signal[df_RSI > 70] = 1
   #signal[df_RSI < 30] = 2
   #signal[(df_RSI <= 70) & (df_RSI >= 30)] = 3
  
   
   if(signal > 0):
    print ('1')
   #elif(pd.Series(df_RSI < 30).all()):
    #print ('2')
   #elif([(pd.Series(df_RSI <= 70)) & (pd.Series(df_RSI >= 30))].any()): 
    #print ('3')
       
rsi = RSI()
rsi.run()


 #order = self.api.submit_order(symbol='TSLA', qty=1, side='buy')
    #rint(order)


 






