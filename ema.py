import alpaca_trade_api as tradeapi
import threading
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class EMA:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('AAPL', 'stooq', start, end)
   df_EMAS = talib.EMA(df['Close'], timeperiod = 12)
   df_EMAL = talib.EMA(df['Close'], timeperiod = 26)
   adx = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod = 21)
   adx.to_numpy()
   df_EMAS.to_numpy()  
   df_EMAL.to_numpy()
  
   if(((df_EMAS.values[12]) > (df_EMAL.values[26]) & ((adx.values[21]) > 25))):
    print('The trend indicates a buying postion, buying stock') 
    api.submit_order(symbol='AAPL', qty=10, side='buy')
    
   elif((df_EMAL.values[26]) > (df_EMAS.values[12])):
    print('The trend indicates a selling  postion, selling stock') 
    api.submit_order(symbol='AAPL', qty=10, side='sell')
    
   elif((df_EMAL.values[26]) == (df_EMAS.values[12])):
    print('Holding stock') 
       
ema = EMA()
ema.run()

