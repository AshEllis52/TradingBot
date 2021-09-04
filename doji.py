import alpaca_trade_api as tradeapi
import datetime as dt
from datetime import date 
import pandas as pd 
import pandas_datareader.data as web
import talib
import yfinance as yfin
yfin.pdr_override()


alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)


class DOJI:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.get_data_yahoo('DELL', start, end)
   df_d = talib.CDLDOJISTAR(df['Open'], df['High'], df['Low'], df['Close'])
   df_e = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
   df_d.to_numpy()
   df_e.to_numpy()
   
   if (df_d.values[0] > 0):
    print('The patterns indicates a Dragonfly Doji on the Candlestick Graph, buying postion') 
    api.submit_order(symbol='DELL', qty=100, side='buy')
    
   elif (df_e.values[0] > 0):
    print('The patterns indicates an Bullish Engulfing Candlestick on the Candlestick Graph, buying postion') 
    api.submit_order(symbol='DELL', qty=100, side='buy') 
   
   elif (df_d.values[0] < 0):
    print('The patterns indicates a Gravestone Doji on the Candlestick Graph, selling postion') 
    api.submit_order(symbol='DELL', qty=100, side='sell')  
    
   elif (df_e.values[0] < 0):
    print('The patterns indicates a Bearish Engulfing Candlestick on the Candlestick Graph, selling postion') 
    api.submit_order(symbol='DELL', qty=100, side='sell')  
    
   elif [(df_d.values[0] == 0) & (df_e.values[0] == 0)]:
    print('The patterns indicates both a Long Legged Doji and no Engulfing Candlestick, holding position')     
    
   print('Searching historical values that do not equal zero so that we can see days where the conditions of Dojistar and engulfing are met') 
   print(df_d[df_d !=0])
   print(df_e[df_e !=0])

doji = DOJI()
doji.run()
