import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import src.plotting_utilities.map as map
import src.plotting_utilities.gen_panels as gp
import src.plotting_utilities.colors as col


def sep_plots(da_list, var_list):

    map_proj = ccrs.SouthPolarStereo()
    carree = ccrs.PlateCarree()

    fig = plt.figure()

    num_da = len(da_list)

    fig, axes = plt.subplots(1, num_da, subplot_kw={"projection": map_proj})

    for i in range(num_da):
        map.southern_ocean_axes_setup(axes[i], fig)
        # sps.ds_for_graphing(da_list[i].to_dataset()).to_array().plot(
        da_list[i].plot(
            transform=carree,  # the data's projection
            ax=axes[i],
            subplot_kws={"projection": map_proj},  # the plot's projection
            cbar_kwargs={
                "shrink": 0.8,
                "label": var_list[i],
                "orientation": "horizontal",  # xr_da.name
                "pad": 0.01,
            },
        )
        axes[i].coastlines()
        axes[i].set_title("")

    gp.label_subplots(axes)


def plot_single_i_metric(da):
    carree = ccrs.PlateCarree()
    map_proj = ccrs.SouthPolarStereo()
    pairs = da.coords["pair"].values.shape[0]

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

    map.southern_ocean_axes_setup(ax1, fig)
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
        cbar.set_label(da.coords["pair"].values[i])
    plt.suptitle("")
    plt.title("")
    ax1.set_title("")
    ax1.coastlines()
