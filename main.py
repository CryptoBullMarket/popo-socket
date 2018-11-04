from res import id as id, constants as constants
from websocket_server import WebsocketServer
from StrategyMain import examine_strategies
from threading import Thread
from time import time, sleep
import websocket
import sched
import json


strategyList = {}
scheduler = sched.scheduler(time, sleep)

class PopoServer(Thread):
    clients = {}

    # Called for every client connecting (after handshake)
    def new_client(self, client, server):
        print("New client connected and was given id %d" % client['id'])
        self.server.send_message_to_all("Hey all, a new client has joined us")

    # Called for every client disconnecting
    def client_left(self, client, server):
        print("Client(%d) disconnected" % client['id'])

    # Called when a client sends a message
    def message_received(self, client, server, message):
        if len(message) > 200:
            message = message[:200] + '..'
        print("Client(%d) said: %s" % (client['id'], message))

    def broadcast(self):
        self.server.send_message_to_all(json.dumps(strategyList))


    def run(self):
        PORT = 9005
        self.server = WebsocketServer(PORT)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()


class BitfinexClient(Thread):
    channelKeys = {}
    candleData = {}



    def removeStaleData(self, chanId):
        no_removed = len(self.candleData[chanId]) - constants.history[id.history_size]
        for i in range(0, no_removed):
            del self.candleData[chanId][i]

    def on_message(self, message):
        newMessage = json.loads(message)

        if id.serverId in newMessage:
            print('Ignore')

        elif id.chanId in newMessage:
            if newMessage[id.chanId] not in self.channelKeys:
                self.channelKeys[newMessage[id.chanId]] = newMessage[id.key]
        else:
            chanId = newMessage[0]
            data = newMessage[1]
            if data and type(data) == list:
                if type(data[0]) == list:
                    data = sorted(data, key=lambda k: k[0])
                if chanId not in self.candleData:
                    self.candleData[chanId] = []
                    for value in data:
                        x = {}
                        if type(data[0]) == list:
                            x[value[0]] = value
                            self.candleData[chanId].append(x)
                            self.removeStaleData(chanId)
                        else:
                            x[value] = data
                            self.candleData[chanId].append(x)
                            self.removeStaleData(chanId)
                else:
                    for value in data:
                        x = {}
                        if type(data[0]) == list:
                            if value[0] > list(self.candleData[chanId][len(self.candleData[chanId]) - 1])[0]:
                                x[value[0]] = value
                                self.candleData[chanId].append(x)
                                self.removeStaleData(chanId)
                        else:
                            if value > list(self.candleData[chanId][len(self.candleData[chanId]) - 1])[0]:
                                x[value] = data
                                self.candleData[chanId].append(x)
                                self.removeStaleData(chanId)
                chanKey = self.channelKeys[chanId].split(':')
                time_frame = chanKey[1]
                key = chanKey[2][1:]
                strategies = examine_strategies(key, time_frame, self.candleData[chanId])
                if strategies:
                    self.update_strategy_list(self.channelKeys[chanId], strategies)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        for key in constants.coinbase:
            for time_frame in constants.time_frame:
                self.ws.send('{' + constants.subscribe[id.ws_subscribe].format(time_frame, key.upper()) + '}')

    def update_strategy_list(self, key, strategies):
        for value in strategies:
            strategy = list(value)[0]
            if strategy not in strategyList:
                strategyList[strategy] = [{key: value[strategy][id.price_action]}]
            else:
                strategyList[strategy].append({key: value[strategy][id.price_action]})

    def run(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(constants.url[id.ws_candles],
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_open=self.on_open)

        self.ws.run_forever()

class StrategyBroadcast(Thread):

    def __init__(self, ps):
        ''' Constructor. '''
        Thread.__init__(self)
        self.popoServer = ps

    def run(self):
        while True:
            scheduler.enter(id.delay, id.priority, self.popoServer.broadcast)
            scheduler.run()


if __name__ == "__main__":

    ps = PopoServer()
    ps.start()
    bc = BitfinexClient()
    bc.start()
    sb = StrategyBroadcast(ps)
    sb.start()