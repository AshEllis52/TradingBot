import alpaca_api as tradeapi
import threading
import time
import datetime 

API_Key = 'PKZMPG3T5B4KNAFUTRF3'
API_Secret = 'JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN'
API_End = 'https://paper-api.alpaca.markets'

class LongShort:
  def __init__(self):
    self.alpaca = tardeapi.REST(API_Key, API_Secret, API_End, 'v2')
    
    stockList = ['TSLA', 'BA', 'AAPL', 'SPY']
    self.allStocks = []
    for stock in stockList:
      self.allStocks.append([stock, 0])
      
    self.long = []
    self.short = []
    self.qShort = None
    self.qLong = None
    self.adjustedQLong = None
    self.adjustedQShort = None
    self.backlist = set()
    self.longAmount = 0
    self.shortAmount = 0
    self.timeToClose = none
   
  def run(self):
    #Cancel any exisiting orders so they dont impact new orders
    orders = self.alpaca.list_orders(status='open')
    for order in Orders:
      self.alpaca.cancael_order(order.id)
    #Wait for market open 
    print ('Waiting for Market to open')
    tAMO = threading.Thread(target=self.awaitMarketOpen)
    tAMO.start()
    tAMO.join()
    print('Market Open')
    
    #Rebalance the portfolio every minute
    while True:
      
      #figure out when the market will close so we can sell beforehand
      clock = self.alpaca.get_clock()
      closingTime = clock.next_close.replace
      (tzinfo=datetime.timezone.utc).timestamp()
      currTime = clock.timestamp.replace
      (tzinfo=datetime.timezone.utc).timestamp()
      self.timeToClose = closingTime - currTime
      
      if (self.timeToClose < (60 * 15)):
        #close all positions 15 mins before market close
        print('Market closing, Closing all trades')
        
        positions = self.alpaca.list_positions()
        for position in positions:
          if(positions.side == 'long'):
            orderSide = 'sell'
            else:
              orderside = 'buy'
            qty = abs(int(float(positions.qty)))
            respSO = []
            tSubmitOrder = threading.Thread
            (target=self.submitOrder(qty, position.symbol, orderSide, respSO))
            tSubmitOrder.start()
            tSubmitOrder.join()
            
        #Run script again after market close for next trading day
        print('Sleeping until market close')
        time.sleep(60 * 15)
       else:
        tRebalance = threading.Thread
        (target=self.rebalance)
        tRebalance.start()
        tRebalance.join()
        time.sleep(60)

  def awaitMarketOpen(self):
    isOpen = self.alpaca.get_clock()
    while(not isOpen):
      clock = self.alpaca.get_clock()
      openingTime = clock.next_open.replace
      (tzinfo=datetime.timezone.utc).timestamp()
      currTime = clock.timestamp.replace
      (tzinfo=datetime.timezone.utc).timestamp()
      timeToOpen = int((openingTime - currTime) / 60)
      print(str(timeToOpen) + 'minutes till market open')
      time.sleep(60)
      isOpen = self.alpaca.get_clock().is_open
      
  def rebalance(self):
    tRerank = threading.Thread(target=self.rerank)
    tRerank.start()
    tRerank.join()
    
    #clear orders again
    orders = self.alpaca.list_orders(status='open')
    for order in orders:
      self.alpaca.cancel_order(order.id)
      
    print('We are taking a long position in:' + str(self.long))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
