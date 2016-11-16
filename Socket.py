import threading
import time
import random
import json
from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Socket():

    def __init__(self, sState, cState):
        self.clients = []
        self.simulatorState = sState
        self.controllerState = cState
        cState.subscribe(self.controller_update)

    def controller_update(self, o):
        parsed = o.toJSON().decode('utf-8')
        for client in self.clients:
            client.sendMessage(parsed)

    def run(self):
        root = self

        class SimpleEcho(WebSocket):

            def as_payload(dct):
                return RequestState(dct['state'])

            def handleMessage(self):
                result = []
                parsed = json.loads(self.data)

                for n in parsed['state']:
                    result.append(SimulatorNodeState(n['trafficLight'], n['count']))
                
                root.simulatorState.set(result)

            def handleConnected(self):
                root.clients.append(self)
                print self.address, 'connected'

            def handleClose(self):
                root.clients.remove(self)
                print self.address, 'closed'

        server = SimpleWebSocketServer('', 8000, SimpleEcho)
        server.serveforever()
