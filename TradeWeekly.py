from flask import Flask
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import plotly.graph_objects as go 
import bt as bt
style.use('ggplot')

app = Flask(__name__)
@app.route("/")

def tradeweekly():
  print('Rebalancing Portfolio')
  start = dt.datetime(2000, 1, 1)
  end = dt.datetime(2021,12,31)

  df = web.DataReader('TSLA', 'stooq', start, end)

  bt_strategy = bt.Strategy('Tarde_Weekly',
                          [bt.algos.RunWeekly(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])

  bt_test = bt.Backtest(bt_strategy, df)

  bt_res = bt.run(bt_test)

  bt_res.plot(title="Backtest result")
  return plt.show()

if __name__ == "__main__":
 app.run(host='0.0.0.0', port='8080') 
