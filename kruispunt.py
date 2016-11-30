import threading

from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState

from Controller import Controller
from Socket import Socket
from Monitor import Monitor
from config import GRAPHIDS

class Kruispunt(object):
    
    def __init__(self):

        self.controllerState = State(map(lambda x: NodeState(x, LightState.red), GRAPHIDS))
        self.simulatorState = SimulatorState(map(lambda x: SimulatorNodeState(x, 0), GRAPHIDS))

    def run(self):

        print "Server started"

        # Start the controller thread
        t = threading.Thread(target = Controller, args=([self.simulatorState, self.controllerState, Monitor()]))
        t.deamon = True
        t.start()

        # Start the websocket
        socket = Socket(self.simulatorState, self.controllerState).run()

if __name__ == "__main__":
    Kruispunt().run()

