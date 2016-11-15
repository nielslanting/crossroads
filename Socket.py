import threading
import time
import random
import json
from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Socket():
    def __init__(self, parent):
        self.parent = parent;
    
    def run(self):
        parentSelf = self

        class SimpleEcho(WebSocket):

            def as_payload(dct):
                return RequestState(dct['state'])

            def handleMessage(self):
                print 'received message'
                parsed = json.loads(self.data)
                simulatorState = SimulatorState(parsed['state'])

            def handleConnected(self):
                parentSelf.parent.clients.append(self)
                print self.address, 'connected'

            def handleClose(self):
                parentSelf.parent.clients.remove(self)
                print self.address, 'closed'

        server = SimpleWebSocketServer('', 8000, SimpleEcho)
        server.serveforever()
