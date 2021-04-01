import numpy as np
import matplotlib.pyplot as plt
import src.plotting_utilities.latex_style as lsty
import src.plotting_utilities.colors as col
import src.data_loading.xr_values_loader as xvl
import src.time_wrapper as twr
import src.constants as cst
import xarray as xr


@twr.timeit
def make_cluster_profiles(ds):
    """
    :param ds: the dataset
    TODO: Add sanity check to this step. Look at BSOSE output, and averages the profiles,
    TODO: using zonal mean including all the longitudinal points, in salinity.

    """

    K_clusters = int(np.nanmax(ds.PCM_LABELS.values) + 1)
    height_list = []
    theta_mean_lol = []
    theta_std_lol = []
    salt_mean_lol = []
    salt_std_lol = []
    labels = xvl.order_indexes(ds.PCM_LABELS, [cst.T_COORD, cst.Y_COORD, cst.X_COORD])
    salt = xvl.order_indexes(
        ds.SALT, [cst.Z_COORD, cst.T_COORD, cst.Y_COORD, cst.X_COORD]
    )
    theta = xvl.order_indexes(
        ds.THETA, [cst.Z_COORD, cst.T_COORD, cst.Y_COORD, cst.X_COORD]
    )
    init_depth_levels = ds.coords[cst.Z_COORD].values

    for k_cluster in range(K_clusters):
        for list_of_list in [
            theta_mean_lol,
            theta_std_lol,
            salt_mean_lol,
            salt_std_lol,
        ]:
            list_of_list.append([])

        for depth_index in range(len(init_depth_levels)):
            depth = init_depth_levels[depth_index]
            if -cst.MIN_DEPTH >= depth >= -cst.MAX_DEPTH:
                theta_filtered = np.where(
                    labels == k_cluster, theta[depth_index, :, :, :], np.nan
                )
                theta_mean_lol[-1].append(np.nanmean(theta_filtered))
                theta_std_lol[-1].append(np.nanstd(theta_filtered))
                salt_filtered = np.where(
                    labels == k_cluster, salt[depth_index, :, :, :], np.nan
                )
                salt_mean_lol[-1].append(np.nanmean(salt_filtered))
                salt_std_lol[-1].append(np.nanstd(salt_filtered))
                if k_cluster == 0:
                    height_list.append(depth)

    new_ds = xr.Dataset(
        {
            "theta_mean": ([cst.CLUST_COORD, cst.Z_COORD], np.asarray(theta_mean_lol)),
            "salt_mean": ([cst.CLUST_COORD, cst.Z_COORD], np.asarray(salt_mean_lol)),
            "theta_std": ([cst.CLUST_COORD, cst.Z_COORD], np.asarray(theta_std_lol)),
            "salt_std": ([cst.CLUST_COORD, cst.Z_COORD], np.asarray(salt_std_lol)),
        },
        coords={
            cst.Z_COORD: np.array(height_list),
            cst.CLUST_COORD: range(0, K_clusters),
        },
    )
    print("profile_characteristics", new_ds)

    return new_ds


def plot_profiles_dataset(ds):
    """
    Originally from:
    https://scitools.org.uk/iris/docs/v1.6/examples/graphics/atlantic_profiles.html
    A program to plot profiles, originally of the original components etc.
    https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html

    There's a fair deal of duplication in this function.
    Could probably half its length without changing its functionality.
    """
    K_clusters = len(ds.coords[cst.CLUST_COORD].values)

    print("K_clusters", K_clusters)

    color_list = col.cluster_colors(K_clusters)
    ylim = [-1.8, -0.3]

    # THETA PLOTTING.
    plt.subplot(1, 2, 1)
    ax1 = plt.gca()

    for i in range(0, K_clusters):
        plt.plot(
            ds.isel(cluster=i).theta_mean,
            ds.coords[cst.Z_COORD].values / 1000,
            color=color_list[i],
            alpha=0.5,
            label=str(i + 1),
        )
        for sig_mult, alpha in [[1, 0.4]]:
            plt.fill_betweenx(
                ds.coords[cst.Z_COORD].values / 1000,
                ds.isel(cluster=i).theta_mean
                - np.multiply(sig_mult, ds.isel(cluster=i).theta_std),
                ds.isel(cluster=i).theta_mean
                + np.multiply(sig_mult, ds.isel(cluster=i).theta_std),
                alpha=alpha,
                color=color_list[i],
            )

    ax1.set_xlabel(
        r"Potential Temperature, $\theta$ / $^{\circ}\mathrm{C}$", color="black"
    )
    ax1.set_ylabel("Height / km")
    ax1.set_ylim(ylim)

    # SALINITY
    plt.subplot(1, 2, 2)
    ax2 = plt.gca()

    for i in range(0, K_clusters):
        plt.plot(
            ds.isel(cluster=i).salt_mean,
            ds.coords[cst.Z_COORD].values / 1000,
            color=color_list[i],
            alpha=0.5,
            label=str(i + 1),
        )
        for sig_mult, alpha in [[1, 0.4]]:
            plt.fill_betweenx(
                ds.coords[cst.Z_COORD].values / 1000,
                ds.isel(cluster=i).salt_mean
                - np.multiply(sig_mult, ds.isel(cluster=i).salt_std),
                ds.isel(cluster=i).salt_mean
                + np.multiply(sig_mult, ds.isel(cluster=i).salt_std),
                alpha=alpha,
                color=color_list[i],
            )

    ax2.set_xlabel(r"Salinity, $S$ / PSU", color="black")
    ax2.set_ylim(ylim)
    ax2.set_yticks([])
    plt.setp(ax2.get_yticklabels(), visible=False)

    ax1.legend(
        bbox_to_anchor=(0.0, 1.02, 2.05, 0.102),
        loc="lower left",
        ncol=2,
        mode="expand",
        borderaxespad=0.0,
    )

    plt.tight_layout()
