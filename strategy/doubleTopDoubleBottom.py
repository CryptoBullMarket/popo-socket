from res import id as id, values as values, constants as constants
from util import utils as utils
import handler.database as db
import pandas as pd
import numpy as np
import talib as ta


def check_double_top(price_action, indices_maxima, obv):

    isDoubleTop = False

    for i in range(0, len(indices_maxima) - 1):
        highVal = price_action[id.high].iloc[indices_maxima[i]]
        closeVal = price_action[id.close].iloc[indices_maxima[i]]
        nextHighVal = price_action[id.high].iloc[indices_maxima[i + 1]]
        minVal = price_action[id.low].iloc[indices_maxima[i]:indices_maxima[i + 1]].min()

        if nextHighVal >= closeVal and nextHighVal <= highVal and obv[indices_maxima[i]] >= obv[indices_maxima[ i +1]]:
            for j in range(indices_maxima[ i +1] + 1, len(price_action ) -1):
                if price_action[id.close].iloc[j] < minVal:
                    isDoubleTop = True
                    break
    return isDoubleTop

def check_double_bottom(price_action, indices_minima, obv):

    isDoubleBottom = False

    for i in range(0, len(indices_minima) - 1):
        lowVal = price_action[id.low].iloc[indices_minima[i]]
        closeVal = price_action[id.close].iloc[indices_minima[i]]
        nextLowVal = price_action[id.low].iloc[indices_minima[i + 1]]
        maxVal = price_action[id.high].iloc[indices_minima[i]:indices_minima[i + 1]].min()

        if nextLowVal <= closeVal and nextLowVal >= lowVal and obv[indices_minima[i]] >= obv[indices_minima[i + 1]]:
            for j in range(indices_minima[i + 1] + 1, len(price_action) - 1):
                if price_action[id.close].iloc[j] > maxVal:
                    isDoubleBottom = True
                    break
    return isDoubleBottom

def double_top_double_bottom(key, dataList, time_frame):

    price_action = pd.DataFrame(dataList, columns=[id.time, id.open, id.close, id.high, id.low, id.volume])
    if price_action.empty:
        return

    window_size = constants.strategy_params[id.window_size]
    # To determine up/down trend and the strength
    upTrend = utils.__uptrend(price_action.iloc[- 2 *window_size - 3:-3][id.close].values, window_size)
    downTrend = utils.__downtrend(price_action.iloc[- 2 *window_size - 3:-3][id.close].values, window_size)

    # ADX to determine the strength of the trend and OBV to get volume of trades placed
    adx = ta.ADX(price_action[id.high], price_action[id.low], price_action[id.close], window_size)
    obv = ta.OBV(price_action[id.close], price_action[id.volume])

    # Calculate the local maxima and minima in the window frame
    local_minima, local_maxima, indices_minima, indices_maxima = utils.__local_min_max(np.array(price_action[id.high]))

    notifier = {
        values.double_top: False,
        values.double_bottom: False
    }

    if upTrend and adx[len(adx ) -1] >= constants.strategy_params[id.trend_strength]:
        notifier[values.double_top] = check_double_top(price_action, indices_maxima, obv)
    if downTrend and adx[len(adx ) -1] >= constants.strategy_params[id.trend_strength]:
        notifier[values.double_bottom] = check_double_bottom(price_action, indices_minima, obv)

    if notifier[values.double_top]:
        try:
            db.insert_strategy(key, time_frame, values.double_top, price_action.iloc[-1][id.time])
            return {
                id.name: id.double_top,
                id.key: key,
                id.price_action: dataList
            }
        except:
            print('Unable to add to database')

    if notifier[values.double_bottom]:
        try:
            db.insert_strategy(key, time_frame, values.double_bottom, price_action.iloc[-1][id.time])
            return {
                id.name: id.double_bottom,
                id.key: key,
                id.price_action: dataList
            }
        except:
            print('Unable to add to database')

    return {}