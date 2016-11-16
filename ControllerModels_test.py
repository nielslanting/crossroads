import unittest
import re

from ControllerModels import State, NodeState, LightState

class TestControllerModels(unittest.TestCase):
    
    # TODO: Test obserable logic

    def test_node_state_constructor(self):
        test = NodeState(1, LightState.red)

        self.assertEqual(1, test.trafficLight)
        self.assertNotEqual(2, test.trafficLight)

        self.assertEqual(LightState.red.name, test.status)
        self.assertNotEqual(LightState.orange.name, test.status)
        self.assertNotEqual(LightState.green.name, test.status)

    def test_node_state_equal(self):
        a = NodeState(1, LightState.red)
        b = NodeState(1, LightState.red)
        c = NodeState(2, LightState.orange)

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, c)

    def test_state_constructor(self):
        expected = [1, 2, 3]
        unexpected = [4, 2, 3]
        test = State(expected)

        self.assertEqual(test.get(), expected)
        self.assertNotEqual(test.get(), unexpected)

    def test_state_equal(self):
        a = State([1, 2, 3])
        b = State([1, 2, 3])
        c = State([4, 2, 3])

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, c)

    def test_state_to_json_simple(self):
        inputArguments = [1, 2, 3]

        test = State(inputArguments)
        result = re.sub("[\s+]", "", test.toJSON())
        expected = unicode('{"state":[1,2,3]}', 'utf-8')

        self.assertEqual(result, expected)

    def test_state_to_json_advance(self):
        inputArguments = [NodeState(1, LightState.green)]

        test = State(inputArguments)
        result = re.sub("[\s+]", "", test.toJSON())
        expected = unicode('{"state":[{"status":"green","trafficLight":1}]}', 'utf-8')

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
