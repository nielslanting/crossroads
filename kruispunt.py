import threading
import time
import random
import json

from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from Controller import Controller
from Socket import Socket

# The IDS of all graphs
graphIds = range(1, 11) + range(21, 29) + range(31, 39) + [42, 45];

class Kruispunt(object):
    
    def __init__(self):

        # Config
        self.port = 8000

        # States
        self.clients = []
        self.controllerState = State(map(lambda x: NodeState(x, LightState.red), graphIds))
        self.simulatorState = SimulatorState

    def run(self):

        print "Server started on port: " + str(self.port)

        # Start the controller thread
        t = threading.Thread(target = Controller, args=([self]))
        t.deamon = True
        t.start()

        # Start the websocket
        socket = Socket(self).run()

if __name__ == "__main__":
    Kruispunt().run()

