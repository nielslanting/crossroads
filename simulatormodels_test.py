import unittest
import re

from simulatormodels import SimulatorState, SimulatorNodeState

class TestSimulatorModels(unittest.TestCase):

    def test_simulator_node_state_constructor(self):
        test = SimulatorNodeState(1, 5)

        self.assertEqual(test.trafficLight, 1)
        self.assertNotEqual(test.trafficLight, 2)
        self.assertEqual(test.count, 5)
        self.assertNotEqual(test.count, 4)

    def test_simulator_state_constructor(self):
        expected = [1, 2, 3]
        unexpected = [4, 2, 3]

        test = SimulatorState(expected)

        self.assertEqual(test.get(), expected)
        self.assertNotEqual(test.get(), unexpected)

    def test_simulator_state_to_json_simple(self):
        inputArguments = [1, 2, 3]

        test = SimulatorState(inputArguments)
        result = re.sub("[\s+]", "", test.toJSON())
        expected = unicode('{"state":[1,2,3]}', 'utf-8')

        self.assertEqual(result, expected)

    def test_simulator_state_to_json_advance(self):
        inputArguments = [SimulatorNodeState(1, 2)]

        test = SimulatorState(inputArguments)
        result = re.sub("[\s+]", "", test.toJSON())
        expected = unicode('{"state":[{"count":2,"trafficLight":1}]}', 'utf-8')

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
