from flask import Flask
import alpaca_trade_api as tradeapi 

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)

account = api.get_account()
print(account)


api.submit_order(symbol='AAPL', qty=1, side='buy')

print(order)

