import threading
import time
import random
import json
from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Controller:

    def __init__(self, parent):
        self.parent = parent

    # Creates a new state with random LightStates
    def scrambleState(self, state):
        newState = []

        for node in state:
            ls = LightState.red
            rand = random.randint(0, 2)
            
            if rand == 0:
                ls = LightState.green
            elif rand == 1:
                ls = LightState.orange
                
            newState.append(NodeState(node.trafficLight, ls));

        return newState


    def run(self):
        while(True):
            
            self.parent.controllerState.state = self.scrambleState(self.parent.controllerState.state)
            parsed = self.parent.controllerState.toJSON().decode('utf-8')
           
            print 'connected clients: ' + str(len(self.parent.clients))
            for client in self.parent.clients:
                client.sendMessage(parsed)

            time.sleep(3) 
