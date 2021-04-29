"""Label subplots. is the main function"""
from typing import Sequence, Union
import numpy as np
import pandas as pd
import matplotlib
import cftime
import src.time_wrapper as twr


@twr.timeit
def label_subplots(
    axs: Sequence[matplotlib.axes.Axes],
    labels: Sequence[str] = [chr(ord("`") + z) for z in range(1, 27)],
    start_from: int = 0,
    fontsize: int = 10,
    x_pos: float = 0.02,
    y_pos: float = 0.95,
) -> None:
    """Adds e.g. (a), (b), (c) at the top left of each subplot panel.

    Labelling order achieved through ravelling the input `list` or `np.array`.

    Args:
        axs (Sequence[matplotlib.axes.Axes]): `list` or `np.array` of
            `matplotlib.axes.Axes`.
        labels (Sequence[str]): A sequence of labels for the subplots.
        start_from (int, optional): skips first `start_from` labels. Defaults to 0.
        fontsize (int, optional): Font size for labels. Defaults to 10.
        x_pos (float, optional): Relative x position of labels. Defaults to 0.02.
        y_pos (float, optional): Relative y position of labels. Defaults to 0.95.

    Returns:
        void; alters the `matplotlib.axes.Axes` objects

    Example:
        Here is an example of using this function::
            >>> label_subplots(axs, start_from=0, fontsize=10)

    """
    if isinstance(axs, list):
        axs = np.asarray(axs)

    assert len(axs.ravel()) + start_from <= len(labels)
    subset_labels = []

    for i in range(len(axs.ravel())):
        subset_labels.append(labels[i + start_from])

    for i, label in enumerate(subset_labels):
        axs.ravel()[i].text(
            x_pos,
            y_pos,
            str("(" + label + ")"),
            color="black",
            transform=axs.ravel()[i].transAxes,
            fontsize=fontsize,
            fontweight="bold",
            va="top",
        )


def time_title(
    ax: matplotlib.axes.Axes,
    time: Union[np.datetime64, float, cftime.Datetime360Day],
    date_time_formatter: str = "%Y.%m.%d",
) -> None:
    """Add time title to axes.

    Args:
        ax (matplotlib.axes.Axes): axis to add title to.
        time (Union[np.datetime64, float, cftime.Datetime360Day]): time string.
        date_time_formatter (str, optional): Default is
    Example:
        Usage with an xarray.Datarray object::
            >>> time_title(ax, xr_da.time.values[index])
    """
    if isinstance(time, np.datetime64):
        # use pandas to format time
        ax.set_title(pd.to_datetime(str(time)).strftime(date_time_formatter))
    elif isinstance(time, cftime.Datetime360Day):
        ax.set_title(time.strftime()[0:10])
    elif isinstance(time, (float, np.floating)):
        # It would be better to have this as an option
        ax.set_title("%2.1f months after 1960" % time)
    else:
        print(
            "!Warning!: input of type "
            + str(type(time))
            + " does not lead to title plotting."
        )
