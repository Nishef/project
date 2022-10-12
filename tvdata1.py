#%%
from tvDatafeed import TvDatafeed, Interval
import datetime
import logging
import pandas as pd
#%%
logging.basicConfig(level=logging.DEBUG)
#%%
username = 'nishef'
password = 'nima@1379'

tv = TvDatafeed(username, password)


#%%
data_btc=tv.get_hist('BTCUSD','Binance',Interval.in_1_minute,n_bars=1000000)
data_eth=tv.get_hist("ETHUSD","binance",Interval.in_1_minute,n_bars=1000000)
# %%
data_btc.to_csv('btc_1.csv',index=True)
data_eth.to_csv('eth_1.csv',index=True)
# %%
