"""
The purpose of this is to visualise the i_metric on the southern ocean map.
"""
import numpy as np
import xarray as xr
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import src.plotting_utilities.colors as col
import src.time_wrapper as twr
import src.plotting_utilities.gen_panels as gp
import src.plotting_utilities.latex_style as lsty
import src.plotting_utilities.ko_plot as ko
import src.plotting_utilities.map as mp
import src.constants as cst


@twr.timeit
def plot_map_imetric_clusters(da_i: xr.DataArray, da: xr.DataArray) -> None:
    """Plot map i metric clusters.

    :param da_i: xarray.dataarray object.
    :param da: xarray.dataarray object.

    :return: void (although matplotlib will be storing the figure).
    """
    pairs_list = []
    width_ratios = []
    num_pairs = 0
    num_plots = 2
    da_i = da_i + 1
    map_proj = ccrs.SouthPolarStereo()
    carree = ccrs.PlateCarree()

    for i in range(num_plots):
        if i == 0:
            num_pairs += 1
            pairs = np.asarray([i for i in range(1)])
            width_ratios.append(0.5)
            pairs_list.append(pairs)
        elif i == 1:
            width_ratios.append(0.05)
            num_pairs += 1
            pairs = da.coords[cst.P_COORD].values
            cmap_list = col.return_list_of_colormaps(len(pairs), fade_to_white=False)
            pairs_list.append(pairs)
            for width in [1 / num_plots / len(pairs) for x in range(len(pairs))]:
                width_ratios.append(width)
        print(pairs_list)
        print(width_ratios)

    gs = GridSpec(
        nrows=2,
        ncols=len(width_ratios),
        width_ratios=width_ratios,
        height_ratios=[1, 0.05],
        wspace=0.15,
    )

    fig = plt.gcf()
    fig.set_size_inches(7 * num_plots + 1 * num_plots, 7 * 1.2)
    used_up_columns = 0
    primary_axes_list = []

    for i in range(2):
        if i == 0:
            ax1 = fig.add_subplot(
                gs[0, 0],
                projection=map_proj,
            )
            cbar_ax = fig.add_subplot(gs[1, 0])
            used_up_columns += 2
            mp.southern_ocean_axes_setup(ax1, fig)

        elif i == 1:
            print("used_up_columns", used_up_columns)
            print(
                "used_up_columns + pairs_list[i].shape[0]",
                used_up_columns + pairs_list[i].shape[0],
            )
            ax1 = fig.add_subplot(
                gs[0, used_up_columns : used_up_columns + pairs_list[i].shape[0]],
                projection=map_proj,
            )
            mp.southern_ocean_axes_setup(ax1, fig)
            cbar_axes = [
                fig.add_subplot(gs[1, used_up_columns + j])
                for j in range(len(pairs_list[i]))
            ]
            used_up_columns += pairs_list[i].shape[0] + 1

        number_clusters = 5

        if i == 0:
            print("da_i", da_i)
            print("ax1", ax1)
            im = da_i.plot(
                ax=ax1,
                add_colorbar=False,
                cmap=cm.get_cmap("Set1", number_clusters),
                vmin=0.5,
                vmax=number_clusters + 0.5,
                transform=carree,
                subplot_kws={"projection": map_proj},
                alpha=0.5,
            )

            plt.colorbar(
                im,
                cax=cbar_ax,
                label="Class Assignment",
                ticks=range(1, number_clusters + 1),
                orientation="horizontal",
            )

            primary_axes_list.append(ax1)
            ax1.set_title("")
            ax1.coastlines()

        if i == 1:
            fig = plt.gcf()

            for j in range(len(pairs_list[i])):
                # kim orsi fronts.
                im = da.isel(pair=j).plot(
                    cmap=cmap_list[j],
                    vmin=0,
                    vmax=1,
                    ax=ax1,
                    add_colorbar=False,
                    transform=carree,
                    subplot_kws={"projection": map_proj},
                    alpha=0.5,
                )

                cbar = plt.colorbar(
                    im, cax=cbar_axes[j], orientation="horizontal", ticks=[0, 1]
                )
                cbar.set_label(da.coords[cst.P_COORD].values[j])

            primary_axes_list.append(ax1)
            mp.southern_ocean_axes_setup(ax1, fig)
            ax1.set_title("")
            ax1.coastlines()
            ko.draw_fronts_kim(ax1)
            ax1.legend()

    gp.label_subplots(primary_axes_list)


# plt.tight_layout()
# gp.label_subplots(primary_axes_list)
# plt.savefig("../FBSO-Report/images/fig2-3d.png", bbox_inches="tight", dpi=700)
