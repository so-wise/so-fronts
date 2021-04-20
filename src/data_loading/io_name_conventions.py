"""Defaults for naming files."""
import os


def _return_name(K: int, pca: int) -> str:
    """Return name.

    Args:
        K (int): The number of classes.
        pca (int): The number of pcas.

    Returns:
        str: file names.
    """
    return "../pyxpcm/nc/i-metric-joint-k-" + str(K) + "-d-" + str(pca)


def _return_plot_folder(K: int, pca: int) -> str:
    """Return name.

    Args:
        K (int): The number of classes.
        pca (int): The number of pcas.

    Returns:
        str: file names.
    """
    folder = "../FBSO-Report/images/i-metric-joint-k-" + str(K) + "-d-" + str(pca) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_folder(K: int, pca: int) -> str:
    """Return name.

    Args:
        K (int): The number of classes.
        pca (int): The number of pcas.

    Returns:
        str: file names.
    """
    folder = _return_name(K, pca) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_pair_name(K: int, pca: int) -> str:
    """Return name.

    Args:
        K (int): The number of classes.
        pca (int): The number of pcas.

    Returns:
        str: file names.
    """
    return "../pyxpcm/" + "nc/pair-i-metric-k-" + str(K) + "-d-" + str(pca)


def _return_pair_folder(K: int, pca: int) -> str:
    """Return name.

    Args:
        K (int): The number of classes.
        pca (int): The number of pcas.

    Returns:
        str: file names.
    """
    folder = "nc/pair-i-metric-k-" + str(K) + "-d-" + str(pca) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
