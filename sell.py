from flask import Flask
import alpaca_trade_api as tradeapi 
import schedule, time

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)

#account = api.get_account()
#print(account)


#print(order)

def sell_aapl(): 
  print('Selling Apple')
  order = api.submit_order(symbol='AAPL', qty=537, side='sell')
  print(order)
  
schedule.every(1).minute.do(sell_aapl)

while True:
  schedule.run_pending()
  time.sleep(1)
