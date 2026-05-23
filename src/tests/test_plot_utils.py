"""Tests for plot utilities."""
import unittest
from unittest.mock import patch

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import src.plot_utils.ellipses as ell
except ModuleNotFoundError:
    ell = None


class _DummyClassifier:
    covariances_ = np.array(
        [
            [[1.0, 0.0], [0.0, 2.0]],
            [[2.0, 0.1], [0.1, 3.0]],
        ]
    )
    weights_ = np.array([0.6, 0.4])
    means_ = np.array([[0.0, 0.0], [1.0, -1.0]])


class _DummyPCM:
    _classifier = _DummyClassifier()


@unittest.skipIf(ell is None, "Optional dependency missing: pyxpcm")
class TestPlotUtilities(unittest.TestCase):
    """Unit tests for plotting utilities without GUI requirements."""

    def test_ellispes_adds_expected_number_of_patches(self):
        """Each cluster should add 3 ellipses to the axes."""
        fig, ax = plt.subplots()
        try:
            with patch.object(ell.gp, "label_subplots") as label_mock:
                ell.ellispes(_DummyPCM(), ax)
        finally:
            plt.close(fig)

        self.assertEqual(len(ax.patches), 6)
        self.assertEqual(label_mock.call_count, 6)


suite = unittest.TestLoader().loadTestsFromTestCase(TestPlotUtilities)
