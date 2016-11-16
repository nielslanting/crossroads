import itertools
from WeightState import WeightState

class Formation:
    def __init__(self, n, cn = []):
        self.node = n
        self.counterNodes = cn

class FormationFinder:
    _formations = [
        Formation(1, [3, 7, 42]),
        Formation(2, [3, 4, 7, 8, 9, 10]),
        Formation(3, [1, 2, 6, 7, 10, 42]),
        Formation(4, [2, 6, 7, 8, 9]),
        Formation(5, [9]),
        Formation(6, [3, 4, 9, 10]),
        Formation(7, [1, 2, 3, 4, 9, 10, 42]),
        Formation(8, [2, 4, 42]),
        Formation(9, [2, 5, 6, 7, 42]),
        Formation(10, [2, 3, 6, 42]),
        Formation(42, [1, 3, 4, 8, 9, 10, 71]),
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
        Formation(38, [1, 4, 7]),
    ]

    def find_all_subsets(self, weightState):
        subsets = []
        ids = map(lambda x: x.node, weightState)

        for n in range(1, len(ids)+1):
          for subset in itertools.combinations(ids, n):
            subsets.append(list(subset))

        return subsets

    def calculate_subset_weight(self, subsets, weightState):
        result = []

        for subset in subsets:
            weight = 0
            for n in subset:
                ws = next((x for x in weightState if x.node == n), None)
                weight = weight + ws.weight
            
            result.append(WeightState(subset, weight))

        return sorted(result, reverse=True)

    def find_best_formation(self, weightState):
        # Calculate the weights of all posibilities

        subsets = self.find_all_subsets(weightState)
        weightedSubsets = self.calculate_subset_weight(subsets, weightState)

        for subset in weightedSubsets:
            blocked = []

            for node in subset.node:
                formation = next((x for x in self._formations if x.node == node), None)
                blocked = blocked + formation.counterNodes 
                
            foundBlocked = False

            for node in subset.node:
                if node in blocked:
                    foundBlocked = True
                    continue

            if foundBlocked == True: continue

            return subset.node

        return []
