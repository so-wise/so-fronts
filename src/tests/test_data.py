"""Tests for data-loading path and naming helpers."""
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import xarray as xr

import src.constants as cst
import src.data_loading.io_names as io


class TestDataLoading(unittest.TestCase):
    """Unit tests for path naming and loading helpers."""

    def test_constants_paths_do_not_duplicate_segments(self):
        """Resolved constants should avoid duplicated path segments."""
        norm_salt = cst.SALT_FILE.replace("\\", "/")
        self.assertTrue(norm_salt.startswith(cst.BSOSE_PATH.replace("\\", "/")))
        self.assertNotIn("/nc/nc/", norm_salt)
        self.assertNotIn("/bsose_stuv/bsose_stuv/", norm_salt)

    def test_return_name_uses_data_path(self):
        """return_name should always anchor output under DATA_PATH."""
        expected = os.path.join(cst.DATA_PATH, "i-metric-joint-k-5-d-3")
        self.assertEqual(io.return_name(5, 3), expected)

    def test_return_folder_creates_directory(self):
        """return_folder creates and returns a run-specific data directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_root = os.path.join(tmp_dir, "nc")
            with patch.object(io.cst, "DATA_PATH", data_root):
                folder = io.return_folder(k_clusters=2, pca_components=4)
                self.assertTrue(folder.startswith(data_root))
                self.assertTrue(folder.endswith(os.sep))
                self.assertTrue(os.path.isdir(folder))

    def test_return_plot_folder_creates_directory(self):
        """return_plot_folder creates and returns a figure output folder."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.object(io.cst, "FIGURE_PATH", tmp_dir):
                folder = io.return_plot_folder(k_clusters=2, pca_components=3)
                self.assertTrue(folder.startswith(tmp_dir))
                self.assertTrue(folder.endswith(os.sep))
                self.assertTrue(os.path.isdir(folder))

    def test_return_pair_i_metric_save_nc_true_uses_pair_metric(self):
        """save_nc=True should call pair_i_metric on the selected time slice."""
        base_ds = MagicMock()
        sliced_ds = object()
        base_ds.isel.return_value = sliced_ds
        expected_da = xr.DataArray([1.0], dims=["dummy"])

        with patch.object(io, "return_name", return_value="/tmp/joint-path"):
            with patch.object(io.xr, "open_dataset", return_value=base_ds) as open_mock:
                with patch.object(io.tpi, "pair_i_metric", return_value=expected_da) as pair_mock:
                    actual = io.return_pair_i_metric(
                        k_clusters=5,
                        pca=3,
                        save_nc=True,
                        t_index=7,
                    )

        self.assertIs(actual, expected_da)
        open_mock.assert_called_once_with("/tmp/joint-path.nc")
        base_ds.isel.assert_called_once_with(time=slice(7, 9))
        pair_mock.assert_called_once_with(sliced_ds, threshold=0.05)

    def test_return_pair_i_metric_save_nc_false_loads_pair_file(self):
        """save_nc=False should load from the pair netcdf naming helper."""
        base_ds = MagicMock()
        pair_ds = MagicMock()
        expected_da = xr.DataArray([42.0], dims=["dummy"])
        pair_ds.to_array.return_value.isel.return_value = expected_da

        with patch.object(io, "return_name", return_value="/tmp/joint-path"):
            with patch.object(io, "_return_pair_name", return_value="/tmp/pair-path"):
                with patch.object(
                    io.xr,
                    "open_dataset",
                    side_effect=[base_ds, pair_ds],
                ) as open_mock:
                    actual = io.return_pair_i_metric(
                        k_clusters=5,
                        pca=3,
                        save_nc=False,
                        t_index=3,
                    )

        self.assertIs(actual, expected_da)
        self.assertEqual(open_mock.call_count, 2)
        pair_ds.to_array.return_value.isel.assert_called_once_with(time=slice(3, 5))


suite = unittest.TestLoader().loadTestsFromTestCase(TestDataLoading)
