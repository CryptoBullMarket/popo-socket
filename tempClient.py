from websocket import create_connection
import json

ws = create_connection('ws://127.0.0.1:9005')
ws.send('{' + '"event": "sendMessage", "message":{}'.format(json.dumps('{')) + '}')
ws.close()