import os
import numpy as np
import xarray as xr
import pyxpcm
from pyxpcm.models import pcm

xr.set_options(keep_attrs=True)


def train_on_interpolated_year(
    time_i=42,
    K=5,
    maxvar=3,
    min_depth=300,
    max_depth=2000,
    separate_pca=True,
    remove_s_and_t=True,
):
    """
    TODO: Stop hard coding file locations
    """

    main_dir = "/Users/simon/bsose_monthly/"
    salt = main_dir + "bsose_i106_2008to2012_monthly_Salt.nc"
    theta = main_dir + "bsose_i106_2008to2012_monthly_Theta.nc"

    z = np.arange(-min_depth, -max_depth, -10.0)
    features_pcm = {"THETA": z, "SALT": z}
    features = {"THETA": "THETA", "SALT": "SALT"}
    fname = "nc/interp.nc"
    if not os.path.isfile(fname):
        salt_nc = xr.open_dataset(salt).isel(time=slice(time_i, time_i + 12))
        theta_nc = xr.open_dataset(theta).isel(time=slice(time_i, time_i + 12))
        big_nc = xr.merge([salt_nc, theta_nc])
        both_nc = big_nc.where(big_nc.coords["Depth"] > max_depth).drop(
            ["iter", "Depth", "rA", "drF", "hFacC"]
        )

        lons_new = np.linspace(both_nc.XC.min(), both_nc.XC.max(), 60 * 4)
        lats_new = np.linspace(both_nc.YC.min(), both_nc.YC.max(), 60)

        ds = both_nc.interp(
            coords={"YC": lats_new, "XC": lons_new}
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

    m.fit(ds, features=features, dim="Z")

    m.add_pca_to_xarray(ds, features=features, dim="Z", inplace=True)

    m.find_i_metric(ds, inplace=True)
    m.predict(ds, features=features, dim="Z", inplace=True)

    del ds.PCA_VALUES.attrs["_pyXpcm_cleanable"]
    del ds.IMETRIC.attrs["_pyXpcm_cleanable"]
    del ds.A_B.attrs["_pyXpcm_cleanable"]
    del ds.PCM_LABELS.attrs["_pyXpcm_cleanable"]

    if remove_s_and_t:
        ds = ds.drop(["THETA", "SALT"])

    return m, ds
