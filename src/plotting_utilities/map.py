import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature


def southern_ocean_axes_setup(ax, fig):
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
