from enum import Enum
import json
from json import JSONEncoder

class LightState(Enum):
    red = 'red'
    orange = 'organge'
    green = 'green'

class NodeState():

    def __init__(self, n, ls):
        self.trafficLight = n
        self.status = ls.name

    def __eq__(self, other):
        return self.trafficLight == other.trafficLight and self.status == other.status

class State():
    state = []

    def __init__(self, s = []):
        self.state = s
    
    def toJSON(self):
        raw = json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
        return unicode(raw, 'utf8')

    def __eq__(self, other):
        for id, ns in enumerate(self.state):
            if ns != other.state[id]:
                return False

        return True

