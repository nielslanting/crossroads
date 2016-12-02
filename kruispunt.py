import threading

from controllermodels import LightState, NodeState, State
from simulatormodels import SimulatorNodeState, SimulatorState

from controller import Controller
from sock import Socket
from monitor import Monitor
from config import GRAPH_IDS

class Kruispunt(object):
    
    def __init__(self):

        self.controllerState = State(map(lambda x: NodeState(x, LightState.red), GRAPH_IDS))
        self.simulatorState = SimulatorState(map(lambda x: SimulatorNodeState(x, 0), GRAPH_IDS))

    def run(self):

        # Start the controller thread
        controller = Controller(self.simulatorState, self.controllerState, Monitor())
        t = threading.Thread(target = controller.run)
        t.deamon = True
        t.start()

        # Start the websocket
        socket = Socket(self.simulatorState, self.controllerState).run()

if __name__ == "__main__":
    Kruispunt().run()

