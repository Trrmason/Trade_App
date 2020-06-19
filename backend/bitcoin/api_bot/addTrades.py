import joblib
import requests
import json
import datetime
import equations as eq
import numpy as np
import pandas as pd
import schedule
import time
pd.options.mode.chained_assignment = None  # default='warn'


def pull_trigger(cur_rsi, prev_rsi):
    if prev_rsi < 75 and cur_rsi > 75:
        return True
    elif prev_rsi > 75 and cur_rsi < 75:
        return True
    elif prev_rsi < 30 and cur_rsi > 30:
        return True
    elif prev_rsi > 30 and cur_rsi < 30:
        return True
    elif prev_rsi < 45 and cur_rsi > 45:
        return True
    elif prev_rsi > 45 and cur_rsi < 45:
        return True
    elif prev_rsi < 65 and cur_rsi > 65:
        return True
    elif prev_rsi > 65 and cur_rsi < 65:
        return True
    elif prev_rsi < 15 and cur_rsi > 15:
        return True
    elif prev_rsi > 85 and cur_rsi < 85:
        return True
    return False

def pull_data(pair):
    #api constants
    base = "https://bitcoin-api-prod.herokuapp.com/coin_data/?pair={}&limit=200".format(pair)
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
    valueId = df.id
    outValues = df.drop(columns=['id','closePrice', 'openTime', 'closeTime', 'lowPrice', 'highPrice', 'openPrice'], axis=1)
    return np.array(outValues), valueId

def check_valid_trade(decision, pair):
    base = "https://bitcoin-api-prod.herokuapp.com/executed_trade/?coinData__pair={}".format(pair)
    response = requests.get(base).json()['results']
    if len(response) > 0:
        prevDecision = response[0]['decision']
        if prevDecision == decision:
            return False
    return True

def post_trade(decision, valueId):
    base = "https://bitcoin-api-prod.herokuapp.com/executed_trade/"
    params = {
        'decision': decision,
        'coinData': valueId
    }
    response = requests.post(base, data=params)
    print(response.text)

def bundle(pair):
    print(pair)
    model = joblib.load('./trained_models/{}_model.pkl'.format(pair))
    data = pull_data(pair)
    values, valueId = prepare_data(data)
    rsiVals = values[:,2]
    valueId = list(valueId)
    for i in range(1,len(rsiVals)):
        tradeDecision = pull_trigger(rsiVals[i], rsiVals[i-1])
        if tradeDecision:
            predVal = np.array([values[i]])
            prediction = model.predict(predVal)[0]
            validCheck = check_valid_trade(prediction, pair)
            print(validCheck)
            if validCheck:
                print(valueId[i])
                post_trade(prediction, valueId[i])



def job():

    print(datetime.datetime.now())

    all_pairs = [
        'BTCUSDT',
        'ETHUSDT',
        'LTCUSDT',
        'TRXUSDT',
        'BATUSDT',
        'EOSUSDT',
        'ETCUSDT',
        'LINKUSDT',
        'ADAUSDT',
        'ZECUSDT',
        'DASHUSDT',
        'BNBUSDT',
        'VETUSDT'
    ]

    for pair in all_pairs:
        bundle(pair)


job()

schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(30) # wait one minute