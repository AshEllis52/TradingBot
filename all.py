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
  
   if((adx.values[20]) <= 25):
    print('The trend indicates little momentum, holding position') 
    
   elif[((adx.values[20]) >= 26) or ((adx.values[20]) <= 50)]:
    print('The trend indicates moderate momentum, buying some stock') 
    api.submit_order(symbol='SPY', qty=20, side='buy')
    
   elif[((adx.values[20]) >= 51) or ((adx.values[20]) <= 75)]:
    print('The trend indicates strong momentum, buying stock') 
    api.submit_order(symbol='SPY', qty=30, side='buy') 
       
   elif((adx.values[20]) > 75):
    print('The trend indicates very strong momentum, buying a lot of stock') 
    api.submit_order(symbol='SPY', qty=50, side='buy')   
 
class EMA:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('AAPL', 'stooq', start, end)
   df_EMAS = talib.EMA(df['Close'], timeperiod = 12)
   df_EMAL = talib.EMA(df['Close'], timeperiod = 26)
   df_EMAS.to_numpy()  
   df_EMAL.to_numpy()
  
   if((df_EMAS.values[11]) > (df_EMAL.values[25])):
    print('The trend indicates a buying postion, buying stock') 
    api.submit_order(symbol='AAPL', qty=10, side='buy')
    
   elif((df_EMAL.values[25]) > (df_EMAS.values[11])):
    print('The trend indicates a selling  postion, selling stock') 
    api.submit_order(symbol='AAPL', qty=10, side='sell')
    
   elif((df_EMAL.values[25]) == (df_EMAS.values[11])):
    print('Holding stock') 
       

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
    
class BB:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
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
    
   elif [((mid.values[19]) > lower.values[24]) & ((mid.values[19] < upper.values[24]))]: 
    print("Stock is within mean value, holding position") #if SMA(mid) today is between  lower & upper 5 days ago stock is at mean value  
       
   
rsi = RSI()
adx = ADX()
ema = EMA()
bb = BB()

print("Running EMA cross over strategy")
ema.run()

print("Running RSI trend strategy")
rsi.run()

print("Running ADX momentum strategy")
adx.run()

print("Running Bollinger mean revision strategy")
bb.run() 
