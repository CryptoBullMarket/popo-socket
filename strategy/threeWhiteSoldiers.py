from res import id as id, values as values, constants as constants
import handler.database as db
from util import utils as utils

# check if the bear candle open between and close lower
# values of 1 is more recent than 2
def __is_higher(open_1, close_1, low_1, open_2, close_2):
    return open_1 > open_2 > low_1 and close_1 > close_2


def __small_upper_wick(price):
    if utils.__body(price[id.open], price[id.close]) > 0:
        return utils.__body(price[id.close], price[id.high]) / utils.__body(price[id.open], price[id.close]) \
            < constants.strategy_params[id.wick_percentage]
    return True

# main strategy call
def three_white_soldiers(key, price_action, time_frame):
    window_size = constants.strategy_params[id.window_size]
    # soldiers=check if the last 3 candles are soldiers
    soldiers = utils.__is_bull(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) \
            and utils.__is_bull(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
            and utils.__is_bull(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) \
            and __is_higher(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close], price_action.iloc[-1][id.low],
                           price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
            and __is_higher(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close], price_action.iloc[-2][id.low],
                           price_action.iloc[-3][id.open], price_action.iloc[-3][id.close])
    # check lower wick
    lower_wick = __small_upper_wick(price_action.iloc[-1]) \
                 and __small_upper_wick(price_action.iloc[-2]) \
                 and __small_upper_wick(price_action.iloc[-3])

    # find trend for candles from -17 to -3, extra window_size data for sma buffer
    trend = utils.__downtrend(price_action.iloc[-2*window_size - 3:-3][id.close].values, window_size)

    # check strategy
    if trend and soldiers and lower_wick:
        try:
            db.insert_strategy(key, time_frame, values.three_white_soldiers, price_action.iloc[-1][id.time])
            return {
                id.name: id.three_white_soldiers,
                id.key: key,
                id.price_action: price_action.to_dict()
            }
        except:
            print('Unable to add to database')

    return {}


