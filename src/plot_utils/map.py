"""map.py by sdat2 - the different maps options.

southern_ocean_axes_setup - SO - up to 30 deg South to 90 degrees south.

"""
import numpy as np
from typing import List
import xarray as xr
from numba import jit
import matplotlib
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import src.constants as cst
import src.time_wrapper as twr

# import cartopy.feature
# import matplotlib.cm as cm


@twr.timeit
def southern_ocean_axes_setup(
    ax: matplotlib.axes.Axes, fig: matplotlib.figure.Figure
) -> None:
    """
    This function sets up the subplot so that it is a cartopy map of the southern ocean.

    Void as the ax and figure objects are pointers not data.

    Args:
        ax (matplotlib.axes.Axes): The axis object to add the map to.
        fig (matplotlib.figure.Figure): The figure object for the figure in general.
    """
    carree = ccrs.PlateCarree()
    ax.set_extent([-180, 180, -90, -30], carree)
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

    def plot_boundary():
        theta = np.linspace(0, 2 * np.pi, 100)
        center, radius = [0.5, 0.5], 0.45
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)

    plot_boundary()
    ax.coastlines(resolution="50m", linewidth=0.2)

    @jit(cache=True)  # significant performance enhancement.
    def find_isobath(
        tmp_bathymetry: np.ndarray, crit_depth=cst.MAX_DEPTH
    ) -> List[list]:
        isobath_index_list = []
        shape_bathymetry = np.shape(tmp_bathymetry)
        for i in range(0, shape_bathymetry[0] - 1):
            for j in range(0, shape_bathymetry[1] - 1):
                if tmp_bathymetry[i, j] >= crit_depth:
                    if tmp_bathymetry[i - 1, j] < crit_depth:
                        isobath_index_list.append([i, j])
                    if tmp_bathymetry[i, j - 1] < crit_depth:
                        isobath_index_list.append([i, j])
                    if tmp_bathymetry[i + 1, j] < crit_depth:
                        isobath_index_list.append([i, j])
                    if tmp_bathymetry[i, j + 1] < crit_depth:
                        isobath_index_list.append([i, j])
        return isobath_index_list

    i_list = find_isobath(
        xr.open_dataset(cst.SALT_FILE)[cst.DEPTH_NAME].values,
        crit_depth=cst.MAX_DEPTH,
    )

    index_npa: np.ndarray = np.array(i_list)
    lons = xr.open_dataset(cst.SALT_FILE)[cst.X_COORD].values[index_npa[:, 1]]
    lats = xr.open_dataset(cst.SALT_FILE)[cst.Y_COORD].values[index_npa[:, 0]]

    ax.plot(
        lons,
        lats,
        ".",
        markersize=0.3,
        color="grey",
    )
