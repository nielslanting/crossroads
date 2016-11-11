from enum import Enum
import json
from json import JSONEncoder

# Enum of possible states (red, yellow, green)
class LightState(Enum):
    red = 'red'
    orange = 'organge'
    green = 'green'

# The state of a node
class NodeState():

    def __init__(self, n, ls):
        self.trafficLight = n
        self.status = ls.name

    def set(self, ls):
        self.status = ls

    def __eq__(self, other):
        return self.trafficLight == other.trafficLight and self.status == other.status

class State():
    state = []

    def __init__(self, s = []):
        self.state = s
    
    def add(self, i):
        self.state.append(i)

    def get(self):
        return self.state

    def getItem(self, i):
        return self.state[i]

    def setItem(self, i, ls):
        return self.state[i].set(ls)

    def toJSON(self):
        raw = json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
        return unicode(raw, 'utf8')

    def __eq__(self, other):
        print 'compf'
        for id, ns in enumerate(self.state):
            if ns != other.getItem(id):
                return False

        return True

