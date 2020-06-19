import pandas as pd
import numpy as np
import requests
import json
import datetime
import equations as eq
import joblib
from scipy.ndimage.interpolation import shift
from sklearn.ensemble import GradientBoostingClassifier


def over_under(data, eq):
    columns = data.columns
    out = []
    for i in range(1, len(data["{}".format(eq)])):
        cur_data = data["{}".format(eq)]
        if cur_data.iloc[i-1] < 80 and cur_data.iloc[i] > 80:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] > 80 and cur_data.iloc[i] < 80:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] < 20 and cur_data.iloc[i] > 20:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] > 20 and cur_data.iloc[i] < 20:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] < 45 and cur_data.iloc[i] > 45:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] > 45 and cur_data.iloc[i] < 45:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] < 65 and cur_data.iloc[i] > 65:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] > 65 and cur_data.iloc[i] < 65:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] < 10 and cur_data.iloc[i] > 10:
            out.append(np.array(data.iloc[i]))
        elif cur_data.iloc[i-1] > 90 and cur_data.iloc[i] < 90:
            out.append(np.array(data.iloc[i]))
        df = pd.DataFrame(data = out, columns = columns)
    return df


def up_down(close, window):
    out = []
    for i in range(len(close)-1):
        if close[i] > close[i+1]:
            out.append(0)
        else:
            out.append(1)
    if window == 0:
        return out
    else:
        return out[window-2:]


def start_date():
    #This are the furthest Binance will allow
    startYear = 2017
    startMonth = 8
    startDay = 17
    startDateTime = datetime.datetime(startYear, startMonth, startDay)
    return startDateTime


def pull_data(pair):
    #api constants
    base = "http://127.0.0.1:8000/coin_data/?pair={}&limit=100000".format(pair)
    response = requests.get(base).json()
    return response['results'][::-1]


lor = pull_data('LTCUSDT')
#print(lor)
binance_df = pd.DataFrame(data=lor)
binance_df = binance_df.drop(columns=['pair', 'id'], axis=1)
binance_df = binance_df.astype(float)
print(binance_df)
close = list(binance_df['closePrice'])
high = list(binance_df['highPrice'])
low = list(binance_df['lowPrice'])
volume = list(binance_df['volume'])
up_down_close = up_down(close,21)
percent_r = eq.percent_r(close,high,low,21)
percent_b = eq.percent_b(close, 21)
rsi = eq.rsi(close, 21)
rsi_over_under = eq.over_under(rsi)
closed_percent_change = eq.percent_change(close,21)
for_finished_df = binance_df.drop(columns=[
                                       'openTime',
                                       'closeTime',
                                       'openPrice',
                                       'lowPrice',
                                       'highPrice',
                                       'volume'], axis=1)

for_finished_df = for_finished_df.iloc[20:]
print(len(for_finished_df))
print(len(up_down_close))
print(len(percent_r))
print(len(percent_b))
print(len(rsi))
print(len(rsi_over_under))
print(len(closed_percent_change))
for_finished_df['percent_r'] = percent_r
for_finished_df['percent_b'] = percent_b
for_finished_df['rsi'] = rsi
for_finished_df['close_percent_change'] = closed_percent_change
final_df = for_finished_df
final_df = over_under(final_df, 'rsi')
print(len(final_df))
print(final_df)
x_data = np.array(final_df.drop(columns=['closePrice'],axis=1))[1:]
y_data = np.array(up_down(final_df['closePrice'],0))
close = final_df['closePrice'][1:-1]
y_data = shift(y_data, -1)
x_data = x_data[:-1]
y_data = y_data[:-1].astype(int)
print(len(x_data))
print(len(y_data))
print("{} last 10 close prices".format(close[-10:]))
print("{} last 10 up_down".format(y_data[-10:]))
gbc = GradientBoostingClassifier(n_estimators = 100, max_depth = 1, random_state = 0)
gbc.fit(x_data,y_data)
print(gbc.score(x_data,y_data))
joblib.dump(gbc,'./trained_models/ethusdt_model.pkl', compress=9)