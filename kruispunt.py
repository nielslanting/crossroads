import threading

from controllermodels import LightState, NodeState, State
from simulatormodels import SimulatorNodeState, SimulatorState

from controller import Controller
from sock import Socket
from monitor import Monitor
from config import GRAPHIDS

class Kruispunt(object):
    
    def __init__(self):

        self.controllerState = State(map(lambda x: NodeState(x, LightState.red), GRAPHIDS))
        self.simulatorState = SimulatorState(map(lambda x: SimulatorNodeState(x, 0), GRAPHIDS))

    def run(self):

        # Start the controller thread
        t = threading.Thread(target = Controller, args=([self.simulatorState, self.controllerState, Monitor()]))
        t.deamon = True
        t.start()

        # Start the websocket
        socket = Socket(self.simulatorState, self.controllerState).run()

if __name__ == "__main__":
    Kruispunt().run()

