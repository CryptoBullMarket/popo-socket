from res import constants as constants, id as id, values as values
from util import utils as utils
import handler.database as db

def shooting_star(key, price_action, time_frame):
    window_size = constants.strategy_params.window_size
    uptrend = utils.__uptrend(price_action.iloc[-window_size - 1:-1][id.close].values, window_size)

    shooting_star = utils.__is_wick_len(utils.__body(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]),
                    utils.__body(min(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]), price_action.iloc[-1][id.low])) \
                    and utils.__small_lower_wick(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close], price_action.iloc[-1][id.low]) \
                    and utils.__percentage_change(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) < \
                    constants.strategy_params[id.small_body_percentage]

    if uptrend and shooting_star:
        db.insert_strategy(key, time_frame, values.shooting_star, price_action.iloc[-1][id.time])