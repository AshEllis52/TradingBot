from flask import Flask
import alpaca_trade_api as tradeapi 

class API(object):
 def __int__(self):
  self.key = 'PKZMPG3T5B4KNAFUTRF3'
  self.secret = 'JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN'
  self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
  self.api = tradeapi.REST(self.key,self.secret, self.alpaca_endpoint)
  self.symbol ='TSLA'
  self.current_order = None
  self.last_price = 1
  
  try:
   self.position = int(self.api.get_position(self.symbol).qty)
  except:
   self.position = 0 
   
 def submit_order(self, target):
  if self.current_order is not None:
   self.api.cancael_order(self,curent_order.id)
   
  delat = target - self.position 
  if delta = 0:
    return
  print(f'Processing the order for {target} shares') 
  
  if delta > 0:
   buy_quantity = delta
   if self.position < 0:
    buy_quantity = min(abs(self.position), buy_quantity)
   print(f 'Buying {buy_quantity} shares')
   self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price) 
                                        
  elif delta < 0:
    sell_quantity = abs(delta)
    if self.position > 0:
      sell_quantity = min(abs(self.postion), sell_quantity)
    print(f'Selling {sell_quantity} shares') 
    self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)                                            
  
#account = api.get_account()
#print(account.status)


if __name__ == "__main__":
 t = API()
 t.submit_order(3)
 #app.run(host='0.0.0.0', port='8080') 
