from ControllerModels import LightState, NodeState, State

class WeightState:
    def __init__(self, n, w):
        self.node = n;
        self.weight = w;

    def __cmp__(self, other):
        if hasattr(other, 'weight'):
            return self.weight.__cmp__(other.weight)

    def __repr__(self):
        return 'n {}: {}'.format(self.node, self.weight)

""" Generates a new WeightState 
:param state: The current WeightState 
:param cState: The ControllerState 
:param sState: The SimulatorState 
:returns: a new WeightState 
"""
# Generates a new state
def generateWeightState(state = [], cState = [], sState = []):
    newState = []

    for i, n in enumerate(state):
        if cState[i].status == LightState.red.name and sState[i].count > 0:
            newState.append(WeightState(n.node, n.weight + 1))
        else:
            newState.append(WeightState(n.node, 0))

    return newState
