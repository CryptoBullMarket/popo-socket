from res import id as id, constants as constants
from websocket_server import WebsocketServer
from threading import Thread
from time import time, sleep
import sched
import simplejson as json
import boto3

scheduler = sched.scheduler(time, sleep)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PeopleCounter')

class AttendeeServer(Thread):
    clients = {}
    broadcast_counter = 0

    # Called for every client connecting (after handshake)
    def new_client(self, client, server):
        print("New client connected and was given id %d" % client['id'])
        #self.server.send_message_to_all("Hey all, a new client has joined us")

    # Called for every client disconnecting
    def client_left(self, client, server):
        print("Client(%d) disconnected" % client['id'])

    # Called when a client sends a message
    def message_received(self, client, server, message):
        if len(message) > 200:
            message = message[:200] + '..'
        print("Client(%d) said: %s" % (client['id'], message))

    def broadcast(self):
        response = table.scan()
        items = response['Items']
        while True:
            print('Total items: ' + str(len(response['Items'])))
            if response.get('LastEvaluatedKey'):
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items += response['Items']
            else:
                break
        self.broadcast_counter += 1
        print('Broadcast number: ', self.broadcast_counter)
        self.all = self.server.send_message_to_all(json.dumps(items))

    def run(self):
        self.server = WebsocketServer(host=constants.server[id.host], port=9006) #constants.server[id.port])
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

class DataFetcher(Thread):

    def __init__(self, ass):
        ''' Constructor. '''
        Thread.__init__(self)
        self.AttendeeServer = ass

    def run(self):
        while True:
            scheduler.enter(constants.scheduler_params[id.delay], constants.scheduler_params[id.priority], self.AttendeeServer.broadcast)
            scheduler.run()

if __name__ == "__main__":

    ass = AttendeeServer()
    ass.start()
    df = DataFetcher(ass)
    df.start()