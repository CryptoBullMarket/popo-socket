from res import id as id, constants as constants
from tempClient import main as tempClientPush
from StrategyMain import examine_strategies
from time import sleep
import threading
import websocket
import json

channelKeys = {}
candleData = {}
strategyList = {}

def removeStaleData(chanId):
    no_removed = len(candleData[chanId]) - constants.history[id.history_size]
    for i in range(0, no_removed):
        del candleData[chanId][i]

def on_message(ws, message):
    print(message)
    newMessage = json.loads(message)

    if id.serverId in newMessage:
        print('Ignore')

    elif id.chanId in newMessage:
        if newMessage[id.chanId] not in channelKeys:
            channelKeys[newMessage[id.chanId]] = newMessage[id.key]

    else:
        chanId = newMessage[0]
        data = newMessage[1]
        if data and type(data) == list:
            if type(data[0]) == list:
                data = sorted(data, key=lambda k: k[0])
            if chanId not in candleData:
                candleData[chanId] = []
                for value in data:
                    x = {}
                    if type(data[0]) == list:
                        x[value[0]] = value
                        candleData[chanId].append(x)
                        removeStaleData(chanId)
                    else:
                        x[value] = data
                        candleData[chanId].append(x)
                        removeStaleData(chanId)
            else:
                for value in data:
                    x = {}
                    if type(data[0]) == list:
                        if value[0] > list(candleData[chanId][len(candleData[chanId]) - 1])[0]:
                            x[value[0]] = value
                            candleData[chanId].append(x)
                            removeStaleData(chanId)
                    else:
                        if value > list(candleData[chanId][len(candleData[chanId]) - 1])[0]:
                            x[value] = data
                            candleData[chanId].append(x)
                            removeStaleData(chanId)
            chanKey = channelKeys[chanId].split(':')
            time_frame = chanKey[1]
            key = chanKey[2][1:]
            strategies = examine_strategies(key, time_frame, candleData[chanId])
            if strategies:
                update_strategy_list(channelKeys[chanId], strategies)

        print(data)

def on_error(error):
    print(error)

def on_close():
    print("### closed ###")

def on_open(ws):
    for key in constants.coinbase:
        for time_frame in constants.time_frame:
            ws.send('{' + constants.subscribe[id.ws_subscribe].format(time_frame, key.upper()) + '}')


def push_data():
    tempClientPush(strategyList)


def update_strategy_list(key, strategies):
    for value in strategies:
        strategy = list(value)[0]
        if strategy not in strategyList:
            strategyList[strategy] = [{key:value[strategy][id.price_action]}]
        else:
            strategyList[strategy].append({key:value[strategy][id.price_action]})
        print('wow')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(constants.url[id.ws_candles],
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)


    ws.on_open = on_open
    t = threading.Thread(target=ws.run_forever)
    t.start()
