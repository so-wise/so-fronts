"""Defaults for naming files."""
import os
import xarray as xr
import src.constants as cst
import src.time_wrapper as twr
import src.models.to_pair_i_metric as tpi


@twr.timeit
def return_pair_i_metric(
    k_clusters: int = cst.K_CLUSTERS, pca: int = cst.D_PCS, save_nc: bool = True
) -> xr.DataArray:
    """Return pair i metric.

    Args:
        k_clusters (int, optional): Number of
               clusters. Defaults to cst.K_CLUSTERS.
        pca (int, optional): Number of principal components. Defaults to cst.D_PCS.
        save_nc (bool, optional): Whether or not to save the resulting dataset.
            Defaults to True.

    Returns:
        xr.DataArray: pair i metric.
    """
    link_to_netcdf = _return_name(k_clusters, pca) + ".nc"
    ds = xr.open_dataset(link_to_netcdf)
    print(ds.__str__())
    batch_size = 2
    for i in range(cst.EXAMPLE_TIME_INDEX, cst.EXAMPLE_TIME_INDEX + 2, batch_size):
        print("running", i)
        if save_nc:
            da = tpi.pair_i_metric(
                ds.isel(time=slice(i, i + batch_size)), threshold=0.05
            )
            print("not saving")
        else:
            da = (
                xr.open_dataset(_return_pair_name(k_clusters, pca) + "..nc")
                .to_array()
                .isel(time=slice(i, i + batch_size))
            )

    return da


def _return_name(k_clusters: int, pca_components: int) -> str:
    """Return name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.
    """
    return (
        "../pyxpcm_sithom/nc/i-metric-joint-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
    )


def _return_plot_folder(k_clusters: int, pca_components: int) -> str:
    """Return plot folder name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.
    """
    folder = (
        "../FBSO-Report/images/i-metric-joint-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
        + "/"
    )
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_folder(k_clusters: int, pca_components: int) -> str:
    """Return return folder name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.

    """
    folder = _return_name(k_clusters, pca_components) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_pair_name(k_clusters: int, pca_components: int) -> str:
    """Return pair name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.

    """
    return (
        "../pyxpcm_sithom/"
        + "nc/pair-i-metric-k-"
        + str(k_clusters)
        + "-d-"
        + str(pca_components)
    )


def _return_pair_folder(k_clusters: int, pca_components: int) -> str:
    """Return pair folder name.

    Args:
        k_clusters (int): The number of classes.
        pca_components (int): The number of pcas.

    Returns:
        str: file names.

    """
    folder = "nc/pair-i-metric-k-" + str(k_clusters) + "-d-" + str(pca_components) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
