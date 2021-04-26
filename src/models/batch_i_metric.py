"""Make i metric in a batch."""
import xarray as xr
import pyxpcm
import src.constants as cst
import src.data_loading.io_name_conventions as io
import src.train_pyxpcm as tim

xr.set_options(keep_attrs=True)


def pca_from_interpolated_year(
    pcm_object: pyxpcm.pcm,
    pca: int = cst.D_COORD,
    k_clusters: int = cst.K_CLUSTERS,
    time_i: int = cst.EXAMPLE_TIME_INDEX,
    max_depth: float = cst.MAX_DEPTH,
    remove_init_var: bool = True,
) -> None:
    """
    pcm_object: the pcm object which has already been trained
    pca: how many principal components were chosen to be fitted.
    k_clusters: how many Guassians were fitted.
    max_depth: the maximum_depth (in pcm_object) that the data is fitted to.
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
    ds = pcm_object.find_i_metric(ds, inplace=True)
    ds = pcm_object.add_pca_to_xarray(
        ds, features=cst.FEATURES_D, dim=cst.Z_COORD, inplace=True
    )

    def sanitize() -> None:
        del ds.IMETRIC.attrs["_pyXpcm_cleanable"]
        del ds.A_B.attrs["_pyXpcm_cleanable"]
        del ds.PCA_VALUES.attrs["_pyXpcm_cleanable"]

    sanitize()

    for coord in attr_d:
        ds.coords[coord].attrs = attr_d[coord]

    if remove_init_var:
        ds = ds.drop(cst.VAR_NAME_LIST)

    ds = ds.expand_dims(dim=cst.T_COORD, axis=None)
    ds = ds.assign_coords(
        {cst.T_COORD: (cst.T_COORD, [salt_nc.coords[cst.T_COORD].values])}
    )
    ds.coords[cst.T_COORD].attrs = salt_nc.coords[cst.T_COORD].attrs
    ds.to_netcdf(
        io.return_folder(k_clusters, pca) + str(time_i) + ".nc", format="NETCDF4"
    )


def run_through_sep(k_clusters: int = cst.K_CLUSTERS, pca: int = cst.D_PCS) -> None:
    """
    Run through joint.

    Args:
        k_clusters (int, optional): [description]. Defaults to 5.
        pca (int, optional): [description]. Defaults to 3.
    """
    pcm_object, _ = tim.train_on_interpolated_year(
        time_i=cst.EXAMPLE_TIME_INDEX,
        k_clusters=k_clusters,
        maxvar=pca,
        min_depth=cst.MIN_DEPTH,
        max_depth=cst.MAX_DEPTH,
        separate_pca=False,
    )
    for time_i in range(60):
        pca_from_interpolated_year(
            pcm_object, k_clusters=k_clusters, pca=pca, time_i=time_i
        )


def merge_and_save(k_clusters: int = 5, pca: int = 3) -> None:
    """Merge and save joint."""

    pca_ds = xr.open_mfdataset(
        io.return_folder(k_clusters, pca) + "*.nc",
        concat_dim=cst.T_COORD,
        combine="by_coords",
        chunks={cst.T_COORD: 1},
        data_vars="minimal",
        coords="minimal",
        compat="override",
    )
    xr.save_mfdataset(
        [pca_ds], [io.return_name(k_clusters, pca) + ".nc"], format="NETCDF4"
    )


def run_through() -> None:
    """Run through."""
    k_list = [4, 2, 10]
    for k_clusters in k_list:
        run_through_sep(k_clusters=k_clusters)
    for k_clusters in k_list:
        merge_and_save(k_clusters=k_clusters)
