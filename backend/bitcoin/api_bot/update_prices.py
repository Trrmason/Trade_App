import requests
import json
import datetime
import time
import numpy as np
import schedule

#Pull Data from binance
def pull_data(pair, limit):
    base = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol':pair,
        'interval': '1h',
        'limit' : limit
    }
    response = requests.get(base, params).json()
    return np.array(response)[:,0:7]

def last_ids(pair, limit):
    base = "http://127.0.0.1:8000/coin_data/?pair={}&limit={}".format(pair,limit)
    response = requests.get(base).json()
    return response

#Post Data to API
def post_data(pair, data):
    base = "http://127.0.0.1:8000/coin_data/"
    for each in data:
        params = {
            'pair': pair,
            'openTime': each[0],
            'openPrice' : each[1],
            'highPrice': each[2],
            'lowPrice' : each[3],
            'closePrice': each[4],
            'volume' : each[5],
            'closeTime' : each[6]
        }
        response = requests.post(base, data = params)
        print(response)

def put_data(pair, limit):
    id_response = last_ids(pair,limit)['results']
    ids = [each['id'] for each in id_response]
    closeTimes = [each['closeTime'] for each in id_response]
    data = pull_data(pair, limit)
    combined = {}

    #Search for ID's
    for i in range(limit):
        cur_closeTime = closeTimes[i]
        cur_id = ids[i]
        for j in range(limit):
            data_closeTime = data[j][-1]
            if cur_closeTime == int(data_closeTime):
                combined[cur_id] = np.array(data[j])
                break

    #Take the dict and call the api endpoint , put
    for key, value in combined.items():
        base = "http://127.0.0.1:8000/coin_data/{}/".format(key)
        params = {
            'pair': pair,
            'openTime': value[0],
            'openPrice' : value[1],
            'highPrice': value[2],
            'lowPrice' : value[3],
            'closePrice': value[4],
            'volume' : value[5],
            'closeTime' : value[6]
        }
        response = requests.put(base, data = params)
        print(response)




#All Pairs
def job():
    print(datetime.datetime.now())

    all_pairs = [
        'BTCUSDT',
        'ETHBTC',
        'LINKBTC',
        'TRXBTC',
        'XRPBTC',
        'BATBTC'
    ]

    for pair in all_pairs:
        data = pull_data(pair, 10)
        post_data(pair, data)
        put_data(pair,10)
    
job()

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(30) # wait one minute