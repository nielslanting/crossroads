import threading
import time
import random
import json
from ResponseModels import LightState, NodeState, State
from RequestModels import RequestNodeState, RequestState
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

# Init the server
port = 8000
print "Server started on port: " + str(port)

# Graph ids
graphIds = range(1, 11) + range(21, 29) + range(31, 39) + [42, 45];

# Create the initial states
state = State(map(lambda x: NodeState(x, LightState.red), graphIds))
simulatorState = RequestState

def Controller():
    global state
    global simulatorState

    while(True):
        print 'kaas'
        time.sleep(3) 

def main():
    global state
    global clients
    global simulatorState

    # Start the controller thread
    t = threading.Thread(target = Controller)
    t.deamon = True
    t.start()

    class SimpleEcho(WebSocket):

        def as_payload(dct):
            return RequestState(dct['state'])

        def handleMessage(self):
            parsed = json.loads(self.data)
            simulatorState = RequestState(parsed['state'])

        def handleConnected(self):
            clients.append(self)
            print self.address, 'connected'

        def handleClose(self):
            clients.remove(self)
            print self.address, 'closed'

    server = SimpleWebSocketServer('', port, SimpleEcho)
    server.serveforever()

if __name__ == "__main__": main()
