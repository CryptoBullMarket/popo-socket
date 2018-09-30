import websocket
import json
from res import id as id, constants as constants

channelKeys = {}
candleData = {}

try:
    import thread
except ImportError:
    import _thread as thread

def on_message(ws, message):
    print(message)
    newMessage = json.loads(message)
    if id.chanId in newMessage:
        if newMessage[id.chanId] not in channelKeys:
            channelKeys[newMessage[id.chanId]] = newMessage[id.key]
    elif id.event in newMessage:
        print('Ignore')
    else:
        chanId = newMessage[0]
        data = newMessage[1]
        if data and type(data) == list:
            if type(data[0]) == list:
                data = sorted(data, key= lambda k:k[0])
            if chanId not in candleData:
                candleData[chanId] = []
                for value in data:
                    x = {}
                    x[value[0]] = value
                    candleData[chanId].append(x)
            else:
                for value in data:
                    if type(data[0]) == list:
                        if value[0] > list(candleData[chanId][len(candleData[chanId])-1])[0]:
                            x = {}
                            x[value[0]] = value
                            candleData[chanId].append(x)
                    else:
                        if value > list(candleData[chanId][len(candleData[chanId]) - 1])[0]:
                            x = {}
                            x[value] = data
                            candleData[chanId].append(x)

        print(data)



def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    for key in constants.coinbase:
        for time_frame in constants.time_frame:
            ws.send('{' + constants.subscribe[id.ws_subscribe].format(time_frame, key.upper()) + '}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(constants.url[id.ws_candles],
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()