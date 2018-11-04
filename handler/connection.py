from res import constants as constants, id as id
import pandas as pd
import requests


def get_price_action(key, time_frame):
    # data is in sorted in ascending order by time
    data = requests.get(constants.url[id.price_action].format(time_frame, key.upper()),
                        params=constants.url_params[id.price_action]).json()

    # Converting it into a Dataframe
    data = pd.DataFrame(data)

    try:
        data.columns = [id.time, id.open, id.close, id.high, id.low, id.volume]
    except:
        return pd.DataFrame()
    # filter data as needed
    return data

def get_symbol_list():
    data = requests.get(constants.url[id.symbols]).json()

    print(data)