from flask import Flask
import alpaca_trade_api as tradeapi 

app = Flask(__name__)
@app.route("/")#URL leading to method

account = api.getaccount()
Print(account.status)

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)



if __name__ == "__main__":
 app.run(host='0.0.0.0', port='8080') 
