"""
sithom_plotting_style.py
========================
import sithom_plotting_style as sps
usage

ds = xr.open_dataset('example.nc')

sps.ds_for_grahing(ds).plot()
"""

import numpy as np
import numpy.linalg as la
import re

# import cartopy.crs as ccrs
import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import xarray as xr


def mpl_params(quality="high"):
    """
    Apply my plotting style to produce nice looking figures.
    Call this at the start of a script which uses matplotlib,
    and choose the correct setting.
    :return:
    """
    if quality == "high":
        matplotlib.style.use("seaborn-colorblind")
        param_set = {
            "pgf.texsystem": "pdflatex",
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": [],
            "font.sans-serif": ["DejaVu Sans"],
            "font.monospace": [],
            "lines.linewidth": 0.75,
            "axes.labelsize": 10,  # 10
            "font.size": 8,
            "legend.fontsize": 9,
            "xtick.labelsize": 10,  # 10,
            "ytick.labelsize": 10,  # 10,
            "scatter.marker": "+",
            "image.cmap": "RdYlBu_r",
            "pgf.preamble": [r"\usepackage[utf8x]{inputenc} \usepackage[T1]{fontenc}"],
        }
    else:
        matplotlib.style.use("seaborn-colorblind")
        param_set = {
            "text.usetex": False,
            "lines.linewidth": 0.75,
            "font.family": "sans-serif",
            "font.serif": [],
            "font.sans-serif": ["DejaVu Sans"],
            "axes.labelsize": 10,
            "font.size": 6,
            "legend.fontsize": 8,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "image.cmap": "RdYlBu_r",
        }

    matplotlib.rcParams.update(param_set)


def tex_escape(text):
    """
    It is better to plot in TeX, but this involves escaping strings.
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


def proper_units(text):
    conv = {
        "degK": r"K",
        "degC": r"$^{\circ}$C",
        "degrees\_celsius": r"$^{\circ}$C",
        "degrees\_north": r"$^{\circ}$N",
        "degrees\_east": r"$^{\circ}$E",
        "degrees\_west": r"$^{\circ}$W",
        "I metric": "$\mathcal{I}$--metric",
    }
    regex = re.compile(
        "|".join(
            re.escape(key) for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)


def ds_for_graphing(dsA):
    ds = dsA.copy()

    for varname, da in ds.data_vars.items():
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
