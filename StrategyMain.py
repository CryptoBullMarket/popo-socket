from strategy import threeBlackCrows as tbc, doubleTopDoubleBottom as dtdb, threeWhiteSoldiers as tws, bullishAbandonedBaby as bab, eveningStar as es, morningStar as ms, shootingStar as ss
from res import id as id

def examine_strategies(key, time_frame, dataList):
    print(key, time_frame)
    strategyList = []

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
    ES = es.evening_star(key, dataList, time_frame)
    if ES:
        strategyList.append({id.evening_star: ES})
    MS = ms.morning_star(key, dataList, time_frame)
    if MS:
        strategyList.append({id.morning_star: MS})
    SS = ss.shooting_star(key, dataList, time_frame)
    if SS:
        strategyList.append({id.shooting_star: SS})
    return strategyList

if __name__ == "__main__":
    #connection.get_symbol_list()
    #examine_strategies('1h')
    print('hi')