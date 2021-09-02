import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib
import yfinance as yfin
yfin.pdr_override()

import pandas
from pandas_datareader import data as pdr

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class DOJI:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.get_data_yahoo('VFINX', start, end)
   df_d = talib.CDLDOJISTAR(df['Open'], df['High'], df['Low'], df['Close'])
   df_ms = talib.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
   df_e = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
  
  
  #if (df_d = 100)
   #print('The trend indicates moderate momentum, buying some stock') 
    #api.submit_order(symbol='SPY', qty=20, side='buy')
    
    
    
    
    
    
   print(df_d[df_d !=0])
   print(df_ms[df_ms !=0])
   print(df_e[df_e !=0])
   

doji = DOJI()
doji.run()
