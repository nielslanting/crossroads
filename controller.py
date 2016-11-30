import time
import sys

from weightstate import WeightState, generateWeightState
from controllermodels import LightState, NodeState
from formations import FormationFinder
from monitor import Monitor

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

        period = 0
        while(True):
            
            #self.monitor.clear()
            #self.monitor.printHeader()
            self.monitor.write(period)

            self.prevControllerState = list(self.controllerState.get())

            newState = self.generateState(self.simulatorState.get(), 
                self.weightState)

            self.weightState = generateWeightState(self.weightState, 
                                        self.controllerState.get(), 
                                        self.simulatorState.get())

            if period == 0:
                self.controllerState.set(newState)
                time.sleep(5) 

            elif period == 1:
                orangeNewState = []

                for i, n in enumerate(self.controllerState.get()):
                    ls = LightState[n.status]

                    if self.prevControllerState[i].status == LightState.green.name:
                        ls = LightState.orange

                    orangeNewState.append(NodeState(n.trafficLight, ls))
                self.controllerState.set(orangeNewState)

                time.sleep(2)

            elif period == 2:
                period = -1
                
                redNewState = []
                for i, n in enumerate(self.controllerState.get()):
                    ls = LightState.red
                    redNewState.append(NodeState(n.trafficLight, ls))

                self.controllerState.set(redNewState)
                time.sleep(2)

            #self.monitor.printState(self.simulatorState, self.controllerState, self.prevControllerState, self.weightState);
            period = period + 1
