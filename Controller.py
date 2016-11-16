import time

from WeightState import WeightState, generateWeightState
from ControllerModels import LightState, NodeState
from Formations import FormationFinder

class Controller:

    def __init__(self, sState, cState):
        self.simulatorState = sState
        self.controllerState = cState
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
            total = n.weight + state[i].count
            ws.append(WeightState(n.node, total))
        
        # Calculate best formation
        bestFormation = self.formationFinder.find_best_formation(ws)

        # Create the new state
        for n in sorted(ws, reverse=True):
            ls = LightState.red
            
            if n.weight > 0  and n.node in bestFormation:
                ls = LightState.green

            newState.append(NodeState(n.node, ls));

        return sorted(newState)

    def run(self):
        while(True):
            
            newState = self.generateState(self.simulatorState.get(), 
                self.weightState)

            self.controllerState.set(newState)

            self.weightState = generateWeightState(self.weightState, 
                                        self.controllerState.get(), 
                                        self.simulatorState.get())
            
            time.sleep(10) 
