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

            def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
            def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

            def handleMessage(self):
                print 'received message'

                result = []
                parsed = json.loads(self.data)

                for n in parsed['state']:
                    result.append(SimulatorNodeState(n['trafficLight'], n['count']))
                
                parentSelf.parent.simulatorState.state = result 


            def handleConnected(self):
                parentSelf.parent.clients.append(self)
                print self.address, 'connected'

            def handleClose(self):
                parentSelf.parent.clients.remove(self)
                print self.address, 'closed'

        server = SimpleWebSocketServer('', 8000, SimpleEcho)
        server.serveforever()
