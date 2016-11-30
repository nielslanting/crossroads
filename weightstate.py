from controllermodels import LightState, NodeState, State

class WeightState:
    def __init__(self, n, w):
        self.node = n;
        self.weight = w;

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
        if cState[i].status == LightState.red.name and sState[i].count > 0:
            newState.append(WeightState(n.node, n.weight + 1))
        else:
            newState.append(WeightState(n.node, 0))


    # Sets weight the same for combined nodes
    combos = [
        [27, 28],
        [37, 38],
        [35, 36],
        [25, 26],
        [21, 22],
        [31, 32]
    ]
    
    for c in combos:
        print 'looking for ' + str(c[0])
        print 'looking for ' + str(c[1])

        a = filter(lambda x: x.node == c[0], newState)
        b = filter(lambda x: x.node == c[1], newState)

        if len(a) > 0 and len(b) > 0:
            print 'found yay'
            if a[0].weight > b[0].weight:
                b[0].weight = a[0].weight
            else:
                a[0].weight = b[0].weight

    return newState
