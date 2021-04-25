"""The purpose of this is the algorithm in 3D."""
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import xarray as xr
import src.models.to_pair_i_metric as tpi
import src.plotting_utilities.ellipses as pel
import src.plotting_utilities.colors as col
import src.time_wrapper as twr
import src.constants as cst

# import src.plotting_utilities.gen_panels as gp


@twr.timeit
def comp_3d(
    weights: np.ndarray, means: np.ndarray, covariances: np.ndarray, ds: xr.Dataset
) -> None:
    """
    This will hopefully plot fig2a and fig2b with automatic labelling.

    Args:
        weights (np.ndarray): weights numpy array.
        means (np.ndarray): means numpy array.
        covariances (np.ndarray): covariances numpy array.
        ds (xr.Dataset): dataset.

    """
    da = tpi.pair_i_metric(ds)
    pairs_list = []
    width_ratios = []
    num_pairs = 0
    num_plots = 2

    for i in range(num_plots):
        if i == 0:
            num_pairs += 1
            pairs = np.asarray([0])
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

        print("pairs_list", pairs_list)
        print("width_ratios", width_ratios)

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
        print("trying fig", i)

        if i == 0:
            ax1 = fig.add_subplot(
                gs[0, 0],
                projection="3d",
            )
            cbar_ax = fig.add_subplot(gs[1, 0])
            used_up_columns += 2

        elif i == 1:
            print("used_up_columns", used_up_columns)
            print(
                "used_up_columns + pairs_list[i].shape[0]",
                used_up_columns + pairs_list[i].shape[0],
            )
            ax1 = fig.add_subplot(
                gs[0, used_up_columns : used_up_columns + pairs_list[i].shape[0]],
                projection="3d",
            )

            cbar_axes = [
                fig.add_subplot(gs[1, used_up_columns + j])
                for j in range(len(pairs_list[i]))
            ]

            used_up_columns += pairs_list[i].shape[0] + 1

        if i == 0:
            principal_component_da = ds.PCA_VALUES
            im = ax1.scatter(
                principal_component_da.isel(pca=0).values.ravel(),
                principal_component_da.isel(pca=1).values.ravel(),
                principal_component_da.isel(pca=2).values.ravel(),
                cmap=cm.get_cmap("Set1", len(weights)),
                c=ds.PCM_LABELS.values.ravel() + 1,
                vmin=0.5,
                vmax=len(weights) + 0.5,
                alpha=0.5,
            )

            # VIEWING ANGLE
            ax1.view_init(30, 60)

            plt.colorbar(
                im,
                cax=cbar_ax,
                label="Class Assignment",
                ticks=range(1, len(weights) + 1),
                orientation="horizontal",
            )
            ax1.set_xlabel("PC1")
            ax1.set_ylabel("PC2")
            ax1.set_zlabel("PC3")
            primary_axes_list.append(ax1)

        if i == 1:

            number_clusters = np.shape(means)[0]
            colors = col.cluster_colors(number_clusters)
            fig = plt.gcf()

            for j in range(number_clusters):
                fig, ax1 = pel.plot_ellipsoid(
                    fig, ax1, covariances[j], means[j], weights[j], colors[j]
                )

            for j in range(len(pairs_list[i])):

                im = ax1.scatter(
                    ds.PCA_VALUES.isel(pca=0).values.ravel(),
                    ds.PCA_VALUES.isel(pca=1).values.ravel(),
                    ds.PCA_VALUES.isel(pca=2).values.ravel(),
                    c=da.isel(pair=j).values.ravel(),
                    cmap=cmap_list[j],
                    alpha=0.5,
                )

                cbar = plt.colorbar(
                    im, cax=cbar_axes[j], orientation="horizontal", ticks=[0, 1]
                )
                # VIEWING ANGLE
                ax1.view_init(30, 60)
                cbar.set_label(da.coords[cst.P_COORD].values[j])

            primary_axes_list.append(ax1)
            ax1.set_xlabel("PC1")
            ax1.set_ylabel("PC2")
            ax1.set_zlabel("PC3")

    # plt.tight_layout()
    # gp.label_subplots(primary_axes_list)
    # plt.savefig("../FBSO-Report/images/fig2-3d.png", bbox_inches="tight", dpi=700)
