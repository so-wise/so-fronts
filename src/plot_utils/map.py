"""map.py by sdat2 - the different maps options.

southern_ocean_axes_setup - SO - up to 30 deg South to 90 degrees south.

"""
import numpy as np
import matplotlib
import matplotlib.path as mpath
import cartopy.crs as ccrs
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
    ax.coastlines(resolution="50m", linewidth=0.1)
