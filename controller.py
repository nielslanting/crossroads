import time
import sys

from weightstate import WeightState, generateWeightState
from controllermodels import LightState, NodeState
from formations import FormationFinder
from monitor import Monitor
from config import SLEEP_TIME, SLEEP_TIME_CLEARANCE

class Controller:

    def __init__(self, sState, cState, mon):
        self.monitor = mon
        self.simulatorState = sState
        self.controllerState = cState
        self.prevControllerState = list(cState.get())
        self.formationFinder = FormationFinder()
        self.weightState = map(lambda x: 
            WeightState(x.trafficLight, 0), self.simulatorState.get())

    # Turns green if the count is higher
    def generateState(self, state, weightState):
        newState = []

        # Calculate the total weight
        newWeightState = []
        for i, trafficLight in enumerate(weightState):
            total = trafficLight.weight

            if state[i]:
                total = total + state[i].count

            newWeightState.append(WeightState(trafficLight.node, total))
        
        # Calculate best formation
        filteredWeightState = filter(lambda x: x.weight > 0, newWeightState)
        bestFormation = self.formationFinder.find_best_formation(filteredWeightState)

        # Create the new state
        for trafficLight in sorted(weightState, reverse=True):
            lightState = LightState.red
            
            if trafficLight.weight > 0  and trafficLight.node in bestFormation:
                lightState = LightState.green

            newState.append(NodeState(trafficLight.node, lightState));

        # Returns the new state sorted by the trafficLight id
        return sorted(newState)

    # Main controller logic
    def run(self):

        period = LightState.red

        while(True):
            
            longClearance = False
            
            # Calculate the states
            self.prevControllerState = list(self.controllerState.get())

            newState = self.generateState(self.simulatorState.get(), 
                self.weightState)

            self.weightState = generateWeightState(self.weightState, 
                                        self.controllerState.get(), 
                                        self.simulatorState.get())

            if period == LightState.green:
                self.controllerState.set(newState)
                longClearance = True
                period = LightState.orange

            elif period == LightState.orange:
                orangeNewState = []

                for i, n in enumerate(self.controllerState.get()):
                    ls = LightState[n.status]

                    if self.prevControllerState[i].status == LightState.green.name:
                        ls = LightState.orange

                    orangeNewState.append(NodeState(n.trafficLight, ls))
                self.controllerState.set(orangeNewState)
                period = LightState.red

            elif period == LightState.red:

                redNewState = []
                for i, n in enumerate(self.controllerState.get()):
                    ls = LightState.red

                    # Longer lanes require longer clearance time
                    if n.trafficLight == 4 or n.trafficLight == 3:
                        longClearance = True

                    redNewState.append(NodeState(n.trafficLight, ls))

                self.controllerState.set(redNewState)
                period = LightState.green

            # Show the states on the monitor
            self.monitor.clear()
            self.monitor.printHeader()
            self.monitor.printState(self.simulatorState, self.controllerState, 
                self.prevControllerState, self.weightState);

            # Sleep timer
            # TODO: sleep times to constants
            time.sleep(SLEEP_TIME)
            if longClearance == True: time.sleep(SLEEP_TIME_CLEARANCE)

