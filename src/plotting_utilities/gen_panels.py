import numpy as np
import matplotlib
import src.time_wrapper as twr


@twr.timeit
def label_subplots(axs: matplotlib.axes.Axes, start_from: int = 0, fontsize: int = 13):
    """Label subplots.

    :param axs:
    """

    if isinstance(axs, list):
        axs = np.asarray(axs)

    orig_label_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    assert len(axs.ravel()) + start_from <= len(orig_label_list)
    subset_labels = []
    for i in range(len(axs.ravel())):
        subset_labels.append(orig_label_list[i + start_from])
    for i, label in enumerate(subset_labels):
        print(i, label)
        axs.ravel()[i].text(
            0.02,
            0.95,
            str("(" + label.lower() + ")"),
            color="black",
            transform=axs.ravel()[i].transAxes,
            fontsize=fontsize,
            fontweight="bold",
            va="top",
        )
