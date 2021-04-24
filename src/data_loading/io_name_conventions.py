"""Defaults for naming files."""
import os


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
