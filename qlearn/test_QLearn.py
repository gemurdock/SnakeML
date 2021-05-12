import unittest
from QLearn import temporal_difference, new_quality


class TestQLearn(unittest.TestCase):

    def test_temporal_difference(self):
        reward = 2
        discount = 0.9
        self.assertEqual(temporal_difference(0, 0, reward, discount), 2)
        self.assertEqual(temporal_difference(2, 0, reward, discount), 3.8)
        self.assertEqual(temporal_difference(0, 2, reward, discount), 0)

    def test_new_quality(self):
        learn_rate = 0.9
        reward = 2
        discount = 0.9
        self.assertEqual(new_quality(0, 0, learn_rate, reward, discount), 1.8)
        self.assertEqual(new_quality(1.8, 0, learn_rate, reward, discount), 3.258)
        self.assertEqual(new_quality(2, 0, learn_rate, reward, discount), 3.42)
        self.assertEqual(new_quality(0, 2, learn_rate, reward, discount), 2)
