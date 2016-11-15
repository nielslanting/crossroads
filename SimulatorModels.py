from enum import Enum
import json
from json import JSONEncoder

class SimulatorNodeState():

    def __init__(self, n, c):
        self.trafficLight = n
        self.count = c

class SimulatorState():
    state = []

    def __init__(self, s):
        self.state = s
    
    def toJSON(self):
        raw = json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

        return unicode(raw, 'utf-8')
