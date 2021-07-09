from flask import Flask
import alpaca_trade_api as tradeapi 

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)

#app = Flask(__name__)
#@app.route("/")#URL leading to method

account = api.get_account()
print(account)


if __name__ == "__main__":
 app.run(host='0.0.0.0', port='8080') 
