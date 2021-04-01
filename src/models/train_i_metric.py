import os
import numpy as np
import xarray as xr
import pyxpcm
from pyxpcm.models import pcm
import src.constants as cst


xr.set_options(keep_attrs=True)


def train_on_interpolated_year(
    time_i: int = 42,
    K: int = 5,
    maxvar: int = 3,
    min_depth: float = 300,
    max_depth: float = 2000,
    separate_pca: bool = True,
    remove_init_var: bool = True,
):
    """
    Put Seed in the CONSTANTS file.

    """

    z = np.arange(-min_depth, -max_depth, -10.0)
    features_pcm = {}
    for var in cst.VAR_NAME_LIST:
        features_pcm[var] = z
    features = cst.FEATURES_D
    fname = cst.INTERP_FILE_NAME
    if not os.path.isfile(fname):
        salt_nc = xr.open_dataset(cst.SALT_FILE).isel(time=slice(time_i, time_i + 12))
        theta_nc = xr.open_dataset(cst.THETA_FILE).isel(time=slice(time_i, time_i + 12))
        big_nc = xr.merge([salt_nc, theta_nc])
        both_nc = big_nc.where(big_nc.coords[cst.DEPTH_NAME] > max_depth).drop(
            cst.USELESS_LIST
        )

        lons_new = np.linspace(both_nc.XC.min(), both_nc.XC.max(), 60 * 4)
        lats_new = np.linspace(both_nc.YC.min(), both_nc.YC.max(), 60)

        ds = both_nc.interp(
            coords={cst.Y_COORD: lats_new, cst.X_COORD: lons_new}
        )  # , method='cubic')
        ds.to_netcdf(fname)
    else:
        ds = xr.open_dataset(fname)

    m = pcm(
        K=K,
        features=features_pcm,
        separate_pca=separate_pca,
        maxvar=maxvar,
        timeit=True,
        timeit_verb=1,
    )

    m.fit(ds, features=features, dim=cst.Z_COORD)
    m.add_pca_to_xarray(ds, features=features, dim=cst.Z_COORD, inplace=True)
    m.find_i_metric(ds, inplace=True)
    m.predict(ds, features=features, dim=cst.Z_COORD, inplace=True)

    del ds.PCA_VALUES.attrs["_pyXpcm_cleanable"]
    del ds.IMETRIC.attrs["_pyXpcm_cleanable"]
    del ds.A_B.attrs["_pyXpcm_cleanable"]
    del ds.PCM_LABELS.attrs["_pyXpcm_cleanable"]

    if remove_init_var:
        ds = ds.drop(cst.VAR_NAME_LIST)

    return m, ds
