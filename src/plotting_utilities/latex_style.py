"""Plotting style file.

import src.plotting_utilities.latex_style as lsty
usage

ds = xr.open_dataset('example.nc')

sps.ds_for_grahing(ds).plot()
"""
from typing import Tuple
from sys import platform
import re
import matplotlib
import xarray as xr
from distutils.spawn import find_executable
import src.time_wrapper as twr

xr.set_options(keep_attrs=True)


def get_dim(
    width: float = 398.3386,
    fraction_of_line_width: float = 1,
    ratio: float = (5 ** 0.5 - 1) / 2,
) -> Tuple[float, float]:
    """Return figure height, width in inches to avoid scaling in latex.

    Default width is `src.constants.REPORT_WIDTH`.
    Default ratio is golden ratio, with figure occupying full page width.

    Args:
        width (float, optional): Textwidth of the report to make fontsizes match.
            Defaults to `src.constants.REPORT_WIDTH`.
        fraction_of_line_width (float, optional): Fraction of the document width
            which you wish the figure to occupy.  Defaults to 1.
        ratio (float, optional): Fraction of figure width that the figure height
            should be. Defaults to (5 ** 0.5 - 1)/2.

    Returns:
        fig_dim (tuple):
            Dimensions of figure in inches

    Example:
        Here is an example of using this function::
            >>> dim_tuple = get_dim(fraction_of_line_width=1, ratio=(5 ** 0.5 - 1) / 2)

    """

    # Width of figure
    fig_width_pt = width * fraction_of_line_width

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * ratio

    return (fig_width_in, fig_height_in)


def set_dim(
    fig: matplotlib.figure.Figure,
    width: float = 398.3386,
    fraction_of_line_width: float = 1,
    ratio: float = (5 ** 0.5 - 1) / 2,
) -> None:
    """Set aesthetic figure dimensions to avoid scaling in latex.

    Default width is `src.constants.REPORT_WIDTH`.
    Default ratio is golden ratio, with figure occupying full page width.

    Args:
        fig (matplotlib.figure.Figure): Figure object to resize.
        width (float): Textwidth of the report to make fontsizes match.
            Defaults to `src.constants.REPORT_WIDTH`.
        fraction_of_line_width (float, optional): Fraction of the document width
            which you wish the figure to occupy.  Defaults to 1.
        ratio (float, optional): Fraction of figure width that the figure height
            should be. Defaults to (5 ** 0.5 - 1)/2.

    Returns:
        void; alters current figure to have the desired dimensions

    Example:
        Here is an example of using this function::
            >>> set_dim(fig, fraction_of_line_width=1, ratio=(5 ** 0.5 - 1) / 2)
    """
    fig.set_size_inches(
        get_dim(width=width, fraction_of_line_width=fraction_of_line_width, ratio=ratio)
    )


@twr.timeit
def mpl_params(quality: str = "high", use_tex: bool = True, dpi: int = 600) -> None:
    """Apply plotting style to produce nice looking figures.

    Call this at the start of a script which uses `matplotlib`.
    Can enable `matplotlib` LaTeX backend if it is available.

    Args:
        use_tex (bool, optional): Whether or not to use latex matplotlib backend.
            Defaults to True.
        dpi (int, optional): Which dpi to set for the figures.
            Defaults to 600 dpi (high quality). 150 dpi probably
            fine for notebooks. Largest dpi needed for presentations.

    Examples:
        Basic setting the plotting defaults::
            >>> mpl_defaults()

        Setting defaults for a jupyter notebook::
            >>> mpl_defaults(use_tex=False, dpi=150)

    """
    print(quality)

    if platform == "darwin":
        matplotlib.use("TkAgg")

    p_general = {
        "font.family": "STIXGeneral",  # Nice alternative font.
        # "font.family": "serif",
        # "font.serif": [],
        # Use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 10,
        "font.size": 10,
        "figure.dpi": dpi,
        "savefig.dpi": dpi,
        "savefig.bbox": "tight",
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "date.autoformatter.year": "%Y",
        "date.autoformatter.month": "%Y-%m",
        "date.autoformatter.day": "%Y-%m-%d",
        "date.autoformatter.hour": "%m-%d %H",
        "date.autoformatter.minute": "%Y-%m-%d %H:%M:%S",
        "date.autoformatter.second": "%H:%M:%S",
        "date.autoformatter.microsecond": "%M:%S.%f",
        # Set the font for maths
        "mathtext.fontset": "cm",
        # "font.sans-serif": ["DejaVu Sans"],  # gets rid of error messages
        # "font.monospace": [],
        "figure.figsize": get_dim(),
        "lines.linewidth": 1.0,
        "scatter.marker": "+",
        "image.cmap": "viridis",
    }
    matplotlib.rcParams.update(p_general)
    matplotlib.style.use("seaborn-colorblind")

    if use_tex and find_executable("latex"):
        p_setting = {
            "pgf.texsystem": "pdflatex",
            "text.usetex": True,
            "pgf.preamble": (
                r"\usepackage[utf8x]{inputenc} \usepackage[T1]{fontenc}"
                + r"\usepackage[separate -uncertainty=true]{siunitx}"
            ),
        }
    else:
        p_setting = {
            "text.usetex": False,
        }
    matplotlib.rcParams.update(p_setting)


@twr.timeit
def tex_escape(text: str) -> str:
    """It is better to plot in TeX, but this involves escaping strings.

    from:
        https://stackoverflow.com/questions/16259923/
        how-can-i-escape-latex-special-characters-inside-django-templates
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX

    # removed unicode(key) from re.escape because this seemed an unnecessary,
      and was throwing an error.
    """
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    regex = re.compile(
        "|".join(
            re.escape(key) for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)


@twr.timeit
def proper_units(text: str) -> str:
    conv = {
        r"degK": r"K",
        r"degC": r"$^{\circ}$C",
        r"degrees\_celsius": r"$^{\circ}$C",
        r"degrees\_north": r"$^{\circ}$N",
        r"degrees\_east": r"$^{\circ}$E",
        r"degrees\_west": r"$^{\circ}$W",
        r"I metric": r"$\mathcal{I}$--metric",
    }
    regex = re.compile(
        "|".join(
            re.escape(key) for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)


@twr.timeit
def ds_for_graphing(dsA: xr.Dataset) -> xr.Dataset:
    """
    Transform dataset for graphing.

    Args:
        dsA (xr.Dataset): dataest input

    Returns:
        xr.Dataset: transformed dataset.
    """
    ds = dsA.copy()

    for _, da in ds.data_vars.items():
        for attr in da.attrs:
            if attr in ["units", "long_name"]:
                da.attrs[attr] = proper_units(tex_escape(da.attrs[attr]))

    for coord in ds.coords:
        if coord not in ["Z"]:
            for attr in ds.coords[coord].attrs:
                if attr in ["units", "long_name"]:
                    da.coords[coord].attrs[attr] = proper_units(
                        tex_escape(da.coords[coord].attrs[attr])
                    )

    return ds


mpl_params(quality="high")
