from enum import Enum
import json
from json import JSONEncoder

class SimulatorNodeState():

    def __init__(self, n, c):
        self.trafficLight = n
        self.count = c

    def __repr__(self):
        return 'n {}: {}'.format(self.trafficLight, self.count)

class SimulatorState():
    def __init__(self, s = []):
        self._state = s
        self._observers = []
    
    # Get & Set Logic
    def get(self):
        return self._state

    def set(self, s):
        self._state = s
        for callback in self._observers:
            callback(self)

    # Observer Logic
    def subscribe(self, callback):
        self._observers.append(callback)

    def unsubscribe(self, callback):
        self._observers.remove(callback)

    # JSON serialize Logic
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
