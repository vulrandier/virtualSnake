from unittest import TestCase
from main import Position


class TestPosition(TestCase):
    def test_equal(self):
        pos1_a = Position(0, 0)
        pos1_b = Position(0, 0)
        pos2_a = Position(1, 9)
        pos2_b = Position(1, 9)
        pos3_a = Position(2, 6)
        pos3_b = Position(2, 6)
        pos4_a = Position(18, 21)
        pos4_b = Position(18, 21)

        self.assertEqual(pos1_a,pos1_b)
        self.assertEqual(pos2_a,pos2_b)
        self.assertEqual(pos3_a,pos3_b)
        self.assertEqual(pos4_a,pos4_b)
