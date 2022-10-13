#%%
# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
#%%
# data = yf.download("BTC-USD ETH-USD",period='1m',interval='1m')

data = yf.download("ETH-USD",start="2022-07-17", end="2022-07-24",interval='2m')
#%%
data.to_csv('eth2.csv')
#%%
#Interval required 1 minute
btc_y_h = yf.download(tickers='BTC-USD', period='1y', interval='60m')
eth_y_h = yf.download(tickers='ETH-USD', period='1y', interval='60m')
gld_y_h = yf.download(tickers='GC=F', period='1y', interval='60m')
btc_y_h.to_csv("btc_y_h.csv")
eth_y_h.to_csv("eth_y_h.csv")
gld_y_h.to_csv("gld_y_h.csv")
#%%
#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=btc_y_h.index,
                open=btc_y_h['Open'],
                high=btc_y_h['High'],
                low=btc_y_h['Low'],
                close=btc_y_h['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='Uber live share price evolution',
    yaxis_title='Stock Price (USD per Shares)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()
# %%

# %%
