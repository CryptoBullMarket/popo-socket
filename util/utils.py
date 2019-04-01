from math import floor as floor
from res import constants as constants, id as id
import talib as ta

def __uptrend(price_action, window_size):
    ema = ta.EMA(price_action, window_size)
    for i in range(1, window_size + 1):
        if price_action[-i] < ema[-i]:
            return False
    return True

def __downtrend(price_action, window_size):
    ema = ta.EMA(price_action, window_size)
    for i in range(1, window_size + 1):
        if price_action[-i] > ema[-i]:
            return False
    return True

def __sma_trend(price_action):
    sma10 = ta.SMA(price_action, 10)
    sma20 = ta.SMA(price_action, 20)
    sma50 = ta.SMA(price_action, 50)

    # make start same for all sma
    sma10 = sma10[-48:]
    sma20 = sma20[-48:]
    sma50 = sma50[-48:]

    # find the most recent value where sma10>sma20>sma30
    for i in reversed(range(len(sma10))):
        if sma10[i] > sma20[i] and sma10[i] > sma50[i] and sma20[i] > sma50[i]:
            return id.uptTend
        elif sma10[i] < sma20[i] and sma10[i] < sma50[i] and sma20[i] < sma50[i]:
            return id.downTrend
    # if none of above conditions match, trend is consolidated
    return id.consol

   
def __body(open, close):
    return abs(open-close)

def __is_bear(open, close):
    return close < open

def __is_bull(open, close):
    return close > open

def __percentage_change(open, close):
    return abs(open-close)/open*100

def __is_doji(open,close):
    return floor(abs(open-close)/open) < constants.strategy_params[id.doji_criteria]

def __local_min_max(closingPrices):
    local_maxima = []
    local_minima = []
    indices_minima = []
    indices_maxima = []
    trend = 'neutral'
    for i in range(len(closingPrices)-1):
        if closingPrices[i+1] > closingPrices[i]:
            if trend == 'decreasing':
                local_minima.append(closingPrices[i])
                indices_minima.append(i)
                trend = 'increasing'
            else:
                trend = 'increasing'
        elif closingPrices[i+1] < closingPrices[i]:
            if trend == 'increasing':
                local_maxima.append(closingPrices[i])
                indices_maxima.append(i)
                trend = 'decreasing'
            else:
                trend = 'decreasing'
        elif trend == 'neutral':
            continue
    return local_minima, local_maxima, indices_minima,indices_maxima

def percentage_change(price_action):
    return price_action[len(price_action)-1]-price_action[len(price_action)-2]/price_action[len(price_action)-2]

# price can be either open or close, depending upon where the gap is to be checked
def __is_gap_down(price, open, close):
    return price < min(open, close)

def __is_gap_up(price, open, close):
    return price > max(open, close)

def __threshold_up(open, close, price):
    return (open+close)/2 > price

def __threshold_down(open, close, price):
    return (open+close)/2 < price

def __is_wick_len(body, wick):
    if wick > 0:
        return (body/wick) <= constants.strategy_params[id.wick_percentage]
    return True

def __star_wick_len(body, wick, param):
    if body > 0:
        return wick/body >= param
    return True

def __small_lower_wick(open, close, low):
    body = __body(open, close)
    if body > 0:
        return abs(min(open, close)-low)/body < constants.strategy_params[id.wick_percentage]
    return True