import joblib
import requests
import json
import datetime
import equations as eq
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def pull_trigger(cur_rsi, prev_rsi):
    if prev_rsi < 80 and cur_rsi > 80:
        return True
    elif prev_rsi > 80 and cur_rsi < 80:
        return True
    elif prev_rsi < 20 and cur_rsi > 20:
        return True
    elif prev_rsi > 20 and cur_rsi < 20:
        return True
    elif prev_rsi < 45 and cur_rsi > 45:
        return True
    elif prev_rsi > 45 and cur_rsi < 45:
        return True
    elif prev_rsi < 65 and cur_rsi > 65:
        return True
    elif prev_rsi > 65 and cur_rsi < 65:
        return True
    elif prev_rsi < 10 and cur_rsi > 10:
        return True
    elif prev_rsi > 90 and cur_rsi < 90:
        return True
    return False

def pull_data(pair):
    #api constants
    base = "http://127.0.0.1:8000/coin_data/?pair={}&limit=100".format(pair)
    response = requests.get(base).json()
    return response['results'][::-1]

def calculations(df):
    #Prepare data for calculations
    close = list(df['closePrice'])
    high = list(df['highPrice'])
    low = list(df['lowPrice'])
    percent_r = eq.percent_r(close,high,low,21)
    percent_b = eq.percent_b(close, 21)
    rsi = eq.rsi(close, 21)
    closed_percent_change = eq.percent_change(close,21)
    #resize df for new data
    df = df.iloc[20:]
    #Add new data to df
    df['percentR'] = percent_r
    df['percentB'] = percent_b
    df['rsi'] = rsi
    df['closedPercentChange'] = closed_percent_change
    #return epoch to be evaulated
    return df

def prepare_data(data):
    df = pd.DataFrame(data=data)
    df = df.drop(columns=['pair', 'volume'], axis=1)
    df.openPrice = df.openPrice.astype(float)
    df.closePrice = df.closePrice.astype(float)
    df.highPrice = df.highPrice.astype(float)
    df.lowPrice = df.lowPrice.astype(float)
    df = calculations(df)
    valueId = df.id.iloc[-2]
    outValues = df.drop(columns=['id','closePrice', 'openTime', 'closeTime', 'lowPrice', 'highPrice', 'openPrice'], axis=1)
    return np.array(outValues.iloc[-3:-1]), valueId

def post_trade(decision, valueId):
    base = "http://127.0.0.1:8000/executed_trade/"
    params = {
        'decision': decision,
        'coinData': valueId
    }
    response = requests.post(base, data=params)
    print(response.text)

def bundle(pair):
    model = joblib.load('./trained_models/{}_model.pkl'.format(pair.lower()))
    data = pull_data(pair)
    values, valueId = prepare_data(data)
    rsiVals = values[:,2]
    tradeDecision = pull_trigger(rsiVals[0], rsiVals[-1])
    print(rsiVals)
    print(tradeDecision)
    if tradeDecision:
        predVal = np.array([values[-1]])
        prediction = model.predict(predVal)[0]
        post_trade(prediction, valueId)


all_pairs = [
    'BTCUSDT',
    'ETHBTC',
    'LINKBTC',
    'TRXBTC',
    'XRPBTC',
    'BATBTC'
]
for pair in all_pairs:  
    bundle(pair)