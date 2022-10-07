#%%
from cProfile import label
from importlib import reload
from LSTM_Func import *
from matplotlib.dates import DateFormatter
from statsmodels.tsa.vector_ar.vecm import coint_johansen, JohansenTestResult
from scipy.stats import linregress, zscore
import statsmodels.tsa.stattools as st
import matplotlib.dates as mpl_dates
import matplotlib.ticker as mtick
import pandas_ta as ta
import seaborn as sns
import LSTM_Func
#%%
reload(LSTM_Func)
pre = LSTM_Func.Preprocessing()
# %%
data=pd.read_csv('BTCUSDT_day.csv',index_col=False,parse_dates=['date'])
data
                                                                     
# %%
# data['close_ma60']=ta.sma(data['close'],length=60)
# data['close_ma5']=ta.sma(data['close'],length=5)
# data['close_eth_ma60']=ta.sma(data['close_eth'],length=60)
# data['close_eth_ma5']=ta.sma(data['close_eth'],length=5)
# data['close']
# %%
# data.to_csv('btc_eth_d_ma.csv',index=False)
# %%
# Set date column as index 
data1 = data.set_index('date')

# Resample to daily sum of precip
precip_daily = data1.resample('D').mean()
#%%
data.to_csv('BTCUSDT_day.csv',index=False)
#%%