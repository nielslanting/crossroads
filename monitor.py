import os
from controllermodels import LightState, NodeState

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

    def _generateSimulatorLogs(self, logs, simulatorState):

        newLogs = list(logs)

        for n in simulatorState.get():
            cCount = str(n.count).ljust(3)

            if n.count > 0:
                cCount = bcolors.OKBLUE + cCount + bcolors.ENDC

            newLogs.append('Node ' + str(n.trafficLight).ljust(3) + ' | Cars: ' + cCount)

        return newLogs

    def _generateControllerLogs(self, logs, controllerState):

        newLogs = list(logs)

        for i, n in enumerate(controllerState.get()):
            cStatus = n.status.ljust(7)

            if n.status == LightState.RED.name:
                cStatus = bcolors.FAIL + cStatus + bcolors.ENDC
            elif n.status == LightState.ORANGE.name:
                cStatus = bcolors.WARNING + cStatus + bcolors.ENDC
            elif n.status == LightState.GREEN.name:
                cStatus = bcolors.OKGREEN + cStatus + bcolors.ENDC

            newLogs[i] = newLogs[i] + ' | Current State: ' + cStatus

        return newLogs

    def _generatePreviousLogs(self, logs, previousState):
        newLogs = list(logs)

        for i, n in enumerate(previousState):
            
            cStatus = n.status.ljust(7)

            if n.status == LightState.RED.name:
                cStatus = bcolors.FAIL + cStatus + bcolors.ENDC
            elif n.status == LightState.ORANGE.name:
                cStatus = bcolors.WARNING + cStatus + bcolors.ENDC
            elif n.status == LightState.GREEN.name:
                cStatus = bcolors.OKGREEN + cStatus + bcolors.ENDC

            newLogs[i] = newLogs[i] + ' | Last state: ' + cStatus

        return newLogs

    def _generateWeightState(self, logs, weightState):
        newLogs = list(logs)

        for i, n in enumerate(weightState):
            cWeight = str(n.weight).ljust(7)

            if n.weight > 0:
                cWeight = bcolors.OKBLUE + cWeight + bcolors.ENDC

            newLogs[i] = newLogs[i] + ' | Weight: ' + cWeight

        return newLogs

    def printState(self, sState, cState, pCState, wState):
        nodeLogs = []

        nodeLogs = self._generateSimulatorLogs(nodeLogs, sState)
        nodeLogs = self._generateControllerLogs(nodeLogs, cState)
        nodeLogs = self._generatePreviousLogs(nodeLogs, pCState)
        nodeLogs = self._generateWeightState(nodeLogs, wState)

        # Write all logs
        for n in nodeLogs:
            self.write(n)
