import json
from SimulatorModels import SimulatorNodeState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

# TODO: Duplicate declaration fix pls
graphIds = range(1, 11) + range(21, 29) + range(31, 39) + [42, 45];

class Socket():

    def __init__(self, sState, cState):
        self.clients = []
        self.simulatorState = sState
        self.controllerState = cState
        cState.subscribe(self.controller_update)

    def controller_update(self, o):
        message = o.toJSON()

        for client in self.clients:
            client.sendMessage(message)

    def run(self):
        root = self

        class SimpleEcho(WebSocket):

            def as_payload(dct):
                return RequestState(dct['state'])

            def handleMessage(self):
                result = []
                parsed = json.loads(self.data)

                #print 'received: '
                #print parsed
                
                ids = []
                for n in parsed['state']:
                    ids.append(n['trafficLight'])
                    result.append(SimulatorNodeState(n['trafficLight'], n['count']))

                # Fix unspecified trafficLight Nodes
                for n in graphIds:
                    if n not in ids:
                        result.append(SimulatorNodeState(n, 0))
                
                root.simulatorState.set(result)

            def handleConnected(self):
                root.clients.append(self)
                print self.address, 'connected'

            def handleClose(self):
                root.clients.remove(self)
                print self.address, 'closed'

        server = SimpleWebSocketServer('', 8000, SimpleEcho)
        server.serveforever()
