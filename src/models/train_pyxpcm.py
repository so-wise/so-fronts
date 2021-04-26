"""Train i metric.

Example:
    To test::
        python3 src/models/train_pyxpcm.py
"""
import os
from typing import Tuple
import numpy as np
import xarray as xr
import pyxpcm
from pyxpcm.models import pcm
import src.constants as cst
import src.time_wrapper as twr

xr.set_options(keep_attrs=True)


@twr.timeit
def train_on_interpolated_year(
    time_i: int = cst.EXAMPLE_TIME_INDEX,
    k_clusters: int = cst.K_CLUSTERS,
    maxvar: int = cst.D_PCS,
    min_depth: float = cst.MIN_DEPTH,
    max_depth: float = cst.MAX_DEPTH,
    remove_init_var: bool = True,
    separate_pca: bool = False,
    interp: bool = False,
    remake: bool = True,
) -> Tuple[pyxpcm.pcm, xr.Dataset]:
    """Train on interpolated year.

    Args:
        time_i (int, optional): time index. Defaults to cst.EXAMPLE_TIME_INDEX.
        k_clusters (int, optional): clusters. Defaults to cst.K_CLUSTERS.
        maxvar (int, optional): num pca. Defaults to cst.D_PCS.
        min_depth (float, optional): minimum depth for column.
            Defaults to cst.MIN_DEPTH.
        max_depth (float, optional): maximum depth for column.
            Defaults to cst.MAX_DEPTH.
        separate_pca (bool, optional): separate the pca. Defaults to True.
        remove_init_var (bool, optional): remove initial variables. Defaults to True.

    Returns:
        Tuple[pyxpcm.pcm, xr.Dataset]: the fitted object and its corresponding dataset.

    """
    z = np.arange(-min_depth, -max_depth, -10.0)
    features_pcm = {}
    for var in cst.VAR_NAME_LIST:
        features_pcm[var] = z
    features = cst.FEATURES_D
    fname = cst.INTERP_FILE_NAME
    if not os.path.isfile(fname) or remake is True:
        if os.path.isfile(fname):
            os.remove(fname)
        print("going to save to: ", fname)
        salt_nc = xr.open_dataset(cst.SALT_FILE).isel(time=slice(time_i, time_i + 12))
        theta_nc = xr.open_dataset(cst.THETA_FILE).isel(time=slice(time_i, time_i + 12))
        big_nc = xr.merge([salt_nc, theta_nc])
        both_nc = big_nc.where(big_nc.coords[cst.DEPTH_NAME] > max_depth).drop(
            cst.USELESS_LIST
        )
        if interp:
            mult_fact = 2
            lons_new = np.linspace(
                both_nc.XC.min(), both_nc.XC.max(), 60 * 4 * mult_fact
            )
            lats_new = np.linspace(both_nc.YC.min(), both_nc.YC.max(), 60 * mult_fact)
            ds = both_nc.interp(coords={cst.Y_COORD: lats_new, cst.X_COORD: lons_new})
        else:
            ds = both_nc
        ds.to_netcdf(fname)
    else:
        ds = xr.open_dataset(fname)

    pcm_object = pcm(
        K=k_clusters,
        features=features_pcm,
        separate_pca=separate_pca,
        maxvar=maxvar,
        timeit=True,
        timeit_verb=1,
    )

    pcm_object.fit(ds, features=features, dim=cst.Z_COORD)
    pcm_object.add_pca_to_xarray(ds, features=features, dim=cst.Z_COORD, inplace=True)
    pcm_object.find_i_metric(ds, inplace=True)
    pcm_object.predict(ds, features=features, dim=cst.Z_COORD, inplace=True)

    del ds.PCA_VALUES.attrs["_pyXpcm_cleanable"]
    del ds.IMETRIC.attrs["_pyXpcm_cleanable"]
    del ds.A_B.attrs["_pyXpcm_cleanable"]
    del ds.PCM_LABELS.attrs["_pyXpcm_cleanable"]

    if remove_init_var:
        ds = ds.drop(cst.VAR_NAME_LIST)

    # Tuple[pyxpcm.pcm, xr.Dataset]
    return pcm_object, ds


if __name__ == "__main__":
    train_on_interpolated_year()
