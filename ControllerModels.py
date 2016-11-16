from enum import Enum
import json
from json import JSONEncoder

class LightState(Enum):
    red = 'red'
    orange = 'orange'
    green = 'green'

class NodeState():

    def __init__(self, n, ls):
        self.trafficLight = n
        self.status = ls.name

    def __eq__(self, other):
        return self.trafficLight == other.trafficLight and self.status == other.status

    def __repr__(self):
        return 'n {}: {}'.format(self.trafficLight, self.status)

    def __cmp__(self, other):
        if hasattr(other, 'trafficLight'):
            return self.trafficLight.__cmp__(other.trafficLight)

class State():

    def __init__(self, s = []):
        self._state = s
        self._observers = [] 

    # Get & Set logic
    def get(self):
        return self._state

    def set(self, s):
        self._state = s
        for callback in self._observers:
            callback(self)

    # Observer logic
    def subscribe(self, callback):
        self._observers.append(callback)

    def unsubscribe(self, callback):
        self._observers.remove(callback)
    
    # JSON serialize logic
    def serialize(self, o):
        res = o.__dict__.copy()

        if hasattr(o, '_state') and hasattr(o, '_observers'):
            res['state'] = self.get()
            del res['_observers']
            del res['_state']

        return res 

    def toJSON(self):
        raw = json.dumps(self, indent=4, default=self.serialize)
        return unicode(raw, 'utf-8')

    # Equality logic
    def __eq__(self, other):
        for id, ns in enumerate(self.get()):
            if ns != other.get()[id]:
                return False

        return True

