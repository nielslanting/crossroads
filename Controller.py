import threading
import time
import random
import json
from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class WeightState:
    def __init__(self, n, w):
        self.node = n;
        self.weight = w;

    def __cmp__(self, other):
        if hasattr(other, 'weight'):
            return self.weight.__cmp__(other.weight)

    def __repr__(self):
        return 'n {}: {}'.format(self.node, self.weight)

class Controller:

    def __init__(self, parent):
        print 'Controller started'

        self.parent = parent
        self.weightState = map(lambda x: WeightState(x.trafficLight, 0), parent.simulatorState.state)

        # Starts the controller loop
        self.run()

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

    # Turns green if the count is higher
    def generateState(self, state, wState):
        newState = []
        greenSet = False 
        #print 'node 1 count: ' + str(state[0].count)

        # Calculate the total weight
        ws = []
        for i, n in enumerate(wState):
            total = n.weight + state[i].count
            ws.append(WeightState(n.node, total))
        
        # Create the new state
        for n in sorted(ws, reverse=True):
            ls = LightState.red
            
            if n.weight > 0:
                print 'node ' + str(n.node) + ' weights: ' + str(n.weight)


            if n.weight > 0 and greenSet == False:
                ls = LightState.green
                greenSet = True

            newState.append(NodeState(n.node, ls));

        print '---'

        return sorted(newState)

    def generateWeightState(self, state, cState, sState):
        newState = []

        for i, n in enumerate(state):
            if cState[i].status == LightState.red.name and sState[i].count > 0:
                print str(cState[i].trafficLight) + ' = ' + str(n.node) + 'is red increasing weight'
                newState.append(WeightState(n.node, n.weight + 1))
            else:
                newState.append(WeightState(n.node, 0))

        return newState

    def run(self):
        while(True):
            
            self.parent.controllerState.state = self.generateState(self.parent.simulatorState.state, self.weightState)
            self.weightState = self.generateWeightState(self.weightState, self.parent.controllerState.state, self.parent.simulatorState.state)
            
            #print 'ws:'
            #print self.weightState 

            #print 'cs:'
            #print self.parent.controllerState.state

            #print 'ss:'
            #print self.parent.simulatorState.state

            # Send a message to all connected clients
            #print 'connected clients: ' + str(len(self.parent.clients))
            parsed = self.parent.controllerState.toJSON().decode('utf-8')
            for client in self.parent.clients:
                client.sendMessage(parsed)

            time.sleep(10) 
