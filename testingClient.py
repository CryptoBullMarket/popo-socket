import websocket
import json


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print('Client is open')
    #ws.send('{' + constants.subscribe[id.ws_subscribe].format('5m', 'IOTETH') + '}')
    #ws.send('{' + '"event": "sendMessage", "key": "trade:5m:tIOTETH", "message":"Hello bitches"' + '}')

def on_message(ws, message):
    print('Message received')


if __name__ == "__main__":
    websocket.enableTrace(True)
    try:
        ws = websocket.WebSocketApp('ws://127.0.0.1:9005',
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()
    except Exception as e:
        print('Error is %s' % e)