import xarray as xr
import pyxpcm
from pyxpcm.models import pcm
import src.constants as cst
import src.data_loading.io_name_conventions as io
import src.train_i_metric as tim

xr.set_options(keep_attrs=True)


def pca_from_interpolated_year(
    m, pca=2, K=5, time_i=42, max_depth=2000, remove_init_var=True
):
    """
    m: the pcm object which has already been trained
    pca: how many principal components were chosen to be fitted.
    K: how many Guassians were fitted.
    max_depth: the maximum_depth (in m) that the data is fitted to.
    """

    salt_nc = xr.open_dataset(cst.SALT_FILE).isel(time=time_i)
    theta_nc = xr.open_dataset(cst.THETA_FILE).isel(time=time_i)
    big_nc = xr.merge([salt_nc, theta_nc])
    both_nc = big_nc.where(big_nc.coords[cst.DEPTH_NAME] > max_depth).drop(
        cst.USELESS_LIST
    )

    attr_d = {}

    for coord in both_nc.coords:
        attr_d[coord] = both_nc.coords[coord].attrs

    ds = both_nc

    ds = m.find_i_metric(ds, inplace=True)

    ds = m.add_pca_to_xarray(ds, features=cst.FEATURES_D, dim=cst.Z_COORD, inplace=True)

    def sanitize():
        del ds.IMETRIC.attrs["_pyXpcm_cleanable"]
        del ds.A_B.attrs["_pyXpcm_cleanable"]
        del ds.PCA_VALUES.attrs["_pyXpcm_cleanable"]

    sanitize()

    for coord in attr_d:
        ds.coords[coord].attrs = attr_d[coord]

    if remove_init_var:
        ds = ds.drop(cst.VAR_NAME_LIST)

    ds = ds.expand_dims(dim=cst.TIME_NAME, axis=None)

    ds = ds.assign_coords(
        {cst.TIME_NAME: (cst.TIME_NAME, [salt_nc.coords[cst.TIME_NAME].values])}
    )

    ds.coords[cst.TIME_NAME].attrs = salt_nc.coords[cst.TIME_NAME].attrs

    ds.to_netcdf(io._return_folder(K, pca) + str(time_i) + ".nc", format="NETCDF4")

    # return ds


def run_through_joint_two(K=5, pca=3):
    m, ds = tim.train_on_interpolated_year(
        time_i=42, K=K, maxvar=pca, min_depth=300, max_depth=2000, separate_pca=False
    )

    # m.to_netcdf('nc/pc-joint-m.nc')

    for time_i in range(60):
        pca_from_interpolated_year(m, K=K, pca=pca, time_i=time_i)


# run_through_joint_two()


def merge_and_save_joint(K=5, pca=3):

    pca_ds = xr.open_mfdataset(
        io._return_folder(K, pca) + "*.nc",
        concat_dim=cst.TIME_NAME,
        combine="by_coords",
        chunks={cst.TIME_NAME: 1},
        data_vars="minimal",
        # parallel=True,
        coords="minimal",
        compat="override",
    )  # this is too intense for memory

    xr.save_mfdataset([pca_ds], [io._return_name(K, pca) + ".nc"], format="NETCDF4")


def run_through():
    K_list = [4, 2, 10]
    for K in K_list:
        run_through_joint_two(K=K)
    for K in K_list:
        merge_and_save_joint(K=K)
