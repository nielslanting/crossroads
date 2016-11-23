import os
from ControllerModels import LightState, NodeState

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Monitor:
    def clear(self):
        os.system('clear')
    
    def write(self, message):
        print message

    def printHeader(self):
        self.write('Traffic light controller by Niels Lanting.')
        self.write('Press CRTL + Shift + \\ to abort the application.')
        self.write(' ')

    def printState(self, simulatorState, controllerState, prevControllerState, weightState):
        nodeLogs = []

        for n in simulatorState.get():
            cCount = str(n.count).ljust(3)

            if n.count > 0:
                cCount = bcolors.OKBLUE + cCount + bcolors.ENDC

            nodeLogs.append('Node ' + str(n.trafficLight).ljust(3) + ' | Cars: ' + cCount)

        for i, n in enumerate(controllerState.get()):
            cStatus = n.status.ljust(7)

            if n.status == LightState.red.name:
                cStatus = bcolors.FAIL + cStatus + bcolors.ENDC
            elif n.status == LightState.orange.name:
                cStatus = bcolors.WARNING + cStatus + bcolors.ENDC
            elif n.status == LightState.green.name:
                cStatus = bcolors.OKGREEN + cStatus + bcolors.ENDC

            nodeLogs[i] = nodeLogs[i] + ' | Current State: ' + cStatus

        for i, n in enumerate(prevControllerState):
            
            cStatus = n.status.ljust(7)

            if n.status == LightState.red.name:
                cStatus = bcolors.FAIL + cStatus + bcolors.ENDC
            elif n.status == LightState.orange.name:
                cStatus = bcolors.WARNING + cStatus + bcolors.ENDC
            elif n.status == LightState.green.name:
                cStatus = bcolors.OKGREEN + cStatus + bcolors.ENDC

            nodeLogs[i] = nodeLogs[i] + ' | Last state: ' + cStatus

        for i, n in enumerate(weightState):
            cWeight = str(n.weight).ljust(7)

            if n.weight > 0:
                cWeight = bcolors.OKBLUE + cWeight + bcolors.ENDC

            nodeLogs[i] = nodeLogs[i] + ' | Weight: ' + cWeight

        for n in nodeLogs:
            self.write(n)
