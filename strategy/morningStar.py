from res import constants as constants, id as id, values as values
from util import utils as utils
import handler.database as db

def evening_star(key, price_action, time_frame):
    window_size = constants.strategy_params.window_size
    downtrend = utils.__downtrend(price_action.iloc[-window_size - 3:-3][id.close].values, window_size)

    morning_star = utils.__is_bull(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) \
                  and utils.__percentage_change(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) > constants.strategy_params[id.body_percentage] \
                  and utils.__is_gap_up(price_action.iloc[-1][id.open], price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
                  and utils.__percentage_change(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) < constants.strategy_params[id.small_body_percentage] \
                  and utils.__is_gap_up(price_action.iloc[-3][id.open], price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
                  and utils.__is_bear(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) \
                  and utils.__percentage_change(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) > constants.strategy_params[id.body_percentage] \
                  and utils.__threshold_down(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close], price_action.iloc[-1][id.close])

    if downtrend and morning_star:
        db.insert_strategy(key, time_frame, values.morning_star, price_action.iloc[-1][id.time])