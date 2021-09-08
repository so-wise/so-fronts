"""A program by sdat2 to plot the Southern Ocean with a variety of fronts.
   Currently plots Kim and Orsi 2014 (KO).

Usage:
    Example usage::
        ko.draw_fronts_kim(ax)

"""
import os
from typing import Tuple, List
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import src.plot_utils.latex_style as sps
import src.plot_utils.map as mp
import src.constants as cst


def is_too_far(
    lat_a: float = 0.0,
    lat_b: float = 0.0,
    lon_a: float = 0.0,
    lon_b: float = 0.0,
    max_allowable_square: float = 1.0,
) -> bool:
    """Check if points are too far apart to draw a line between.

    Args:
        lat_a (float, optional): [description]. Defaults to 0.0.
        lat_b (float, optional): [description]. Defaults to 0.0.
        lon_a (float, optional): [description]. Defaults to 0.0.
        lon_b (float, optional): [description]. Defaults to 0.0.
        max_allowable_square (float, optional): Max allowable square. Defaults to 1.

    Returns:
        bool: whether or not.
    """
    assert lat_a > -90
    assert lat_b > -90

    # I prefer positive longitudes
    if lon_a < 0:
        lon_a += 360
    if lon_b < 0:
        lon_b += 360

    # This will suppress line breaking at Greenwich meridian
    if lon_a > 360 - max_allowable_square and lon_b < max_allowable_square:
        return False
    elif lon_b > 360 - max_allowable_square and lon_a < max_allowable_square:
        return False
    else:
        return (lat_a - lat_b) ** 2 + (lon_a - lon_b) ** 2 > max_allowable_square


def split_into_list_of_lists(
    # pylint: disable=dangerous-default-value
    max_square: float = 1,
    # pylint: disable=dangerous-default-value
    list_of_xs: list = [0.0],
    # pylint: disable=dangerous-default-value
    list_of_ys: list = [0.0],
) -> Tuple[List[list], List[list]]:
    """
    Split into list of lists.

    Args:
        max_square (float, optional): [description]. Defaults to 1.
        list_of_xs (list, optional): [description]. Defaults to [0.0].
        list_of_ys (list, optional): [description]. Defaults to [0.0].

    Returns:
        Tuple[List[list], List[list]]: list of lists (lol) for Xs and Ys
    """
    lol_xs = [[list_of_xs[0]]]
    lol_ys = [[list_of_ys[0]]]
    index_lists = 0

    for i in range(len(list_of_xs) - 1):
        if is_too_far(
            lon_a=list_of_xs[i],
            lon_b=list_of_xs[i + 1],
            lat_a=list_of_ys[i],
            lat_b=list_of_ys[i + 1],
            max_allowable_square=max_square,
        ):
            index_lists += 1
            lol_xs.append([])
            lol_ys.append([])

        lol_ys[index_lists].append(list_of_ys[i + 1])
        lol_xs[index_lists].append(list_of_xs[i + 1])

    return lol_xs, lol_ys


def plot_list_of_lists(
    ax: matplotlib.axes.Axes,
    # pylint: disable=dangerous-default-value
    lol_of_xs: List[list] = [[0.0], [0.0]],
    # pylint: disable=dangerous-default-value
    lol_of_ys: List[list] = [[0.0], [0.0]],
    color: str = "red",
    markersize: float = 0.3,
    label: str = "UNLABELED",
    line_type: str = "-",
) -> None:
    """
    Matlplotlib cannot plot a list of lists
    Addresses none of our questsions, makes no prediction,
    and cannot be falsified.
    If one's prediction can't predict anything, it is just wrong,
    and one must try something else.

    Args:
        ax (matplotlib.axes.Axes): [description]
        lol_of_xs (List[list], optional): [description]. Defaults to [[0.0], [0.0]].
        lol_of_ys (List[list], optional): [description]. Defaults to [[0.0], [0.0]].
        color (str, optional): [description]. Defaults to "red".
        markersize (float, optional): [description]. Defaults to 0.3.
        label (str, optional): [description]. Defaults to "UNLABELED".
        line_type (str, optional): [description]. Defaults to "-".
    """
    assert np.shape(lol_of_xs) == np.shape(lol_of_ys)

    new_lol_of_xs = []
    new_lol_of_ys = []

    break_size = 2

    for list_no in range(len(lol_of_xs)):

        if len(lol_of_xs[list_no]) > break_size:
            npa_xs = np.asarray(lol_of_xs[list_no])
            npa_ys = np.asarray(lol_of_ys[list_no])

            for i in range(len(lol_of_xs[list_no]) // break_size):
                new_lol_of_xs.append(
                    npa_xs[(i) * break_size : (i + 1) * break_size + 1].tolist()
                )
                new_lol_of_ys.append(
                    npa_ys[(i) * break_size : (i + 1) * break_size + 1].tolist()
                )

            new_lol_of_xs.append(
                npa_xs[len(lol_of_xs[list_no]) // break_size :].tolist()
            )
            new_lol_of_ys.append(
                npa_xs[len(lol_of_ys[list_no]) // break_size :].tolist()
            )

        else:
            new_lol_of_xs.append(lol_of_xs[list_no])
            new_lol_of_ys.append(lol_of_ys[list_no])

    not_labelled = True

    for list_no in range(len(new_lol_of_xs)):
        x_values = (
            np.mod(np.asarray(new_lol_of_xs[list_no]) + 180, 360) - 180
        ).tolist()

        if (
            x_values[0] > -180
            and x_values[0] < 179
            and x_values[1] > -180
            and x_values[1] < 179
        ):
            x_map_temp, y_map_temp = (x_values, new_lol_of_ys[list_no])

            if not_labelled:
                # only label the first list
                ax.plot(
                    x_map_temp,
                    y_map_temp,
                    line_type,
                    markersize=markersize,
                    label=label,
                    color=color,
                    transform=ccrs.PlateCarree(),
                    LineWidth=0.5,
                )
                not_labelled = False
            else:
                ax.plot(
                    x_map_temp,
                    y_map_temp,
                    line_type,
                    markersize=markersize,
                    color=color,
                    transform=ccrs.PlateCarree(),
                    LineWidth=0.5,
                )


def draw_fronts_kim(ax: matplotlib.axes.Axes) -> None:
    """A function to read the Kim and Orsi (2014) data and plot it on SO.

    Now also includes the data from Kim (c.1995) for the STF.

    Args:
        ax (matplotlib.axes.Axes): draw the kim fronts on this axis.
    """

    def multi_line_map_plot() -> None:
        """split into list of lists and then plot them.

        :return:
        """
        for key in keys:
            if key == "stf":
                max_square = 8
            else:
                max_square = 1

            lol_xs, lol_ys = split_into_list_of_lists(
                max_square=max_square,
                list_of_xs=longitudes[key],
                list_of_ys=latitudes[key],
            )
            # print(lol_xs, lol_ys)
            plot_list_of_lists(
                ax,
                lol_of_xs=lol_xs,
                lol_of_ys=lol_ys,
                color=color_dict[key],
                markersize=marker_size_dict[key],
                label=label_dict[key],
                line_type="-",
            )

    latitudes: dict = {}
    longitudes: dict = {}
    files_names: list = [
        "pf_kim.txt",
        "saccf_kim.txt",
        "saf_kim.txt",
        "sbdy_kim.txt",
    ]
    files: list = [os.path.join(cst.KO_PATH, x) for x in files_names]
    keys: list = ["saf", "pf", "saccf", "sbdy"]
    color_dict: dict = {
        "saf": "black",
        "pf": "purple",
        "saccf": "green",
        "sbdy": "olive",
    }
    # label_dict = {"saf": "SAF-KO", "pf": "PF-KO", "saccf":
    #               "SACCF-KO", "sbdy": "SBDY-KO", "stf": "STF-O"}
    label_dict: dict = {
        "saf": "SAF",
        "pf": "PF",
        "saccf": "SACCF",
        "sbdy": "SBDY",
    }

    marker_size_dict: dict = {
        "saf": 0.15,
        "pf": 0.30,
        "saccf": 0.20,
        "sbdy": 0.10,
    }

    for file_no in range(len(files)):
        tmp_longitude = []
        tmp_latitude = []
        start = False  # Whether to skip the first line
        with open(files[file_no]) as file:
            for line in file:
                #  print(line)
                if not start:
                    line_elements = [float(elt.strip()) for elt in line.split("\t")]
                    tmp_longitude.append(float(line_elements[0]))
                    tmp_latitude.append(float(line_elements[1]))
                else:
                    start = False
        longitudes[keys[file_no]] = tmp_longitude
        latitudes[keys[file_no]] = tmp_latitude

    multi_line_map_plot()


def run_so_map() -> None:
    """Run through and plot."""
    sps.mpl_params()
    map_proj = ccrs.SouthPolarStereo()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection=map_proj)
    mp.southern_ocean_axes_setup(ax, fig)
    draw_fronts_kim(ax)
    plt.legend()
    plt.savefig(os.path.join(cst.FIGURE_PATH, "ko.png"))


if __name__ == "__main__":
    run_so_map()
