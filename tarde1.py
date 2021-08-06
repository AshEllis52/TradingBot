import alpaca_trade_api as tradeapi
import threading
import time
import datetime

API_Key = 'PKZMPG3T5B4KNAFUTRF3'
API_Secret = 'JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN'
API_End = 'https://paper-api.alpaca.markets'


class LongShort:
  def __init__(self):
    self.alpaca = tradeapi.REST(API_Key, API_Secret, API_End, 'v2')

    stockUniverse = ['AAPL', 'BA', 'SPY', 'TSLA' ]
    # Format the allStocks variable for use in the class.
    self.allStocks = []
    for stock in stockUniverse:
      self.allStocks.append([stock, 0])

    self.long = []
    self.short = []
    self.qShort = None
    self.qLong = None
    self.adjustedQLong = None
    self.adjustedQShort = None
    self.blacklist = set()
    self.longAmount = 0
    self.shortAmount = 0
    self.timeToClose = None

 

  def rebalance(self):
    tRerank = threading.Thread(target=self.rerank)
    tRerank.start()
    tRerank.join()

    # Clear existing orders again.
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
      self.alpaca.cancel_order(order.id)

    print("We are taking a long position in: " + str(self.long))
    print("We are taking a short position in: " + str(self.short))
    # Remove positions that are no longer in the short or long list, and make a list of positions that do not need to change.  Adjust position quantities if needed.
    executed = [[], []]
    positions = self.alpaca.list_positions()
    self.blacklist.clear()
    for position in positions:
      if(self.long.count(position.symbol) == 0):
        # Position is not in long list.
        if(self.short.count(position.symbol) == 0):
          # Position not in short list either.  Clear position.
          if(position.side == "long"):
            side = "sell"
          else:
            side = "buy"
          respSO = []
          tSO = threading.Thread(target=self.submitOrder, args=[abs(int(float(position.qty))), position.symbol, side, respSO])
          tSO.start()
          tSO.join()
        else:
          # Position in short list.
          if(position.side == "long"):
            # Position changed from long to short.  Clear long position to prepare for short position.
            side = "sell"
            respSO = []
            tSO = threading.Thread(target=self.submitOrder, args=[int(float(position.qty)), position.symbol, side, respSO])
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

   # Re-rank all stocks to adjust longs and shorts.
  def rerank(self):
    tRank = threading.Thread(target=self.rank)
    tRank.start()
    tRank.join()


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
