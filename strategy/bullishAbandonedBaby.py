from res import constants as constants, id as id, values as values
from util import utils as utils
import handler.database as db
import pandas as pd

def bullish_abandoned_baby(key, dataList, time_frame):

    price_action = pd.DataFrame(dataList, columns=[id.time, id.open, id.close, id.high, id.low, id.volume])
    if price_action.empty:
        return

    window_size = constants.strategy_params[id.window_size]
    downTrend = utils.__downtrend(price_action.iloc[-2*window_size - 3:-3][id.close].values,window_size)

    abandonedBaby = utils.__is_bull(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) \
                    and utils.__percentage_change(price_action.iloc[-1][id.open], price_action.iloc[-1][id.close]) > constants.strategy_params[id.body_percentage] \
                    and price_action.iloc[-1][id.low] > price_action.iloc[-2][id.high] \
                    and utils.__is_doji(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) \
                    and price_action.iloc[-3][id.high] > price_action.iloc[-2][id.low] \
                    and utils.__is_bear(price_action.iloc[-3][id.open], price_action.iloc[-3][id.close]) \
                    and utils.__percentage_change(price_action.iloc[-2][id.open], price_action.iloc[-2][id.close]) > constants.strategy_params[id.body_percentage]

    if downTrend and abandonedBaby:
        try:
            #db.insert_strategy(key, time_frame, values.bullish_abandoned_baby, price_action.iloc[-1][id.time])
            return {
                id.name: id.bullish_abandoned_baby,
                id.key: key
            }
        except:
            print('Unable to add to database')
            return {}