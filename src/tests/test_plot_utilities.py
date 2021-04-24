import unittest
from src.plotting_utilities.ellipses import plot_ellipsoid_test


class TestCase(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_ellipses(self):
        plot_ellipsoid_test()


suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
