from controllermodels import LightState, NodeState, State
from config import COMBINED_WEIGHT_NODES

class WeightState:
    def __init__(self, node, weight):
        self.node = node;
        self.weight = weight

        # Give priority to bus & trains, the train from east needs to move first
        if type(node) is not list and weight > 0 and node >= 40:
            self.weight = 9999
            if node == 45: self.weight = 99999

    def __cmp__(self, other):
        if hasattr(other, 'weight'):
            return self.weight.__cmp__(other.weight)

    def __repr__(self):
        return 'n {}: {}'.format(self.node, self.weight)

# Generates a new state
def generateWeightState(state = [], cState = [], sState = []):
    newState = []

    # Calculates the new weight
    for i, n in enumerate(state):
        if cState[i].status == LightState.RED.name and sState[i].count > 0:
            newState.append(WeightState(n.node, n.weight + n.count + 1))
        else:
            newState.append(WeightState(n.node, 0))

    # Sets weight the same for combined nodes
    for c in COMBINED_WEIGHT_NODES:
        a = filter(lambda x: x.node == c[0], newState)
        b = filter(lambda x: x.node == c[1], newState)

        if len(a) > 0 and len(b) > 0:
            if a[0].weight > b[0].weight:
                b[0].weight = a[0].weight
            else:
                a[0].weight = b[0].weight

    return newState
