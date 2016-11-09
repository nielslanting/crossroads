from enum import Enum
import json
from json import JSONEncoder

# The state of a node
class RequestNodeState():

    def __init__(self, n, c):
        self.trafficLight = n
        self.count = c

class RequestState():
    state = []

    def __init__(self, s):
        self.state = s
    
    def add(self, i):
        self.state.append(i)

    def get(self):
        return self.state

    def get(self, i):
        return self.state[i]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
