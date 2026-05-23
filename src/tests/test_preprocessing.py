"""Tests for preprocessing transformations."""
import os
import tempfile
import unittest
from unittest.mock import patch
from collections.abc import Hashable
from typing import Any

import numpy as np
import xarray as xr

import src.constants as cst

try:
    import src.preprocessing.gsw_transformations as _gsw_t
except ModuleNotFoundError:
    _gsw_t = None

gsw_t: Any = _gsw_t


@unittest.skipIf(_gsw_t is None, "Optional dependency missing: gsw")
class TestPreprocessing(unittest.TestCase):
    """Unit tests for preprocessing helpers and I/O wiring."""

    def _format_da(self) -> xr.DataArray:
        coords: dict[Hashable, list[float]] = {
            cst.T_COORD: [0, 1],
            cst.Y_COORD: [-61.0, -60.0],
            cst.X_COORD: [10.0, 20.0, 30.0],
        }
        da = xr.DataArray(
            np.ones((2, 2, 3), dtype=np.float32),
            dims=[cst.T_COORD, cst.Y_COORD, cst.X_COORD],
            coords=coords,
            name="THETA",
        )
        da.coords[cst.Y_COORD].attrs["units"] = "degree_north"
        return da

    def _density_ds(self) -> xr.Dataset:
        coords: dict[Hashable, list[float]] = {
            cst.T_COORD: [0.0],
            cst.Y_COORD: [-61.0, -60.0],
            cst.X_COORD: [10.0, 20.0, 30.0],
        }
        values = np.arange(6, dtype=np.float32).reshape(1, 2, 3)
        return xr.Dataset(
            {"Density": ([cst.T_COORD, cst.Y_COORD, cst.X_COORD], values)},
            coords=coords,
        )

    def test_create_datarray_preserves_dims_and_attrs(self):
        """create_datarray should preserve layout and attach attrs."""
        source_da = self._format_da()
        attrs = {"units": "kg m-3", "long_name": "Density"}

        out = gsw_t.create_datarray(
            format_dataarray=source_da,
            values=np.zeros((2, 2, 3), dtype=np.float32),
            name="Density",
            v_attr_d=attrs,
        )

        self.assertEqual(out.name, "Density")
        self.assertEqual(out.dims, source_da.dims)
        self.assertEqual(out.attrs["units"], "kg m-3")
        self.assertEqual(out.attrs["long_name"], "Density")
        self.assertEqual(out.coords[cst.Y_COORD].attrs["units"], "degree_north")

    def test_create_known_dataarray_rejects_unknown_name(self):
        """Unknown variable names should fail fast."""
        source_da = self._format_da()

        with self.assertRaises(AssertionError):
            gsw_t.create_known_dataarray(source_da, np.zeros((2, 2, 3)), "UNKNOWN")

    def test_reload_density_netcdf_uses_configured_path(self):
        """reload_density_netcdf should open DENSITY_NC_PATH exactly."""
        sentinel = object()
        with tempfile.TemporaryDirectory() as tmp_dir:
            density_path = os.path.join(tmp_dir, "density.nc")
            with patch.object(gsw_t, "DENSITY_NC_PATH", density_path):
                with patch.object(gsw_t.xr, "open_dataset", return_value=sentinel) as open_mock:
                    result = gsw_t.reload_density_netcdf()

        self.assertIs(result, sentinel)
        open_mock.assert_called_once_with(density_path)

    def test_create_whole_density_netcdf_writes_expected_files(self):
        """create_whole_density_netcdf should emit one rho file per time index."""
        salt_ds = xr.Dataset(coords={cst.T_COORD: [0, 1]})
        density_da = xr.DataArray(
            np.ones((2, 3), dtype=np.float32),
            dims=[cst.Y_COORD, cst.X_COORD],
            coords={cst.Y_COORD: [-61.0, -60.0], cst.X_COORD: [10.0, 20.0, 30.0]},
            name="Density",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.object(gsw_t, "RHO_DIR", tmp_dir):
                with patch.object(gsw_t.xr, "open_dataset", return_value=salt_ds):
                    with patch.object(
                        gsw_t,
                        "test_density_da",
                        return_value=(density_da, None, None, density_da),
                    ):
                        with patch.object(xr.DataArray, "to_netcdf", autospec=True) as to_nc_mock:
                            gsw_t.create_whole_density_netcdf()

        self.assertEqual(to_nc_mock.call_count, 2)
        written_paths = [call.args[1] for call in to_nc_mock.call_args_list]
        self.assertEqual(
            written_paths,
            [
                os.path.join(tmp_dir, "density_0.nc"),
                os.path.join(tmp_dir, "density_1.nc"),
            ],
        )

    def test_x_grad_saves_gradient_dataset(self):
        """x_grad should save only the x-gradient variable to density_grad_x.nc."""
        density_ds = self._density_ds()

        with tempfile.TemporaryDirectory() as tmp_dir:
            density_path = os.path.join(tmp_dir, "density.nc")
            with patch.object(gsw_t, "DENSITY_NC_PATH", density_path):
                with patch.object(gsw_t.cst, "DATA_PATH", tmp_dir):
                    with patch.object(gsw_t.xr, "open_mfdataset", return_value=density_ds):
                        with patch.object(gsw_t.xr, "save_mfdataset") as save_mock:
                            gsw_t.x_grad()

        self.assertEqual(save_mock.call_count, 1)
        saved_datasets, output_paths = save_mock.call_args.args
        self.assertEqual(output_paths, [os.path.join(tmp_dir, "density_grad_x.nc")])
        self.assertIn("x_grad", saved_datasets[0].data_vars)
        self.assertNotIn("Density", saved_datasets[0].data_vars)

    def test_y_grad_set_ok_false_uses_to_netcdf(self):
        """y_grad(set_ok=False) should write density_grad_y_da via to_netcdf."""
        density_ds = self._density_ds()

        with tempfile.TemporaryDirectory() as tmp_dir:
            density_path = os.path.join(tmp_dir, "density.nc")
            with patch.object(gsw_t, "DENSITY_NC_PATH", density_path):
                with patch.object(gsw_t.cst, "DATA_PATH", tmp_dir):
                    with patch.object(gsw_t.xr, "open_mfdataset", return_value=density_ds):
                        with patch.object(xr.DataArray, "to_netcdf", autospec=True) as to_nc_mock:
                            with patch.object(gsw_t.xr, "save_mfdataset") as save_mock:
                                gsw_t.y_grad(set_ok=False)

        self.assertEqual(to_nc_mock.call_count, 1)
        self.assertEqual(to_nc_mock.call_args.args[1], os.path.join(tmp_dir, "density_grad_y_da.nc"))
        self.assertEqual(to_nc_mock.call_args.kwargs["engine"], "netcdf4")
        save_mock.assert_not_called()

    def test_take_derivative_density_uses_dimension_in_filename(self):
        """take_derivative_density should encode the dimension in output filename."""
        density_ds = self._density_ds()

        with tempfile.TemporaryDirectory() as tmp_dir:
            density_path = os.path.join(tmp_dir, "density.nc")
            with patch.object(gsw_t, "DENSITY_NC_PATH", density_path):
                with patch.object(gsw_t.cst, "DATA_PATH", tmp_dir):
                    with patch.object(gsw_t.xr, "open_mfdataset", return_value=density_ds):
                        with patch.object(gsw_t.xr, "save_mfdataset") as save_mock:
                            gsw_t.take_derivative_density(dimension=cst.Y_COORD)

        saved_datasets, output_paths = save_mock.call_args.args
        expected_name = "Density_Gradient_" + cst.Y_COORD
        self.assertEqual(
            output_paths,
            [os.path.join(tmp_dir, "density_grad_" + cst.Y_COORD + ".nc")],
        )
        self.assertIn(expected_name, saved_datasets[0].data_vars)


suite = unittest.TestLoader().loadTestsFromTestCase(TestPreprocessing)
