
import unittest
import numpy as np
from anscogorski import *


class TestAnscombe(unittest.TestCase):

    def test_mbih_valeu(self):
        """
        Example from Mbih & Valeu (2014) that demonstrates Anscombe paradox.
        """
        votes = np.array([
            [1, 1, 0],
            [0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 0, 1],
        ])

        # describe(votes)

        self.assertTrue(anscombe(votes))


class TestOstrogorski(unittest.TestCase):

    def test_simple(self):
        """
        Simple, unambiguous Ostrogorski paradox.
        (2 person is a little ambiguous)
        """
        votes = np.array([
            [1, 1, 0],
            [0, 1, 1],
            [0, 1, 0],
        ])

        # describe(votes)

        self.assertTrue(ostrogorski(votes))


if __name__ == '__main__':
    unittest.main()
