import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class ADX:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('SPY', 'stooq', start, end)
   adx = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod = 21)
   adx.to_numpy()
  
   print (adx.values[45])
   print (adx.values[40])
   print (adx.values[35])
   #if((adx.values[20]) <= 25):
    #print('The trend indicates little momentum, holding position') 
    
   #elif[((adx.values[20]) >= 26) or ((adx.values[20]) <= 50)]:
    #print('The trend indicates moderate momentum, buying some stock') 
    #api.submit_order(symbol='SPY', qty=20, side='buy')
    
   #elif[((adx.values[20]) >= 51) or ((adx.values[20]) <= 75)]:
    #print('The trend indicates strong momentum, buying stock') 
    #api.submit_order(symbol='SPY', qty=30, side='buy') 
       
   #elif((adx.values[20]) > 75):
    #print('The trend indicates very strong momentum, buying a lot of stock') 
    #api.submit_order(symbol='SPY', qty=50, side='buy')   
    
adx = ADX()
adx.run()
