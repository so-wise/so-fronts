"""Plotting style file.

import src.plotting_utilities.latex_style as lsty
usage

ds = xr.open_dataset('example.nc')

sps.ds_for_grahing(ds).plot()
"""
from sys import platform
import numpy as np
import numpy.linalg as la
import re
import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import xarray as xr
from distutils.spawn import find_executable
import src.time_wrapper as twr

xr.set_options(keep_attrs=True)


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
def proper_units(text):
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
