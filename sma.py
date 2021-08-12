import alpaca_trade_api as tradeapi
import threading
import time
import datetime
import datetime as dt
import bt 
import pandas_datareader.data as web
import talib

API_Key = 'PKZMPG3T5B4KNAFUTRF3'
API_Secret = 'JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN'
API_End = 'https://paper-api.alpaca.markets'


class LongShort:
  def __init__(self): #self, thats just the way it is. Doesn't have to be self can be anything. 
    self.alpaca = tradeapi.REST(API_Key, API_Secret, API_End, 'v2')

    stockUniverse = ['AAPL', 'BA', 'SPY', 'TSLA' ]
    # Format the allStocks variable for use in the class.
    self.allStocks = []
    for stock in stockUniverse: #python for loop, doesnt matter what is used for 'stock' on the left, loop will itierate through stockUniverse  
      self.allStocks.append([stock, 0]) #.append adds an element to the end of a list, in this case it is adding all elements of stockUniverse to allStocks

    
    
    self.long = [] #list
    self.short = [] #list
    self.qShort = None #none = null type
    self.qLong = None   #none = null type
    self.adjustedQLong = None  #none = null type
    self.adjustedQShort = None #none = null type
    self.blacklist = set() #=set() creates a set
    self.longAmount = 0 # equal 0
    self.shortAmount = 0 # equal 0
    self.timeToClose = None #none = null type
    #Variables added for use later
   
  def run(self): #run method used to run the entire class on last line 
    
   start = dt.datetime(2000, 1, 1)
   end = dt.datetime(2021,12,31)
   df = web.DataReader('TSLA', 'stooq', start, end)
   # Calculate the EMA
   sma = df.rolling(20).mean()
   sma['Close'] = talib.EMA(df['Close'], timeperiod=20)
   # Define the strategy
   bt_strategy = bt.Strategy('AboveEMA', [bt.algos.SelectWhere(df > sma), bt.algos.WeighEqually(), bt.algos.Rebalance()]
    
    if(df > sma) 
      try:
        self.alpaca.submit_order(stock, qty, side, "market", "day")
        print("Market order of | " + str(qty) + " " + stock + " " + side + " | completed.")
        resp.append(True)
      except:
        print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
        resp.append(False)
    else:
      print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
      resp.append(True)     

ls = LongShort()
ls.run()















#df['SMA'] = talib.SMA(df['Close'],timeperiod = 50)
   # Calculate the EMA
   #df['EMA'] = talib.EMA(df['Close'],timeperiod = 50)
   #signal[SMA > EMA] = 1
   #signal[EMA < SMA ] = -1
   # Define the strategy
   #bt_strategy = bt.Strategy('EMA_crossover',[bt.algos.WeighTarget(signal), bt.algos.Rebalance()])
