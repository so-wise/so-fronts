import os


def _return_name(K, pca):

    return "../pyxpcm/nc/i-metric-joint-k-" + str(K) + "-d-" + str(pca)


def _return_plot_folder(K, pca):
    folder = "../FBSO-Report/images/i-metric-joint-k-" + str(K) + "-d-" + str(pca) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_folder(K, pca):
    folder = _return_name(K, pca) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def _return_pair_name(K, pca):
    return "nc/pair-i-metric-k-" + str(K) + "-d-" + str(pca)


def _return_pair_folder(K, pca):
    folder = "nc/pair-i-metric-k-" + str(K) + "-d-" + str(pca) + "/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
