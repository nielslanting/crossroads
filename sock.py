import json
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from simulatormodels import SimulatorNodeState
from config import GRAPH_IDS, PORT

class Socket():

    def __init__(self, sState, cState):
        self.clients = []
        self.simulatorState = sState
        self.controllerState = cState
        cState.subscribe(self.controller_update)

    # Send WS message to all clients when the controller state changes
    def controller_update(self, state):
        message = state.toJSON()

        for client in self.clients:
            client.sendMessage(message)

    # Run the socket
    def run(self):
        root = self

        class SimpleEcho(WebSocket):

            def as_payload(dct):
                return RequestState(dct['state'])

            def handleMessage(self):
                parsed = json.loads(self.data)

                # Generate the simulator state
                result = []
                ids = []
                for n in parsed['state']:
                    ids.append(n['trafficLight'])
                    result.append(SimulatorNodeState(n['trafficLight'], n['count']))

                # Fix unspecified trafficLight Nodes
                for n in GRAPH_IDS:
                    if n not in ids:
                        result.append(SimulatorNodeState(n, 0))

                sortedResult = sorted(result, key=lambda x: x.trafficLight)
                filteredResult = filter(lambda x: x.trafficLight in GRAPH_IDS, sortedResult)
                uniqueResult = list(set(filteredResult))
                sortedResult = sorted(uniqueResult, key=lambda x: x.trafficLight, reverse=False)

                finalResult = []
                finalIds = []
                for r in sortedResult:
                    if r.trafficLight not in finalIds:
                        finalResult.append(r)
                        finalIds.append(r.trafficLight)

                root.simulatorState.set(finalResult)

            def handleConnected(self):
                root.clients.append(self)

            def handleClose(self):
                root.clients.remove(self)

        server = SimpleWebSocketServer('', PORT, SimpleEcho)
        server.serveforever()
