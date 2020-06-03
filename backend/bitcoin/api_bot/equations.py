import numpy as np
from sklearn.preprocessing import MinMaxScaler


def moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas


def rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)
    rsi = rsi[n - 1::]
    return rsi


def exp_moving_average(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def moving_average_convergence(x, nslow=26, nfast=12):
    emaslow = exp_moving_average(x, nslow, type='exponential')
    emafast = exp_moving_average(x, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow


def macD(x, slow=26, fast=12):
    emaslow = exp_moving_average(x, slow)
    emafast = exp_moving_average(x, fast)
    return emaslow, emafast, emafast - emaslow


def cross_percent(values, window):
    exp = exp_moving_average(values, window)
    cross = []
    for i in range(len(exp)):
        cross.append((values[(len(values) - 1) - i] / exp[i]) * 100)
    return cross


def over_under(rsi):
    ov_un = []
    for each in rsi:
        if each > 90:
            ov_un.append(3)
        elif each > 70:
            ov_un.append(2)
        elif each < 10:
            ov_un.append(-3)
        elif each < 30:
            ov_un.append(-2)
        else:
            ov_un.append(1)
    return ov_un


def mad(x, window):
    m_a_d = []
    ma = moving_average(x, window)
    x = x.tolist()
    close = x[window - 1::]
    for i in range(len(close)):
        m_a_d.append(close[i] - ma[i])
    m_a_d = m_a_d[8::]
    return m_a_d


def standard_dev(values, window):
    std_dev = []
    for i in range(len(values)):
        start = i
        end = start + window
        current_list = values[start:end:]
        if len(current_list) != window:
            break
        std_dev.append(np.std(values[start:end:]))
    return std_dev


def bollinger_band(values, window=20):
    std = standard_dev(values, window)
    middle_band = moving_average(values, window)
    upper_band = [middle_band[i] + (std[i] * 2) for i in range(len(std))]
    lower_band = [middle_band[i] - (std[i] * 2) for i in range(len(std))]
    return middle_band, upper_band, lower_band


def percent_b(values, window=14):
    middle, upper, lower = bollinger_band(values, window)
    values = values[window - 1::]
    b = []
    for i in range(len(values)):
        close = values[i]
        b.append((((close - lower[i]) / (upper[i] - lower[i])) * 100))
    return b


def percent_r(close, high, low, window=14):
    r = []
    for i in range(len(close)):
        start = i
        end = start + window
        current_close = close[start:end:]
        current_high = high[start:end:]
        current_low = low[start:end:]
        if len(current_close) != window:
            return r
        close_c = current_close[-1]
        highest = max(current_high)
        lowest = min(current_low)
        try:
            r.append((((highest - close_c) / (highest - lowest)) * -100))
        except:
            r.append(0)
    return r


def disparity_index(close, window=14):
    index = []
    for i in range(len(close)):
        start = i
        end = start + window
        current_close = close[start:end:]
        if len(current_close) != window:
            break
        close_c = current_close[-1]
        sma = moving_average(current_close, window)
        sma = sma[-1]
        index.append((((close_c - sma) / (sma)) * 100))
    return index


def stoch_rsi(close, high, low, window):
    r = []
    for i in range(len(close)):
        start = i
        end = start + window
        current_close = close[start:end:]
        current_high = high[start:end:]
        current_low = low[start:end:]
        if len(current_close) != window:
            break
        close_c = current_close[-1]
        highest = max(current_high)
        lowest = min(current_low)
        r.append((((highest - close_c) / (highest - lowest)) * -100))
    return r


def eom(close, high, low, volume):
    # print(len(close), len(volume), len(high))
    distance_moved = []
    box_ratio = []
    emv = []
    for i in range(len(high) - 1):
        i += 1
        distance_moved.append(((high[i] + low[i]) / 2) - (high[i - 1] + low[i - 1]) / 2)
        box_ratio.append(((volume[i]) / 1000) / (high[i] - low[i]))
    for i in range(len(box_ratio)):
        emv.append((distance_moved[i] / box_ratio[i]))
    ema_eom = moving_average(emv, 14)
    ema_eom = np.insert(ema_eom, 0, 0)
    return ema_eom


def breadcrumbs(close, high, low, volume):
    r = percent_r(close, high, low)
    print("r", r)
    b = percent_b(close)
    rsi_ = rsi(close)
    eom_ = eom(close, high, low, volume)
    scaled = []
    total = []
    crumbs = []
    bread_crumbs = []
    print(rsi_)
    for i in range(len(r)):
        total.append((rsi_[i]) + r[i] + eom_[i] + (b[i] / 2))  # + r[i])
    for i in range(len(total) - 9):
        scaler = MinMaxScaler()
        temp = scaler.fit_transform(total[i:i + 10])
        scaled.append(temp)
    j = 0
    k = 0
    print("LEEEEEEEEEEEEEEEEEEEEEEEEEEN", len(scaled))
    for i in range(len(scaled)):
        if i == 0:
            crumbs.append(scaled[0])
        else:
            crumbs.append(scaled[i][-1])
    print(scaled[-1])
    bread_crumbs = exp_moving_average(scaled[-1], 3)
    # print(len(finish))
    # print(len(close) - 14)
    # print(finish)
    # print(finish)
    print(bread_crumbs)
    return scaled[-1]


def breadcrumbs2(close, high, low, volume):
    r = percent_r(close, high, low)
    b = percent_b(close)
    rsi_ = rsi(close)
    eom_ = eom(close, high, low, volume)
    print("r", r[-1], "b", b[-1], "rsi", rsi_[-1], "eom", eom_[-1])

def percent_change(val, window):
    out = [0]
    for i in range(len(val)-1):
        out.append(round(((val[i+1]-val[i])/val[i])*100,5))
    return out[0 if window == 0 else window - 1:]