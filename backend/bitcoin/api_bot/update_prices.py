import requests
import json
import datetime
import time
import numpy as np

# #Pull Data from binance
def pull_data(pair):
    base = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol':pair,
        'interval': '1h',
        'limit' : '150'
    }
    response = requests.get(base, params).json()
    print(response)
    return np.array(response)[:,0:7]

#Post Data to API
def post_data(pair, data):
    base = "https://bitcoin-api-prod.herokuapp.com/coin_data/"
    for each in data:
        params = {
            'pair': pair,
            'tradePair': pair,
            'openTime': each[0],
            'openPrice' : each[1],
            'highPrice': each[2],
            'lowPrice' : each[3],
            'closePrice': each[4],
            'volume' : each[5],
            'closeTime' : each[6]
        }
        requests.post(base, data = params)
        print(each)


#All Pairs
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

# for pair in all_pairs:
#     data = pull_data(pair)
#     post_data(pair, data)

#print(pull_data('BTCUSDT'))

def start_date():
    #This are the furthest Binance will allow
    startYear = 2017
    startMonth = 8
    startDay = 17
    startDateTime = datetime.datetime(startYear, startMonth, startDay)
    return startDateTime


# def pull_data(pair):
#     #api constants
#     base = "https://api.binance.com"
#     oldTrades = "/api/v3/klines"
    
#     #startDate
#     startDateTime = start_date()
    
#     #list of responses
#     lor = []
    
#     for i in range(100):
#         if i != 0:
#             startDateTime += datetime.timedelta(hours=1000)
            
#         #convert starttime to int milli
#         startTime = int((startDateTime.timestamp())*1000.0)
#         #params
#         params = {'symbol':pair,
#                   'interval':'1h',
#                   'startTime':startTime,
#                   'limit':'1000'}
#         response = requests.get(base+oldTrades, params).json()
#         lor.append(response)
#     return lor


# lor = pull_data('BTCUSDT')
# forDf = []
# for kline_set in lor:
#     for each in kline_set:
#         forDf.append(np.array(each))
# updateForDf = np.array(forDf)[:,0:7]

def job():
    for pair in all_pairs:
        lor = pull_data(pair)
        #updatedForDf = np.array(forDf)[:,0:7]
        post_data(pair, lor)
job()
