from res import id as id, values as values, constants as constants
import handler.database as db
from util import utils as utils
import pandas as pd

# check if the bear candle open between and close lower
# values of 1 is more recent than 2
def __is_lower(open_1, close_1, open_2, close_2, low_2):
    return open_2 > open_1 > low_2 and close_1 < close_2


def __small_lower_wick(price):
    if utils.__body(price[id.open], price[id.close]) > 0:
        return utils.__body(price[id.close], price[id.high]) / utils.__body(price[id.open], price[id.close]) \
            < constants.strategy_params[id.wick_percentage]
    return True


# main strategy call
def three_black_crows(key, dataList, time_frame):

    price_action = pd.DataFrame(dataList, columns=[id.time, id.open, id.close, id.high, id.low, id.volume])
    if price_action.empty:
        return

    window_size = constants.strategy_params[id.window_size]
    # crows=check if the last 3 candles are crows
    crows = utils.__is_bear(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) \
            and utils.__is_bear(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
            and utils.__is_bear(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) \
            and __is_lower(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close],
                           price_action.iloc[-2][id.open], price_action.iloc[-2][id.close], price_action.iloc[-2][id.low]) \
            and __is_lower(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close],
                           price_action.iloc[-3][id.open], price_action.iloc[-3][id.close], price_action.iloc[-3][id.low])
    # check lower wick
    lower_wick = __small_lower_wick(price_action.iloc[-1]) \
                 and __small_lower_wick(price_action.iloc[-2]) \
                 and __small_lower_wick(price_action.iloc[-3])

    # find trend for candles from -17 to -3, extra window_size data for sma buffer
    trend = utils.__uptrend(price_action.iloc[-2*window_size - 3:-3][id.close].values, window_size)

    # check strategy
    if trend and crows and lower_wick:
        try:
            db.insert_strategy(key, time_frame, values.three_black_crow, price_action.iloc[-1][id.time])
            return {
                id.name: id.three_black_crow,
                id.key: key,
                id.price_action: dataList
            }
        except:
            print('Unable to add to database')
            return {}


