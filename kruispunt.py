import threading
import time
import random
import json
from ControllerModels import LightState, NodeState, State
from SimulatorModels import SimulatorNodeState, SimulatorState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

def main():

    # Init the server
    port = 8000
    clients = []
    print "Server started on port: " + str(port)

    # Graph ids
    graphIds = range(1, 11) + range(21, 29) + range(31, 39) + [42, 45];

    # Create the initial states
    state = State(map(lambda x: NodeState(x, LightState.red), graphIds))
    simulatorState = SimulatorState


    # Initialize the traffic light controller
    def Controller():

        # Creates a new state with random LightStates
        def scrambleState(state):
            newState = []

            for node in state:
                ls = LightState.red
                rand = random.randint(0, 2)
                
                if rand == 0:
                    ls = LightState.green
                elif rand == 1:
                    ls = LightState.orange
                    
                newState.append(NodeState(node.trafficLight, ls));

            return newState


        while(True):
            
            state.state = scrambleState(state.state)
            parsed = state.toJSON().decode('utf-8')

            for client in clients:
                client.sendMessage(parsed)

            time.sleep(3) 

    # Initialize the socket connection
    def ws():


        class SimpleEcho(WebSocket):

            def as_payload(dct):
                return RequestState(dct['state'])

            def handleMessage(self):
                parsed = json.loads(self.data)
                simulatorState = SimulatorState(parsed['state'])

            def handleConnected(self):
                clients.append(self)
                print self.address, 'connected'

            def handleClose(self):
                clients.remove(self)
                print self.address, 'closed'

        server = SimpleWebSocketServer('', port, SimpleEcho)
        server.serveforever()

    # Start the controller thread
    t = threading.Thread(target = Controller)
    t.deamon = True
    t.start()

    # Start the websocket
    ws()

if __name__ == "__main__": main()
