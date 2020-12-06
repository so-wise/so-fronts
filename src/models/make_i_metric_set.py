import xarray as xr
import pyxpcm
from pyxpcm.models import pcm

xr.set_options(keep_attrs=True)


def pca_from_interpolated_year(m, pca=2, K=5, time_i=42, max_depth=2000):

    main_dir = "/Users/simon/bsose_monthly/"
    salt = main_dir + "bsose_i106_2008to2012_monthly_Salt.nc"
    theta = main_dir + "bsose_i106_2008to2012_monthly_Theta.nc"
    features = {"THETA": "THETA", "SALT": "SALT"}

    salt_nc = xr.open_dataset(salt).isel(time=time_i)
    theta_nc = xr.open_dataset(theta).isel(time=time_i)
    big_nc = xr.merge([salt_nc, theta_nc])
    both_nc = big_nc.where(big_nc.coords["Depth"] > max_depth).drop(
        ["iter", "Depth", "rA", "drF", "hFacC"]
    )

    attr_d = {}

    for coord in both_nc.coords:
        attr_d[coord] = both_nc.coords[coord].attrs

    ds = both_nc

    ds = m.find_i_metric(ds, inplace=True)

    ds = m.add_pca_to_xarray(ds, features=features, dim="Z", inplace=True)

    def sanitize():
        del ds.IMETRIC.attrs["_pyXpcm_cleanable"]
        del ds.A_B.attrs["_pyXpcm_cleanable"]
        del ds.PCA_VALUES.attrs["_pyXpcm_cleanable"]

    for coord in attr_d:
        ds.coords[coord].attrs = attr_d[coord]

    sanitize()

    ds = ds.drop(["SALT", "THETA"])

    ds = ds.expand_dims(dim="time", axis=None)

    ds = ds.assign_coords({"time": ("time", [salt_nc.coords["time"].values])})

    ds.coords["time"].attrs = salt_nc.coords["time"].attrs

    ds.to_netcdf(_return_folder(K, pca) + str(time_i) + ".nc", format="NETCDF4")

    # return ds


@timeit
def run_through_joint_two(K=5, pca=3):
    m, ds = train_on_interpolated_year(
        time_i=42, K=K, maxvar=pca, min_depth=300, max_depth=2000, separate_pca=False
    )

    # m.to_netcdf('nc/pc-joint-m.nc')

    for time_i in range(60):
        pca_from_interpolated_year(m, K=K, pca=pca, time_i=time_i)


# run_through_joint_two()


def merge_and_save_joint(K=5, pca=3):

    pca_ds = xr.open_mfdataset(
        _return_folder(K, pca) + "*.nc",
        concat_dim="time",
        combine="by_coords",
        chunks={"time": 1},
        data_vars="minimal",
        # parallel=True,
        coords="minimal",
        compat="override",
    )  # this is too intense for memory

    xr.save_mfdataset([pca_ds], [_return_name(K, pca) + ".nc"], format="NETCDF4")


def run_through():
    K_list = [4, 2, 10]
    for K in K_list:
        run_through_joint_two(K=K)
    for K in K_list:
        merge_and_save_joint(K=K)
