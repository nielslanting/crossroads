import time
import sys

from WeightState import WeightState, generateWeightState
from ControllerModels import LightState, NodeState
from Formations import FormationFinder
from Monitor import Monitor

class Controller:

    def __init__(self, sState, cState, mon):
        self.monitor = mon
        self.simulatorState = sState
        self.controllerState = cState
        self.prevControllerState = list(cState.get())
        self.formationFinder = FormationFinder()
        self.weightState = map(lambda x: 
            WeightState(x.trafficLight, 0), self.simulatorState.get())

        self.run()

    # Turns green if the count is higher
    def generateState(self, state, wState):
        newState = []

        # Calculate the total weight
        ws = []
        for i, n in enumerate(wState):
            total = n.weight

            if state[i]:
                total = total + state[i].count

            if (n.node == 42 or n.node == 45) and n.weight > 0:
                total = 9999

            ws.append(WeightState(n.node, total))
        
        # Calculate best formation
        filteredWs = filter(lambda x: x.weight > 0, ws)
        bestFormation = self.formationFinder.find_best_formation(filteredWs)

        # Create the new state
        for n in sorted(ws, reverse=True):
            ls = LightState.red
            
            if n.weight > 0  and n.node in bestFormation:
                ls = LightState.green

            newState.append(NodeState(n.node, ls));

        return sorted(newState)

    def run(self):
        while(True):
            
            self.monitor.clear()
            self.monitor.printHeader()

            self.prevControllerState = list(self.controllerState.get())

            newState = self.generateState(self.simulatorState.get(), 
                self.weightState)

            orangeNewState = []
            for i, n in enumerate(newState):
                ls = LightState[n.status]

                if self.prevControllerState[i].status == LightState.green.name and n.status == LightState.red.name:
                    ls = LightState.red
                if self.prevControllerState[i].status == LightState.orange.name:
                    ls = LightState.red

                orangeNewState.append(NodeState(n.trafficLight, ls))


            self.controllerState.set(orangeNewState)

            self.monitor.printState(self.simulatorState, self.controllerState, self.prevControllerState, self.weightState);

            self.weightState = generateWeightState(self.weightState, 
                                        self.controllerState.get(), 
                                        self.simulatorState.get())
            
            time.sleep(5) 
