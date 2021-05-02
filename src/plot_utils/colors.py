"""Color utilities."""
from typing import Tuple
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
import src.time_wrapper as twr


def cluster_colors(number_clusters: int) -> np.ndarray:
    """Cluster colors.

    :param number_clusters: The number of clusters.
    :return: cmap.
    """
    return cm.get_cmap("Set1", number_clusters).colors


def replacement_color_list(number_of_colors: int) -> list:
    """Replacement color list.

    :param number_of_colors:
    :return:
    """
    assert isinstance(number_of_colors, int)

    color_d = {
        2: ["b", "r"],
        3: ["b", "green", "r"],
        4: ["b", "green", "orange", "r"],
        5: ["navy", "b", "green", "orange", "r"],
        6: ["navy", "b", "green", "orange", "r", "darkred"],
        7: ["navy", "b", "green", "olive", "orange", "r", "darkred"],
        8: [
            "navy",
            "b",
            "green",
            "olive",
            "orange",
            "r",
            "darkred",
            "deeppink",
        ],
        9: [
            "navy",
            "b",
            "#b8ffeb",
            "green",
            "olive",
            "orange",
            "r",
            "darkred",
            "#fe019a",
        ],
        10: [
            "navy",
            "b",
            "#b8ffeb",
            "green",
            "#ccfd7f",
            "olive",
            "orange",
            "r",
            "darkred",
            "#fe019a",
        ],
        11: [
            "navy",
            "b",
            "#b8ffeb",
            "green",
            "#ccfd7f",
            "olive",
            "orange",
            "r",
            "darkred",
            "#cf0234",
            "#fe019a",
        ],
        12: [
            "navy",
            "b",
            "#b8ffeb",
            "green",
            "#ccfd7f",
            "olive",
            "orange",
            "r",
            "darkred",
            "#cf0234",
            "#6e1005",
            "#fe019a",
        ],
        13: [
            "navy",
            "b",
            "#b8ffeb",
            "green",
            "#ccfd7f",
            "olive",
            "#fdb915",
            "orange",
            "r",
            "darkred",
            "#cf0234",
            "#6e1005",
            "#fe019a",
        ],
    }
    # pylint: disable=consider-using-get
    if number_of_colors in color_d:
        color_list = color_d[number_of_colors]
    else:
        color_list = color_d[13]
    return color_list


@twr.timeit
def return_list_of_colormaps(number: int, fade_to_white: bool = True) -> list:
    """
    Retunr list of colormaps.

    Args:
        number (int): number of colormaps needed.
        fade_to_white (bool, optional): Whether or not. Defaults to True.

    Returns:
        list: list of colormaps.
    """
    color_list = replacement_color_list(number)
    cmap_list = []
    for i in range(number):
        cmap_list.append(
            fading_colormap(
                color_list[i % len(color_list)], fade_to_white=fade_to_white
            )
        )
    return cmap_list


def _fading_colormap_name(from_name: str, fade_to_white: bool = True):
    """Takes a python color name and returns a fading color map.

    :param from_name:
    :return:
    """
    red, green, blue, _ = colors.to_rgba(from_name)

    return _fading_colormap_rgb((red, green, blue), fade_to_white=fade_to_white)


def _fading_colormap_hex(from_hex, fade_to_white: bool = True):
    """Takes a hex string as input and returns a fading color map as output.

    :param from_hex:
    :return:
    """
    hex_number = from_hex.lstrip("#")
    return _fading_colormap_rgb(
        tuple(int(hex_number[i : i + 2], 16) for i in (0, 2, 4)),
        fade_to_white=fade_to_white,
    )


def _fading_colormap_rgb(from_rgb: Tuple, fade_to_white: bool = True):
    """Takes an r g b tuple and returns a fading color map.

    :param from_rgb: an r g b tuple
    :return:
    """

    # from color r,g,b
    red1, green1, blue1 = from_rgb

    # to color r,g,b
    red2, green2, blue2 = 1, 1, 1

    if fade_to_white:
        cdict = {
            "red": ((0, red1, red1), (1, red2, red2)),
            "green": ((0, green1, green1), (1, green2, green2)),
            "blue": ((0, blue1, blue1), (1, blue2, blue2)),
        }
    else:
        cdict = {
            "red": ((0, red2, red2), (1, red1, red1)),
            "green": ((0, green2, green2), (1, green1, green1)),
            "blue": ((0, blue2, blue2), (1, blue1, blue1)),
        }

    cmap = colors.LinearSegmentedColormap("custom_cmap", cdict)

    return cmap


@twr.timeit
def fading_colormap(from_color: str, fade_to_white: bool = True):
    """Takes a hex or color name, and returns a fading color map.

    example usage:

    # cmap_a = fading_colormap('blue')
    # cmap_b = fading_colormap('#96f97b')

    :param from_color: either a hex or a name
    :return: cmap --> a colormap that can be used as a parameter in a plot.
    """
    if from_color.startswith("#"):
        cmap = _fading_colormap_hex(from_color, fade_to_white=fade_to_white)
    else:
        cmap = _fading_colormap_name(from_color, fade_to_white=fade_to_white)

    # print(cmap, cmap)

    return cmap
