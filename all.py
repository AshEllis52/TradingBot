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
    
class DI:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('MSFT', 'stooq', start, end)
   di = talib.PLUS_DI(df['High'], df['Low'], df['Close'])
   di1 = talib.MINUS_DI(df['High'], df['Low'], df['Close'])
   di.to_numpy()
   di1.to_numpy()
  
   if (di.values[14] > di1.values[14]):
    print('The trend indicates an uptrend, buying  stock') 
    api.submit_order(symbol='MSFT', qty=10, side='buy')
   
   elif (di1.values[14] > di.values[14]):
    print('The trend indicates a downtrend, selling  stock') 
    api.submit_order(symbol='MSFT', qty=10, side='sell')
   
   elif (di.values[14] == di1.values[14]):
    print('No trend indentified, holding position') 
  
  
    
class BB:
  def run(self):  
   start = dt.datetime(2021, 1, 1)
   end = date.today()
   df = web.DataReader('BA', 'stooq', start, end)
   upper, mid, lower = talib.BBANDS(df['Close'], nbdevup=2, nbdevdn=2, timeperiod = 20)
   todayPrice = df['Close']
   todayPrice.to_numpy()
   upper.to_numpy()
   mid.to_numpy()
   lower.to_numpy()
  
  
   if((todayPrice.values[0]) > (upper.values[19])): #if price today is above the upper band  stock is overbought 
    print("Stock is above mean value, selling position")
    api.submit_order(symbol='BA', qty=10, side='sell')
    
   elif((todayPrice.values[0]) < (lower.values[19])):
    print("Stock is below mean value, buying position") #if price today is below the lower band  stock is oversold 
    api.submit_order(symbol='BA', qty=10, side='buy')
    
   elif [((todayPrice.values[0]) < (upper.values[19])) & ((todayPrice.values[0]) > (lower.values[19]))]: 
    print("Stock is within mean value, holding position") #if price today is between upper and lower bands stock is within mean value    
       
   
rsi = RSI()
adx = ADX()
ema = EMA()
bb = BB()
di = DI()

print("Running EMA crossover strategy")
ema.run()

print("Running RSI trend strategy")
rsi.run()

print("Running ADX momentum strategy")
adx.run()

print("Running DI+/DI- crossover strategy")
di.run()

print("Running Bollinger Bands mean revision strategy")
bb.run() 
