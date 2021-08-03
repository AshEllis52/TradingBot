from flask import Flask
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import plotly.graph_objects as go 
import bt as bt
import alpaca_trade_api as tradeapi 
import schedule, time
#style.use('ggplot')

#app = Flask(__name__)
#@app.route("/")

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = tradeapi.REST('PKZMPG3T5B4KNAFUTRF3','JIvx2wgkPXtzGl9uy1ZSEryA5OBv9XZ37XPFwQGN', alpaca_endpoint)

def tradeweekly():
  print('Rebalancing Portfolio')
  start = dt.datetime(2000, 1, 1)
  end = dt.datetime(2021,12,31)

  df = web.DataReader('TSLA', 'stooq', start, end)

  bt_strategy = bt.Strategy('Tarde_Weekly',
                           [bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])
  
schedule.every(1).minutes.do(tradeweekly)

while True:
  schedule.run_pending()
  time.sleep(1)

  

  #bt_test = bt.Backtest(bt_strategy, df)

  #bt_res = bt.run(bt_test)

  #bt_res.plot(title="Backtest result")
  #return plt.show()

#if __name__ == "__main__":
 #app.run(host='0.0.0.0', port='8080') 
