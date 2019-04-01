from util import utils
from res import id as id
import pandas as pd

def evaluate_trend(dataList):
    price_action = pd.DataFrame(dataList, columns=[id.time, id.open, id.close, id.high, id.low, id.volume])
    # most candlesticks patterns are of three candlesticks
    trend = utils.__sma_trend(price_action[100:-3][id.close].values)

    return trend