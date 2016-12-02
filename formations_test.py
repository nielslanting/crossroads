import unittest
import re

from formations import Formation, FormationFinder
from weightstate import WeightState

class TestFormations(unittest.TestCase):

    def test_formation_constructor(self):
        test = Formation(1, [1, 2, 3])

        self.assertEqual(test.nodes, [1])
        self.assertNotEqual(test.nodes, 1)
        self.assertNotEqual(test.nodes, [2])
        self.assertNotEqual(test.nodes, 2)

        self.assertEqual(test.counterNodes, [1, 2, 3])
        self.assertNotEqual(test.counterNodes, [2, 3, 4])

    def test_formation_finder_find_best_formation_1(self):
        weightStates = [WeightState(1, 1), WeightState(2, 2), WeightState(3, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(sorted(result), ([1, 2]))

    def test_formation_finder_find_best_formation_2(self):
        weightStates = [WeightState(1, 1), WeightState(2, 2), WeightState(3, 4)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(result, [3])

    def test_formation_finder_find_best_formation_3(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2), WeightState(3, 3)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(sorted(result), sorted([1, 2]))

    def test_formation_finder_find_best_formation_test_priority_1(self):
        weightStates = [WeightState(46, 1), WeightState(45, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(result, [45])

    def test_formation_finder_find_best_formation_test_priority_2(self):
        weightStates = [WeightState(46, 200), WeightState(45, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(result, [45])

    def test_formation_finder_find_best_formation_test_priority_3(self):
        weightStates = [WeightState(8, 200), WeightState(42, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(result, [42])

    def test_formation_finder_find_best_formation_test_priority_4(self):
        weightStates = [WeightState(36, 200), WeightState(35, 200), WeightState(42, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(result, [42])

    def test_formation_finder_find_best_formation_test_priority_5(self):
        weightStates = [WeightState(5, 200), WeightState(42, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(sorted(result), sorted([5, 42]))

    def test_formation_finder_find_best_formation_test_priority_4(self):
        weightStates = [WeightState(36, 200), WeightState(42, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        self.assertEqual(result, [42])

    # Helper method to validate a formation
    def _test_formation(self, formationFinder, formation):
        blocked  = []

        for r in formation:
            found = [x for x in formationFinder._formations if r in x.nodes][0]
            blocked = blocked + found.counterNodes

        for r in formation:
            found = [x for x in blocked if x == r]
            if len(found) > 0: self.fail('Overlapping nodes: ' + str(r) + ' for ' + str(found))

    def test_formation_calculate_complimentary_1(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2)]
        formationFinder = FormationFinder()

        result = formationFinder._calculate_complimentary(weightStates, [1])
        self._test_formation(formationFinder, result)

    def test_formation_calculate_complimentary_2(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2), WeightState(5, 3)]
        formationFinder = FormationFinder()

        result = formationFinder._calculate_complimentary(weightStates, [1])
        self._test_formation(formationFinder, result)

    def test_formation_calculate_complimentary_3(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2), WeightState(42, 3)]
        formationFinder = FormationFinder()

        result = formationFinder._calculate_complimentary(weightStates, [1])
        self._test_formation(formationFinder, result)

    def test_formation_finder_find_subsets_1(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2)]
        formationFinder = FormationFinder()
        result = formationFinder._find_subsets(weightStates)
        
        expected = [[1], [2], [1, 2]]
        self.assertEqual(result, expected)

    def test_formation_finder_find_subsets_1(self):
        weightStates = [WeightState(1, 2), WeightState(2, 20)]
        formationFinder = FormationFinder()
        result = formationFinder._find_subsets(weightStates)
        
        expected = [[1], [2], [1, 2]]
        self.assertEqual(result, expected)

    def test_formation_finder_calculate_subset_weight(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2)]
        subsets = [[1], [2], [1, 2]]

        formationFinder = FormationFinder()
        weightedSubsets = formationFinder._calculate_subset_weight(subsets, weightStates)
        
        self.assertEqual(weightedSubsets[0].weight, 4)
        self.assertEqual(weightedSubsets[0].node, [1, 2])

if __name__ == '__main__':
    unittest.main(exit=False)
