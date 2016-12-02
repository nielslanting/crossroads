import unittest
import re

from weightstate import WeightState 

class TestWeightState(unittest.TestCase):

    def test_weight_state_constructor(self):
        test = WeightState(1, 5)

        self.assertEqual(test.node, 1)
        self.assertEqual(test.weight, 5)

    def test_weight_state_constructor_2(self):
        test = WeightState(40, 0)

        self.assertEqual(test.node, 40)
        self.assertEqual(test.weight, 0)

    def test_weight_state_constructor_priority_1(self):
        low = WeightState(1, 5)
        high = WeightState(42, 5)

        self.assertGreater(high, low)

    def test_weight_state_constructor_priority_1(self):
        low = WeightState(42, 5)
        high = WeightState(45, 5)

        self.assertGreater(high, low)

if __name__ == '__main__':
    unittest.main(exit=False)
