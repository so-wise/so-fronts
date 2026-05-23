"""Tests for model helpers."""
import unittest
from unittest.mock import patch

import numpy as np
import xarray as xr

import src.constants as cst
import src.models.make_pair_metric as mpm


class TestModels(unittest.TestCase):
    """Unit tests for pair-metric model utilities."""

    def _pair_metric_dataset(self) -> xr.Dataset:
        shared_coords = {
            cst.T_COORD: [0],
            cst.Y_COORD: [-61.0, -60.0],
            cst.X_COORD: [10.0, 20.0],
        }
        a_b_coords = {"rank": [0, 1], **shared_coords}
        i_metric_coords = {"Imetric": [0], **shared_coords}
        a_b = xr.DataArray(
            np.zeros((2, 1, 2, 2), dtype=np.int32),
            dims=["rank", cst.T_COORD, cst.Y_COORD, cst.X_COORD],
            coords=a_b_coords,
        )
        i_metric = xr.DataArray(
            np.zeros((1, 1, 2, 2), dtype=np.float32),
            dims=["Imetric", cst.T_COORD, cst.Y_COORD, cst.X_COORD],
            coords=i_metric_coords,
        )
        return xr.Dataset(
            {"A_B": a_b, "IMETRIC": i_metric},
            coords={"rank": [0, 1], "Imetric": [0], **shared_coords},
        )

    def test_make_one_pair_i_metric_applies_threshold(self):
        """Only matching pairs above threshold should be retained."""
        pair = np.array([0, 1])
        sorted_version = np.array(
            [
                [
                    [[0, 0], [1, 1]],
                    [[1, 1], [1, 0]],
                ]
            ]
        )
        i_metric = np.array([[[0.10, 0.01], [0.80, 0.70]]])

        returned_pair, pair_metric, has_points = mpm.make_one_pair_i_metric(
            pair,
            i_metric,
            sorted_version,
            threshold=0.05,
        )

        np.testing.assert_array_equal(returned_pair, pair)
        self.assertTrue(has_points)
        self.assertEqual(pair_metric.shape, (1, 2, 2))
        self.assertEqual(pair_metric[0, 0, 0], 0.10)
        self.assertTrue(np.isnan(pair_metric[0, 0, 1]))

    def test_make_all_pair_i_metric_filters_empty_pairs(self):
        """Pairs without qualifying points should be excluded."""
        cart_prod = [np.array([0, 1]), np.array([1, 2])]
        sorted_version = np.array(
            [
                [
                    [[0, 0], [1, 1]],
                    [[1, 1], [1, 0]],
                ]
            ]
        )
        i_metric = np.array([[[0.10, 0.20], [0.30, 0.40]]])

        pair_metric_list, pair_list = mpm.make_all_pair_i_metric(
            cart_prod,
            i_metric,
            sorted_version,
            threshold=0.05,
        )

        self.assertEqual(len(pair_list), 1)
        np.testing.assert_array_equal(pair_list[0], np.array([0, 1]))
        self.assertEqual(len(pair_metric_list), 1)

    def test_pair_i_metric_builds_expected_output(self):
        """pair_i_metric should return expected dims and pair labels."""
        ds = self._pair_metric_dataset()
        sorted_version = np.array(
            [
                [
                    [[0, 1], [1, 0]],
                    [[1, 1], [0, 1]],
                ]
            ]
        )
        i_metric = np.ones((1, 2, 2), dtype=np.float32)
        pair_metric_values = np.ones((1, 2, 2), dtype=np.float32)

        with patch.object(
            mpm.xvl,
            "order_indexes",
            side_effect=[sorted_version, i_metric],
        ):
            with patch.object(
                mpm,
                "make_all_pair_i_metric",
                return_value=([pair_metric_values], [np.array([0, 1])]),
            ) as make_all_mock:
                da = mpm.pair_i_metric(ds, threshold=0.2)

        self.assertEqual(
            da.dims,
            (cst.P_COORD, cst.T_COORD, cst.Y_COORD, cst.X_COORD),
        )
        self.assertEqual(list(da.coords[cst.P_COORD].values), ["1 to 2"])
        np.testing.assert_array_equal(da.values[0], pair_metric_values)

        cart_prod = make_all_mock.call_args.args[0]
        self.assertEqual(len(cart_prod), 1)
        np.testing.assert_array_equal(cart_prod[0], np.array([0, 1]))


suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
