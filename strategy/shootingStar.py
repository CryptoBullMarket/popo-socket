from res import constants as constants, id as id, values as values
from util import utils as utils
import handler.database as db
import pandas as pd

def shooting_star(key, dataList, time_frame):
    price_action = pd.DataFrame(dataList, columns=[id.time, id.open, id.close, id.high, id.low, id.volume])
    if price_action.empty:
        return

    window_size = constants.strategy_params[id.window_size]
    uptrend = utils.__uptrend(price_action.iloc[-window_size - 1:-1][id.close].values, window_size)

    shooting_star = utils.__is_wick_len(utils.__body(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]),
                    utils.__body(min(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]), price_action.iloc[-1][id.low])) \
                    and utils.__small_lower_wick(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close], price_action.iloc[-1][id.low]) \
                    and utils.__percentage_change(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) < \
                    constants.strategy_params[id.small_body_percentage]

    if uptrend and shooting_star:
        try:
            #db.insert_strategy(key, time_frame, values.shooting_star, price_action.iloc[-1][id.time])
            return {
                id.name: id.shooting_star,
                id.key: key
            }
        except:
            print('Unable to add to database')
            return {}