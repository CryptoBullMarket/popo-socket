from strategy import threeBlackCrows as tbc, doubleTopDoubleBottom as dtdb, threeWhiteSoldiers as tws, bullishAbandonedBaby as bab
from res import id as id
import pandas as pd


def examine_strategies(key, time_frame, data):
    print(key, time_frame)
    dataList = []
    strategyList = []
    for x in data:
        for k, v in x.items():
            dataList.append(v)

    TBC = tbc.three_black_crows(key, dataList, time_frame)
    if TBC:
        strategyList.append({id.three_black_crow: TBC})
    DTDB = dtdb.double_top_double_bottom(key, dataList, time_frame)
    if DTDB:
        if DTDB[id.name] == id.double_top:
            strategyList.append({id.double_top:DTDB})
        else:
            strategyList.append({id.double_bottom:DTDB})
    TWS = tws.three_white_soldiers(key, dataList, time_frame)
    if TWS:
        strategyList.append({id.three_white_soldiers: TWS})
    BAB = bab.bullish_abandoned_baby(key, dataList, time_frame)
    if BAB:
        strategyList.append({id.bullish_abandoned_baby: BAB})
    return strategyList

if __name__ == "__main__":
    #connection.get_symbol_list()
    examine_strategies('1h')