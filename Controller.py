import time

from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from WeightState import WeightState, generateWeightState

class Controller:

    def __init__(self, sState, cState):
        self.simulatorState = sState
        self.controllerState = cState
        self.weightState = map(lambda x: WeightState(x.trafficLight, 0), self.simulatorState.get())

        self.run()

    # Turns green if the count is higher
    def generateState(self, state, wState):
        newState = []
        greenSet = False 

        # Calculate the total weight
        ws = []
        for i, n in enumerate(wState):
            total = n.weight + state[i].count
            ws.append(WeightState(n.node, total))
        
        # Create the new state
        for n in sorted(ws, reverse=True):
            ls = LightState.red
            
            if n.weight > 0 and greenSet == False:
                ls = LightState.green
                greenSet = True

            newState.append(NodeState(n.node, ls));

        return sorted(newState)

    def run(self):
        while(True):
            
            self.controllerState.set(self.generateState(self.simulatorState.get(), self.weightState))

            self.weightState = generateWeightState(self.weightState, 
                                        self.controllerState.get(), 
                                        self.simulatorState.get())
            
            time.sleep(10) 
