import json
from SimulatorModels import SimulatorNodeState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from config import GRAPHIDS, PORT

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

                ids = []
                for n in parsed['state']:
                    ids.append(n['trafficLight'])
                    result.append(SimulatorNodeState(n['trafficLight'], n['count']))

                # Fix unspecified trafficLight Nodes
                for n in GRAPHIDS:
                    if n not in ids:
                        result.append(SimulatorNodeState(n, 0))

                root.simulatorState.set(result)

            def handleConnected(self):
                root.clients.append(self)
                print self.address, 'connected'

            def handleClose(self):
                root.clients.remove(self)
                print self.address, 'closed'

        server = SimpleWebSocketServer('', PORT, SimpleEcho)
        server.serveforever()
