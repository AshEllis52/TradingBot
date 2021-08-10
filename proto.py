import alpaca_trade_api as tradeapi
import threading
import time
import datetime

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
    orders = self.alpaca.list_orders(status="open") #Create variable that uses the alpaca list_orders function to get all orders of status 'open'
    for order in orders: #irierating through orders varaiable and canceling all orders which status are 'open'
      self.alpaca.cancel_order(order.id)


  def rebalance(self): #rebalance method using threading and rerank defined below 
    tRerank = threading.Thread(target=self.rerank)
    tRerank.start()
    tRerank.join()

    # Clear existing orders again.
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
      self.alpaca.cancel_order(order.id)

    print("We are taking a long position in: " + str(self.long)) #print long & short varaiables as string as postion taken 
    print("We are taking a short position in: " + str(self.short))
    # Remove positions that are no longer in the short or long list, and make a list of positions that do not need to change.  Adjust position quantities if needed.
    executed = [[], []] #executed is a list of lists 
    positions = self.alpaca.list_positions() #uses alpaca to get postions 
    self.blacklist.clear() #clear backlist varaible which is a set created above 
    for position in positions:
      if(self.long.count(position.symbol) == 0):
        # if Position is not in long list.
        if(self.short.count(position.symbol) == 0):
          # if Position not in short list either.  Clear position.
          if(position.side == "long"):
            side = "sell"
          else:
            side = "buy"
          respSO = []
          tSO = threading.Thread(target=self.submitOrder, args=[abs(int(float(position.qty))), position.symbol, side, respSO]) #uses threading to call the subOrder method defined below and then fills its paramters 
          tSO.start()
          tSO.join()
        else:
          # Position in short list.
          if(position.side == "long"):
            # Position changed from long to short.  Clear long position to prepare for short position.
            side = "sell"
            respSO = []
            tSO = threading.Thread(target=self.submitOrder, args=[int(float(position.qty)), position.symbol, side, respSO]) #uses threading to call the subOrder method defined below and then fills its paramters 
            tSO.start()
            tSO.join()
          else:
            if(abs(int(float(position.qty))) == self.qShort):
              # Position is where we want it.  Pass for now.
              pass
            else:
              # Need to adjust position amount
              diff = abs(int(float(position.qty))) - self.qShort
              if(diff > 0):
                # Too many short positions.  Buy some back to rebalance.
                side = "buy"
              else:
                # Too little short positions.  Sell some more.
                side = "sell"
              respSO = []
              tSO = threading.Thread(target=self.submitOrder, args=[abs(diff), position.symbol, side, respSO])
              tSO.start()
              tSO.join()
            executed[1].append(position.symbol)
            self.blacklist.add(position.symbol)
      else:
        # Position in long list.
        if(position.side == "short"):
          # Position changed from short to long.  Clear short position to prepare for long position.
          respSO = []
          tSO = threading.Thread(target=self.submitOrder, args=[abs(int(float(position.qty))), position.symbol, "buy", respSO])
          tSO.start()
          tSO.join()
        else:
          if(int(float(position.qty)) == self.qLong):
            # Position is where we want it.  Pass for now.
            pass
          else:
            # Need to adjust position amount.
            diff = abs(int(float(position.qty))) - self.qLong
            if(diff > 0):
              # Too many long positions.  Sell some to rebalance.
              side = "sell"
            else:
              # Too little long positions.  Buy some more.
              side = "buy"
            respSO = []
            tSO = threading.Thread(target=self.submitOrder, args=[abs(diff), position.symbol, side, respSO])
            tSO.start()
            tSO.join()
          executed[0].append(position.symbol)
          self.blacklist.add(position.symbol)

    # Send orders to all remaining stocks in the long and short list.
    respSendBOLong = []
    tSendBOLong = threading.Thread(target=self.sendBatchOrder, args=[self.qLong, self.long, "buy", respSendBOLong])
    tSendBOLong.start()
    tSendBOLong.join()
    respSendBOLong[0][0] += executed[0]
    if(len(respSendBOLong[0][1]) > 0):
      # Handle rejected/incomplete orders and determine new quantities to purchase.
      respGetTPLong = []
      tGetTPLong = threading.Thread(target=self.getTotalPrice, args=[respSendBOLong[0][0], respGetTPLong])
      tGetTPLong.start()
      tGetTPLong.join()
      if (respGetTPLong[0] > 0):
        self.adjustedQLong = self.longAmount // respGetTPLong[0]
      else:
        self.adjustedQLong = -1
    else:
      self.adjustedQLong = -1

    respSendBOShort = []
    tSendBOShort = threading.Thread(target=self.sendBatchOrder, args=[self.qShort, self.short, "sell", respSendBOShort])
    tSendBOShort.start()
    tSendBOShort.join()
    respSendBOShort[0][0] += executed[1]
    if(len(respSendBOShort[0][1]) > 0):
      # Handle rejected/incomplete orders and determine new quantities to purchase.
      respGetTPShort = []
      tGetTPShort = threading.Thread(target=self.getTotalPrice, args=[respSendBOShort[0][0], respGetTPShort])
      tGetTPShort.start()
      tGetTPShort.join()
      if(respGetTPShort[0] > 0):
        self.adjustedQShort = self.shortAmount // respGetTPShort[0]
      else:
        self.adjustedQShort = -1
    else:
      self.adjustedQShort = -1

    # Reorder stocks that didn't throw an error so that the equity quota is reached.
    if(self.adjustedQLong > -1):
      self.qLong = int(self.adjustedQLong - self.qLong)
      for stock in respSendBOLong[0][0]:
        respResendBOLong = []
        tResendBOLong = threading.Thread(target=self.submitOrder, args=[self.qLong, stock, "buy", respResendBOLong])
        tResendBOLong.start()
        tResendBOLong.join()

    if(self.adjustedQShort > -1):
      self.qShort = int(self.adjustedQShort - self.qShort)
      for stock in respSendBOShort[0][0]:
        respResendBOShort = []
        tResendBOShort = threading.Thread(target=self.submitOrder, args=[self.qShort, stock, "sell", respResendBOShort])
        tResendBOShort.start()
        tResendBOShort.join()

  # Re-rank all stocks to adjust longs and shorts.
  def rerank(self):
    tRank = threading.Thread(target=self.rank)
    tRank.start()
    tRank.join()

    # Grabs the top and bottom quarter of the sorted stock list to get the long and short lists.
    longShortAmount = len(self.allStocks) // 4
    self.long = []
    self.short = []
    for i, stockField in enumerate(self.allStocks):
      if(i < longShortAmount):
        self.short.append(stockField[0])
      elif(i > (len(self.allStocks) - 1 - longShortAmount)):
        self.long.append(stockField[0])
      else:
        continue

    # Determine amount to long/short based on total stock price of each bucket.
    equity = int(float(self.alpaca.get_account().equity))

    self.shortAmount = equity * 0.30
    self.longAmount = equity - self.shortAmount

    respGetTPLong = []
    tGetTPLong = threading.Thread(target=self.getTotalPrice, args=[self.long, respGetTPLong])
    tGetTPLong.start()
    tGetTPLong.join()

    respGetTPShort = []
    tGetTPShort = threading.Thread(target=self.getTotalPrice, args=[self.short, respGetTPShort])
    tGetTPShort.start()
    tGetTPShort.join()

    self.qLong = int(self.longAmount // respGetTPLong[0])
    self.qShort = int(self.shortAmount // respGetTPShort[0])

  # Get the total price of the array of input stocks.
  def getTotalPrice(self, stocks, resp):
    totalPrice = 0
    for stock in stocks:
      bars = self.alpaca.get_barset(stock, "minute", 1)
      totalPrice += bars[stock][0].c
    resp.append(totalPrice)

  # Submit a batch order that returns completed and uncompleted orders.
  def sendBatchOrder(self, qty, stocks, side, resp):
    executed = []
    incomplete = []
    for stock in stocks:
      if(self.blacklist.isdisjoint({stock})):
        respSO = []
        tSubmitOrder = threading.Thread(target=self.submitOrder, args=[qty, stock, side, respSO])
        tSubmitOrder.start()
        tSubmitOrder.join()
        if(not respSO[0]):
          # Stock order did not go through, add it to incomplete.
          incomplete.append(stock)
        else:
          executed.append(stock)
        respSO.clear()
    resp.append([executed, incomplete])

  # Submit an order if quantity is above 0.
  def submitOrder(self, qty, stock, side, resp):
    if(qty > 0):
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

  # Get percent changes of the stock prices over the past 10 minutes.
  def getPercentChanges(self):
    length = 10
    for i, stock in enumerate(self.allStocks):
      bars = self.alpaca.get_barset(stock[0], 'minute', length)
      self.allStocks[i][1] = (bars[stock[0]][len(bars[stock[0]]) - 1].c - bars[stock[0]][0].o) / bars[stock[0]][0].o

  # Mechanism used to rank the stocks, the basis of the Long-Short Equity Strategy.
  def rank(self):
    # Ranks all stocks by percent change over the past 10 minutes (higher is better).
    tGetPC = threading.Thread(target=self.getPercentChanges)
    tGetPC.start()
    tGetPC.join()

    # Sort the stocks in place by the percent change field (marked by pc).
    self.allStocks.sort(key=lambda x: x[1])

# Run the LongShort class
ls = LongShort()
ls.run()
