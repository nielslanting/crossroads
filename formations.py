import itertools
from itertools import chain, combinations
from weightstate import WeightState

class Formation:
    def __init__(self, n, cn = []):
        self.node = n
        self.counterNodes = cn

    def __repr__(self):
        return 'n {}: {}'.format(self.node, self.counterNodes)

class FormationFinder:
    _formations = [
        Formation(1, [3, 7, 42, 28, 38]),
        Formation(2, [3, 4, 7, 8, 9, 10]),
        Formation(3, [1, 2, 6, 7, 10, 42]),
        Formation(4, [2, 6, 7, 8, 9, 10]),
        Formation(5, [9]),
        Formation(6, [3, 4, 9, 10]),
        Formation(7, [1, 2, 3, 4, 9, 10, 42]),
        Formation(8, [2, 4, 42]),
        Formation(9, [2, 5, 6, 7, 42]),
        Formation(10, [2, 3, 4, 6, 42]),
        Formation(21, [1, 2, 42]),
        Formation(22, [3, 6, 10]),
        Formation(23, [45]),
        Formation(24, [45]),
        Formation(25, [5, 6, 7]),
        Formation(26, [2, 4, 8, 42]),
        Formation(27, [8, 9, 10]),
        Formation(28, [1, 4, 7]),
        Formation(31, [1, 2, 42]),
        Formation(32, [3, 6, 10]),
        Formation(33, [45]),
        Formation(34, [45]),
        Formation(35, [5, 6, 7]),
        Formation(36, [2, 4, 8, 42]),
        Formation(37, [8, 9, 10]),
        Formation(38, [1, 3, 7]),
        Formation(42, [1, 2, 3, 4, 8, 9, 10, 71]),
        Formation(45, [3, 4, 5, 9, 22, 23, 24, 34, 32, 33, 46]),
        Formation(46, [3, 4, 5, 9, 22, 23, 24, 34, 32, 33, 45])
    ]

    def __init__(self):
        new = []

        for x in self._formations:
            cn = list(x.counterNodes)
            for y in self._formations:
                if x.node in y.counterNodes:
                    cn.append(y.node)
            new.append(Formation(x.node, cn))
        
        self._formations = new

    # Finds some possible subsets of trafficLights
    def find_subsets(self, weightState):
        
        subsets = []

        #weightedNodes = filter(lambda x: x.weight > 0, weightState)
        #ids = map(lambda x: x.node, weightedNodes)
        ids = map(lambda x: x.node, weightState)
            
        maxLen = len(ids) + 1
        if maxLen > 4: maxLen = 4;

        for n in range(1, maxLen):
          for subset in itertools.combinations(ids, n):
            subsets.append(list(subset))

        return subsets

    # Calculates which trafficLight subset would benefit the most
    def calculate_subset_weight(self, subsets, weightState):
        result = []

        for subset in subsets:
            weight = 0
            for n in subset:
                ws = next((x for x in weightState if x.node == n), None)
                weight = weight + ws.weight
            
            result.append(WeightState(subset, weight))

        return sorted(result, reverse=True)

    # Calculates which trafficLights can also turn green without interference
    def calculate_complimentary(self, weightState, selected):

        result = []
        blocked = []

        # Generate the currently blocked nodes
        for s in selected:
            found = [x for x in self._formations if x.node == s]
            for f in found:
                blocked = blocked + f.counterNodes

        # Test new formations
        for f in self._formations:
            if f.node in blocked: continue
            found = [x for x in weightState if x.node == f.node]
            if len(found) <= 0 or found[0].weight <= 0: continue
            
            result.append(f.node)
            blocked = blocked + f.counterNodes
            
        return list(set(result))

    # Selects the best subset without causing conflicts
    def find_best_formation(self, weightState):

        subsets = self.find_subsets(weightState)
        weightedSubsets = self.calculate_subset_weight(subsets, weightState)

        for subset in weightedSubsets:
            blocked = []

            for node in subset.node:
                formation = next((x for x in self._formations if x.node == node), None)
                if formation != None:
                    blocked = blocked + formation.counterNodes 
                
            foundBlocked = False

            for node in subset.node:
                if node in blocked:
                    foundBlocked = True
                    continue

            if foundBlocked == True: continue
            
            complimentary = self.calculate_complimentary(weightState, subset.node)

            return list(set(subset.node + complimentary))

        return []
