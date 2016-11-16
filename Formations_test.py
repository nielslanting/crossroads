import unittest
import re

from Formations import Formation, FormationFinder
from WeightState import WeightState

class TestFormations(unittest.TestCase):

    def test_formation_constructor(self):
        test = Formation(1, [1, 2, 3])

        self.assertEqual(test.node, 1)
        self.assertNotEqual(test.node, 2)

        self.assertEqual(test.counterNodes, [1, 2, 3])
        self.assertNotEqual(test.counterNodes, [2, 3, 4])

    def test_formation_finder_find_best_formation_1(self):
        weightStates = [WeightState(1, 1), WeightState(2, 2), WeightState(3, 1)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        print 'result1: ' + str(result)
        self.assertEqual(result, [1, 2])

    def test_formation_finder_find_best_formation_2(self):
        weightStates = [WeightState(1, 1), WeightState(2, 2), WeightState(3, 3)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        print 'result2: ' + str(result)
        self.assertEqual(result, [3])

    def test_formation_finder_find_best_formation_3(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2), WeightState(3, 3)]
        formationFinder = FormationFinder()
        result = formationFinder.find_best_formation(weightStates)

        print 'result3: ' + str(result)
        self.assertEqual(result, [1, 2])
    
    def test_formation_finder_find_all_subsets(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2)]
        formationFinder = FormationFinder()
        result = formationFinder.find_all_subsets(weightStates)
        
        expected = [[1], [2], [1, 2]]
        self.assertEqual(result, expected)

    def test_formation_finder_calculate_subset_weight(self):
        weightStates = [WeightState(1, 2), WeightState(2, 2)]
        subsets = [[1], [2], [1, 2]]

        formationFinder = FormationFinder()
        weightedSubsets = formationFinder.calculate_subset_weight(subsets, weightStates)
        
        expected = [WeightState([1, 2], 4), WeightState([1], 2), WeightState([2], 2)]
        self.assertEqual(weightedSubsets, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
