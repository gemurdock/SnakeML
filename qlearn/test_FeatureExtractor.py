import unittest
from FeatureExtractor import convert_ai_dir_choice
from lib.Direction import Direction, AIDirectionChoice


class TestFeatureExtractor(unittest.TestCase):

    def test_convert_ai_dir_choice(self):
        self.assertEqual(convert_ai_dir_choice(Direction.UP, AIDirectionChoice.FORWARD), Direction.UP)
        self.assertEqual(convert_ai_dir_choice(Direction.UP, AIDirectionChoice.LEFT), Direction.LEFT)
        self.assertEqual(convert_ai_dir_choice(Direction.UP, AIDirectionChoice.RIGHT), Direction.RIGHT)

        self.assertEqual(convert_ai_dir_choice(Direction.RIGHT, AIDirectionChoice.FORWARD), Direction.RIGHT)
        self.assertEqual(convert_ai_dir_choice(Direction.RIGHT, AIDirectionChoice.LEFT), Direction.UP)
        self.assertEqual(convert_ai_dir_choice(Direction.RIGHT, AIDirectionChoice.RIGHT), Direction.DOWN)

        self.assertEqual(convert_ai_dir_choice(Direction.DOWN, AIDirectionChoice.FORWARD), Direction.DOWN)
        self.assertEqual(convert_ai_dir_choice(Direction.DOWN, AIDirectionChoice.LEFT), Direction.RIGHT)
        self.assertEqual(convert_ai_dir_choice(Direction.DOWN, AIDirectionChoice.RIGHT), Direction.LEFT)

        self.assertEqual(convert_ai_dir_choice(Direction.LEFT, AIDirectionChoice.FORWARD), Direction.LEFT)
        self.assertEqual(convert_ai_dir_choice(Direction.LEFT, AIDirectionChoice.LEFT), Direction.DOWN)
        self.assertEqual(convert_ai_dir_choice(Direction.LEFT, AIDirectionChoice.RIGHT), Direction.UP)
