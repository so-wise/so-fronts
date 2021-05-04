"""Xarray panels."""
from typing import Sequence, Union, List
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import src.plot_utils.map as mp
import src.plot_utils.gen_panels as gp
import src.plot_utils.colors as col
import src.plot_utils.ko_plot as ko
import src.time_wrapper as twr
import src.constants as cst


@twr.timeit
def sep_plots(
    da_list: List[xr.DataArray],
    var_list: List[str],
    min_max_list: Union[List[list], any] = None,
    cmap_list: Union[List[any], any] = None,
) -> None:
    """
    Separate plots.

    Args:
        da_list (Sequence[xr.DataArray]): list of xr.DataArray.
        var_list  (List[str]): list of variable names.
        min_max_list (Union[List[list], any], optional): vmin and vmax.
            Defaults to None.
        cmap_list (Union[List[list], any], optional): vmin and vmax.
            Defaults to None.
    """

    map_proj = ccrs.SouthPolarStereo()
    carree = ccrs.PlateCarree()
    fig = plt.figure()
    num_da = len(da_list)
    fig, axes = plt.subplots(1, num_da, subplot_kw={"projection": map_proj})

    if len(da_list) >= 3:
        fig.set_size_inches(2.5 * num_da + 0.2 * num_da, 2.5 * 1.2)

    if cmap_list is None:
        cmap_list = [cst.DEFAULT_COLORMAP for x in range(len(da_list))]

    if min_max_list is not None:
        assert len(min_max_list) == len(da_list)

    for i in range(num_da):
        mp.southern_ocean_axes_setup(axes[i], fig)
        # sps.ds_for_graphing(da_list[i].to_dataset()).to_array().plot(
        if min_max_list is not None:
            da_list[i].plot(
                transform=carree,  # the data's projection
                ax=axes[i],
                subplot_kws={"projection": map_proj},  # the plot's projection
                cmap=cmap_list[i],
                vmin=min_max_list[i][0],
                vmax=min_max_list[i][1],
                cbar_kwargs={
                    "shrink": 0.8,
                    "label": var_list[i],
                    "orientation": "horizontal",
                    "pad": 0.01,
                },
            )
        else:
            da_list[i].plot(
                transform=carree,  # the data's projection
                ax=axes[i],
                subplot_kws={"projection": map_proj},  # the plot's projection
                cmap=cmap_list[i],
                cbar_kwargs={
                    "shrink": 0.8,
                    "label": var_list[i],
                    "orientation": "horizontal",
                    "pad": 0.01,
                },
            )
        # axes[i].coastlines()
        axes[i].set_title("")

    gp.label_subplots(axes)


@twr.timeit
def plot_single_i_metric(da: xr.DataArray) -> None:
    """Plot single i metric plot with viridis colormap.

    Args:
        da (xr.DataArray): i metric dataarray.
    """
    carree = ccrs.PlateCarree()
    map_proj = ccrs.SouthPolarStereo()
    pairs = da.coords[cst.P_COORD].values.shape[0]

    gs = GridSpec(
        nrows=2,
        ncols=pairs,
        width_ratios=[1 / pairs for x in range(pairs)],
        height_ratios=[1, 0.05],
        wspace=0.15,
    )

    fig = plt.gcf()

    ax1 = fig.add_subplot(gs[0, :], projection=map_proj)
    cbar_axes = [fig.add_subplot(gs[1, i]) for i in range(pairs)]

    mp.southern_ocean_axes_setup(ax1, fig)
    cmap_list = col.return_list_of_colormaps(pairs, fade_to_white=False)

    for i in range(pairs):
        im = da.isel(pair=i).plot(
            cmap=cmap_list[i],
            vmin=0,
            vmax=1,
            ax=ax1,
            add_colorbar=False,
            transform=carree,
            subplot_kws={"projection": map_proj},
        )
        cbar = plt.colorbar(
            im, cax=cbar_axes[i], orientation="horizontal", ticks=[0, 1]
        )
        cbar.set_label(da.coords[cst.P_COORD].values[i])
    plt.suptitle("")
    plt.title("")
    ax1.set_title("")
    # ax1.coastlines()


@twr.timeit
def plot_several_pair_i_metrics(
    da_list: Sequence[xr.DataArray], plot_ko: bool = False
) -> None:
    """Plot several pair i metrics.

    USAGE:
    plot_several_pair_i_metrics([run_through_plot(K=2).isel(time=0),
                                run_through_plot(K=4).isel(time=0)])
    plt.tight_layout()
    plt.savefig(
        "../FBSO-Report/images/fig5-new.png", dpi=900, bbox_inches="tight"
    )

    Args:
        da_list (Sequence[xr.DataArray]): list of dataarrays.
        plot_ko (bool): whether or not to plot the kim and orsi 2014 fronts.
    """

    carree = ccrs.PlateCarree()
    map_proj = ccrs.SouthPolarStereo()

    pairs_list = []
    width_ratios = []
    num_pairs: int = 0
    num_plots: int = len(da_list)

    for i in range(len(da_list)):
        if i != 0:
            width_ratios.append(0.05)
            num_pairs += 1
        num_pairs += da_list[i].coords[cst.P_COORD].values.shape[0]
        pairs = da_list[i].coords[cst.P_COORD].values
        pairs_list.append(pairs)
        for width in [1 / num_plots / len(pairs) for x in range(len(pairs))]:
            width_ratios.append(width)

    gs = GridSpec(
        nrows=2,
        ncols=num_pairs,
        width_ratios=width_ratios,
        height_ratios=[1, 0.05],
        wspace=0.15,
    )

    fig = plt.gcf()

    if len(da_list) >= 3:
        fig.set_size_inches(2.5 * num_plots + 0.2 * num_plots, 2.5 * 1.2)

    used_up_columns = 0
    primary_axes_list = []

    for i in range(len(pairs_list)):
        print("trying fig", i)

        ax1 = fig.add_subplot(
            gs[0, used_up_columns : used_up_columns + pairs_list[i].shape[0]],
            projection=map_proj,
        )
        cbar_axes = [
            fig.add_subplot(gs[1, used_up_columns + j])
            for j in range(len(pairs_list[i]))
        ]

        used_up_columns += pairs_list[i].shape[0] + 1

        mp.southern_ocean_axes_setup(ax1, fig)
        cmap_list = col.return_list_of_colormaps(
            len(pairs_list[i]), fade_to_white=False
        )

        for j in range(len(pairs_list[i])):
            print("pair number", j)
            print("pair name", da_list[i].coords[cst.P_COORD].values[j])

            im = (
                da_list[i]
                .isel(pair=j)
                .plot(
                    cmap=cmap_list[j],
                    vmin=0,
                    vmax=1,
                    ax=ax1,
                    add_colorbar=False,
                    transform=carree,
                    subplot_kws={"projection": map_proj},
                )
            )
            cbar = plt.colorbar(
                im,
                shrink=0.8,
                orientation="horizontal",
                pad=0.01,
                cax=cbar_axes[j],
                ticks=[0, 1],
            )
            cbar.set_label(da_list[i].coords[cst.P_COORD].values[j])

        plt.suptitle("")
        plt.title("")
        ax1.set_title("")
        if plot_ko:
            ko.draw_fronts_kim(ax1)
        primary_axes_list.append(ax1)

    gp.label_subplots(primary_axes_list)
    if plot_ko:
        ax1.legend(
            bbox_to_anchor=(0.0, -0.1, 0, 0),
            loc="lower right",
            ncol=2,
            mode="expand",
            borderaxespad=0.0,
        )
