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
import seaborn as sns
import LSTM_Func
#%%
reload(LSTM_Func)
pre = LSTM_Func.Preprocessing()
# %%
data1 = pd.read_csv("btc_eth_to_d.csv")
# data2 = pd.read_csv("btc_eth_1.csv",parse_dates=['date'])
# data1=data1.drop_duplicates()
# data15 = pd.read_csv("btc_eth_15.csv")
# data30 = pd.read_csv("btc_eth_30.csv")
# data1.dropna(inplace=True)
# data1=data1.sort_values(data1['date'])
#%%
# data1 = data1[-64888:].reset_index()
#%%
# data1.to_csv("btc_eth_to_d.csv",index=False)
# %%
a=np.log(data1["close"])
b=np.log(data1["close_eth"])
x = pd.DataFrame(np.log(data1["close"]))
y = pd.DataFrame(np.log(data1["close_eth"]))
df= pd.DataFrame({'x':data1['close'],'y':data1['close_eth']})
df2=pd.DataFrame({'x':x["close"], 'y':y["close_eth"]})
# %%
# spread = x - y
# %%
# st.coint(data1['per_close_btc'], data1['per_close_eth'])
(a/b).plot(figsize=(15,7)) 
plt.axhline((a/b).mean(), color='red', linestyle='--') 
plt.xlabel('Time')
plt.legend(['Price Ratio', 'Mean'])
plt.show()
#%%
st.coint(a, b)
# The null hypothesis of r=0 means no cointegration relationship; r<=1 means up to one cointegration relationship, and so on.
# x = getx() # dataframe of n series for cointegration analysis
# jres = coint_johansen(df, det_order=0, k_ar_diff=1)
# print(jres.lr1)                 # dim = (n,) Trace statistic
# print(jres.cvt)                 # dim = (n,3) critical value table (90%, 95%, 99%)
# print(jres.evec)                # dim = (n, n), columnwise eigen-vectors

# v1 = jres.evec[:, 0]
# v2 = jres.evec[:, 1]
#%%
ratios = a / b
ratios.plot(figsize=(15,7))
plt.plot()
plt.axhline(ratios.mean())
plt.legend(['Ratio'])

plt.show()
def zscore(series):
    return (series - series.mean()) / np.std(series)
#%%

plt.plot(data1['date'][-200:],zscore(ratios[-200:]))
ax=plt.gca()
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.gcf().autofmt_xdate()
ax.xaxis.set_major_locator(mtick.AutoLocator())
plt.axhline(zscore(ratios).mean(),color='black')
plt.axhline(1.0, color='red',linestyle='--')
plt.axhline(-1.0, color='green',linestyle='--')
plt.show()

#%%
a.corr(b)

#%%
# data2=data1.rolling(window=60).mean()
data1['close_btc60d'] = data1['close'].rolling(60).mean()
data1['close_btc5d']  = data1['close'].rolling(5).mean()
#%%

ratios_mavg5 = ratios.rolling(window=5,
                               center=False).mean()

ratios_mavg60 = ratios.rolling(window=60,
                               center=False).mean()

std_60 = ratios.rolling(window=60,
                        center=False).std()

zscore_60_5 = (ratios_mavg5 - ratios_mavg60)/std_60
plt.figure(figsize=(15,7))
plt.plot( ratios.values[-200:])
plt.plot( ratios_mavg5.values[-200:])
plt.plot( ratios_mavg60.values[-200:])

plt.legend(['Ratio','5d Ratio MA', '60d Ratio MA'])

plt.ylabel('Ratio')
plt.show()
# data2.dropna(inplace=True)
#%%
# Take a rolling 60 day standard deviation
std_60 = ratios.rolling(window=60,center=False).std()
std_60.name = 'std 60d'

# Compute the z score for each day
zscore_60_5 = (ratios_mavg5 - ratios_mavg60)/std_60
zscore_60_5.name = 'z-score'

plt.figure(figsize=(15,7))
zscore_60_5[-200:].plot()
plt.axhline(0, color='black')
plt.axhline(1.0, color='red', linestyle='--')
plt.axhline(-1.0, color='green', linestyle='--')
plt.legend(['Rolling Ratio z-Score', 'Mean', '+1', '-1'])
plt.show()
#%%
# ratios.plot()


#%%
# Plot the ratios and buy and sell signals from z score
plt.figure(figsize=(15,7))

plt.plot(ratios[-200:])
buy = ratios.copy()
sell = ratios.copy()
buy[zscore_60_5>-1] = 0
sell[zscore_60_5<1] = 0
buy[-200:].plot(color='g', linestyle='None', marker='^')
sell[-200:].plot(color='r', linestyle='None', marker='*')
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,ratios[-200:].min(),ratios[-200:].max()))
plt.legend(['Ratio', 'Buy Signal', 'Sell Signal'])
plt.show()

#%%
result = linregress(df2['x'], df2['y']) 
result

#%%
spread = df2['x'] - result.slope * df2['y']
#%%
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec

# Create 2x2 sub plots
gs = gridspec.GridSpec(3, 1)
pl.figure(figsize=(10,10))
ax = pl.subplot(gs[0, :])
pl.plot(df2['x'])



ax = pl.subplot(gs[1, :])
pl.plot(df2['y'])


ax = pl.subplot(gs[2, :])
pl.plot(spread)

pl.show()
#%%

pre.fuller_kpss_test(spread)
#%%


zsc_res=zscore(spread)
pl.plot(zsc_res)


# %%
y2 = y * 1.32
# Plotting the two lines of BTC and ETH.
plt.plot(x, label="BTC")
plt.plot(y2, label="ETH")
plt.legend()
plt.show()
# %%
plt.subplots(figsize=(10, 6))
ax = plt.gca()
plt.plot(spread - 2.5)
plt.gcf().autofmt_xdate()
ax.xaxis.set_major_locator(mtick.AutoLocator())
# ((data1["close"][299673])-(data1["close"][299672]))/data1["close"][299672]
# need *100
# data1['Datetime'] = pd.to_datetime(data1['Datetime'])
# data15['Datetime'] = pd.to_datetime(data15['Datetime'])
# data30['Datetime'] = pd.to_datetime(data30['Datetime'])
# # %%
# data1.to_csv('btc_eth_1.csv',index=False)
# data15.to_csv('btc_eth_15.csv',index=False)
# data30.to_csv('btc_eth_30.csv',index=False)
# data1['per_close_btc']=data1['close'].pct_change()
# data1['per_close_eth']=data1['close_eth'].pct_change()
# data1=data1.dropna()
# %%

# plt.plot(np.log(data1["close"])-np.log(data1["lose_eth"]),label='Spread')
ax = plt.gca()
plt.plot((data1["per_close_btc"][-50:]) * 100, label="BTC")
plt.plot((data1["per_close_eth"][-50:]) * 100, label="ETH")
plt.legend()
# ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))
plt.axhline(y=0, linestyle="--", color='k')
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
# dataplot = sns.heatmap(eth.corr(), cmap="RdYlGn", annot=True)
# %%
plt.subplots(figsize=(10, 6))
ax = plt.gca()
plt.style.use('seaborn')
plt.plot(data1["date"][-10000:], (data1["per_close_btc"][-10000:]) * 100, label="BTC")
plt.plot(data1["date"][-10000:], (data1["per_close_eth"][-10000:]) * 100, label="ETH")
# ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
# mdates.MonthLocater(interval=2)
# ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
# date_format=mpl_dates.DateFormatter("%b, %d %Y")
# Get the access of current figure
plt.ylabel('Percent Change of Closed Price', size=14)
plt.title('Chart of the last 75 data\n1 minutes data', size=18)
plt.axhline(y=0, linestyle="--", color='k')
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.gcf().autofmt_xdate()
ax.xaxis.set_major_locator(mtick.AutoLocator())
# ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
# ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# Get the access of current figure
# ax.xaxis.set_major_formatter('%Y-%m-%d %H:%M')

plt.legend()
# Define the date format
# date_form = DateFormatter("%m-%d")
# plt.xaxis.set_major_formatter(date_form)
plt.show()

# %%
from sklearn.metrics import r2_score

R2 = r2_score(data1["per_close_eth"], data1["per_close_btc"])
# mix=mix.drop(columns=mix.columns[0])
# %%
# from statsmodels.tsa.stattools import adfuller
pre.fuller_kpss_test(data1["close"])
# %%


# %%
plt.figure(figsize=(12, 8))
dataplot = sns.heatmap(data1.corr(), cmap="RdYlGn", annot=True)
# %%
plt.figure(figsize=(12, 8))
dataplot = sns.heatmap(data15.corr(), cmap="RdYlGn", annot=True)
# %%
plt.figure(figsize=(12, 8))
dataplot = sns.heatmap(data30.corr(), cmap="RdYlGn", annot=True)
# %%

import nltk

nltk.__file__
# %%


# %%
i = 0
for index, row in data1.iterrows():
    if (row["per_close_btc"] > 0) and (row["per_close_eth"] < 0) or (row["per_close_btc"] < 0) and (
            row["per_close_eth"] > 0):
        i += 1
print(i)
# %%
j = 0
for index, row in mix.iterrows():
    if row["per_close"] == row["per_close_right"]:
        j += 1
print(j)
# %%
plt.scatter(data1["date"], data1["tradecount_eth"])
# %%
