import time
import sys
import os

from WeightState import WeightState, generateWeightState
from ControllerModels import LightState, NodeState
from Formations import FormationFinder

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Controller:

    def __init__(self, sState, cState):
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
            os.system('clear')
            print 'Traffic light controller by Niels Lanting.'
            print 'Press CRTL + Shift + \\ to abort the application.'
            print ' '
            
            nodeLogs = []

            self.prevControllerState = list(self.controllerState.get())

            newState = self.generateState(self.simulatorState.get(), 
                self.weightState)

            for n in self.simulatorState.get():
                cCount = str(n.count).ljust(3)

                if n.count > 0:
                    cCount = bcolors.OKBLUE + cCount + bcolors.ENDC

                nodeLogs.append('Node ' + str(n.trafficLight).ljust(3) + ' | Cars: ' + cCount)

            orangeNewState = []
            for i, n in enumerate(newState):
                ls = LightState[n.status]

                if self.prevControllerState[i].status == LightState.green.name and n.status == LightState.red.name:
                    ls = LightState.orange
                if self.prevControllerState[i].status == LightState.orange.name:
                    ls = LightState.red

                orangeNewState.append(NodeState(n.trafficLight, ls))


            self.controllerState.set(orangeNewState)

            for i, n in enumerate(self.controllerState.get()):
                cStatus = n.status.ljust(7)

                if n.status == LightState.red.name:
                    cStatus = bcolors.FAIL + cStatus + bcolors.ENDC
                elif n.status == LightState.orange.name:
                    cStatus = bcolors.WARNING + cStatus + bcolors.ENDC
                elif n.status == LightState.green.name:
                    cStatus = bcolors.OKGREEN + cStatus + bcolors.ENDC

                nodeLogs[i] = nodeLogs[i] + ' | Current State: ' + cStatus

            for i, n in enumerate(self.prevControllerState):
                
                cStatus = n.status.ljust(7)

                if n.status == LightState.red.name:
                    cStatus = bcolors.FAIL + cStatus + bcolors.ENDC
                elif n.status == LightState.orange.name:
                    cStatus = bcolors.WARNING + cStatus + bcolors.ENDC
                elif n.status == LightState.green.name:
                    cStatus = bcolors.OKGREEN + cStatus + bcolors.ENDC

                nodeLogs[i] = nodeLogs[i] + ' | Last state: ' + cStatus

            for i, n in enumerate(self.weightState):
                cWeight = str(n.weight).ljust(7)

                if n.weight > 0:
                    cWeight = bcolors.OKBLUE + cWeight + bcolors.ENDC

                nodeLogs[i] = nodeLogs[i] + ' | Weight: ' + cWeight

            for n in nodeLogs:
                print n

            self.weightState = generateWeightState(self.weightState, 
                                        self.controllerState.get(), 
                                        self.simulatorState.get())
            
            time.sleep(5) 
