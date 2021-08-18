import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class RSI:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('TSLA', 'stooq', start, end)
   df_RSI = talib.RSI(df['Close'])
   df_RSI.to_numpy()  
  
   if((df_RSI.values[13]) > 70):
    print('Stock is over bought, selling postion') 
    api.submit_order(symbol='TSLA', qty=10, side='sell')
    
   elif((df_RSI.values[13]) < 30):
    print('Stock is over sold, buying postion') 
    api.submit_order(symbol='TSLA', qty=10, side='buy')
    
   elif[((df_RSI.values[13]) <= 70) & ((df_RSI.values[13]) >= 30)]:
    print('Holding stock') 
       
rsi = RSI()
rsi.run()





 






