import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class DI:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('MSFT', 'stooq', start, end)
   di = talib.PLUS_DI(df['High'], df['Low'], df['Close'], timeperiod = 14)
   di1 = talib.MINUS_DI(df['High'], df['Low'], df['Close'], timeperiod = 14)
   di.to_numpy()
   di1.to_numpy()
   
   if (di.values[13] > di1.values[13]):
    print('The trend indicates an uptrend, buying  stock') 
    api.submit_order(symbol='MSFT', qty=10, side='buy')
   
   elif (di1.values[13] > di.values[13]):
    print('The trend indicates a downtrend, selling  stock') 
    api.submit_order(symbol='MSFT', qty=10, side='sell')
   
   elif (di.values[13] = di1.values[13]):
    print('No trend indentified, holding position') 
  
  
di = DI()
di.run()
