"""Make figures: run through all the paper figures and make them.

Takes roughly 5 minutes the first time it is run.
"""
import os
import numpy.ma as ma
import xarray as xr
import matplotlib.pyplot as plt
import logging
import src.constants as cst
import src.plot_utils.latex_style as lsty
import src.plot_utils.xarray_panels as xp
import src.models.train_pyxpcm as tim
import src.plot.clust_3d as c3d
import src.plot.i_map as imap
import src.plot.profiles as prof
import src.data_loading.io_names as io
import src.time_wrapper as twr


@twr.timeit
def make_all_figures() -> None:
    """
    Make all the figures in the paper in a sequence.

    Takes about 8 minutes or so to run on my laptop.

    Seems to take much longer on jasmin.

    3089 seconds on jasmin.

    That is 50 minutes apparently.
    """
    # Create or get the logger
    logger = logging.getLogger(__name__)
    # set log level
    logger.setLevel(logging.INFO)

    # pylint: disable=logging-not-lazy
    logger.info(
        "Starting make_all_figures_in_sequence, "
        + " should take about about 8 minutes."
    )
    print(
        "settings:\n",
        "cst.EXAMPLE_TIME_INDEX",
        cst.EXAMPLE_TIME_INDEX,
        "cst.SEED",
        cst.SEED,
    )
    lsty.mpl_params()

    # FIGURE 1: pc maps.
    logger.info("Making pc maps.")

    ds = xr.open_dataset(cst.DEFAULT_NC)

    da_temp = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1", "PC2", "PC3"],
    )
    pc_maps_name = os.path.join(cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_map.png")
    plt.savefig(pc_maps_name)
    plt.clf()

    # FIGURE 2 ## make profiles.
    logger.info("Making profiles.")

    temp_name = os.path.join(cst.DATA_PATH, "RUN_" + cst.RUN_NAME + "_temp.nc")
    profiles_name = os.path.join(
        cst.DATA_PATH, "RUN_" + cst.RUN_NAME + "_profiles_temp.nc"
    )
    pcm, ds = tim.train_on_interpolated_year(
        time_i=cst.EXAMPLE_TIME_INDEX,
        k_clusters=cst.K_CLUSTERS,
        maxvar=cst.D_PCS,
        min_depth=cst.MIN_DEPTH,
        max_depth=cst.MAX_DEPTH,
        remove_init_var=False,
    )

    ds.to_netcdf(path=temp_name)
    ds = xr.open_dataset(temp_name)
    profile_ds = prof.make_profiles(ds)
    profile_ds.to_netcdf(path=profiles_name)
    profile_ds = xr.open_dataset(profiles_name)

    print(profile_ds)

    prof.plot_profiles(profile_ds)
    profiles_plot_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_profiles.png"
    )

    plt.savefig(profiles_plot_name)
    plt.clf()

    # FIGURE 3: Plot 3d clusters.
    logger.info("Plot 3d clusters.")

    c3d.comp_3d(
        # pylint: disable=protected-access
        pcm._classifier.weights_,
        # pylint: disable=protected-access
        pcm._classifier.means_,
        # pylint: disable=protected-access
        pcm._classifier.covariances_,
        ds,
    )
    s3d_plot_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_s3d_clusters.png"
    )
    plt.savefig(s3d_plot_name)
    plt.clf()

    # FIGURE 4: I metric viridis colormap.
    logger.info("4: I metric geographical map with viridis colormap.")

    ds = xr.open_dataset(cst.DEFAULT_NC)
    xp.sep_plots(
        [
            ds.IMETRIC.isel(Imetric=0, time=cst.EXAMPLE_TIME_INDEX),
            ds.IMETRIC.isel(Imetric=0).mean(dim=cst.T_COORD, skipna=True),
        ],
        [r"$\mathcal{I}$-metric ", r"$\mathcal{I}$-metric"],
        [[0.0, 1.0], [0.0, 1.0]],
        ["viridis", "viridis"],
    )
    imetric_dual_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_dual.png"
    )
    plt.savefig(imetric_dual_name)
    plt.clf()

    # FIGURE 5: single multi color.
    logger.info("5: Example multi colour i metric plot for K=5.")

    da = io.return_pair_i_metric(k_clusters=cst.K_CLUSTERS)
    xp.plot_single_i_metric(da.isel(time=0))
    imetric_single_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_single.png"
    )
    plt.savefig(imetric_single_name)
    plt.clf()

    # FIGURE 6: Plot clusters and i metrics on maps.
    logger.info("6: Plot cluster/imetric on map.")

    da = io.return_pair_i_metric(k_clusters=cst.K_CLUSTERS).isel(time=0)
    da_i = xr.open_dataset(cst.DEFAULT_NC).A_B.isel(rank=0, time=cst.EXAMPLE_TIME_INDEX)

    print(da)

    imap.map_imetric(da_i, da)
    imetric_single_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_map_i_comp.png"
    )
    plt.savefig(imetric_single_name)
    plt.clf()

    # FIGURE 7: Plot different k_clusters cluster multi colour plots.
    logger.info("7: compare K=2, K=4.")

    xp.plot_several_pair_i_metrics(
        [
            io.return_pair_i_metric(k_clusters=2).isel(time=0),
            io.return_pair_i_metric(k_clusters=4).isel(time=0),
        ]
    )
    plt.tight_layout()
    imetric_comp_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_comp.png"
    )
    plt.savefig(imetric_comp_name)
    plt.clf()

    ds = xr.open_dataset(cst.DEFAULT_NC)

    # FIGURE 8: PC1 y grads
    # TODO: Replace with Sobel.
    logger.info("8: PC1 y grads.")

    da_temp = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX).differentiate(cst.Y_COORD)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1 y-grad", "PC2 y-grad", "PC3 y-grad"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_y_grad.png"
    )
    plt.savefig(pc_y_grad_name)
    plt.clf()

    # Appendix
    logger.info("A: Appendix figures.")

    # uvel, pca1 y grad for example.
    logger.info("A: uvel/ y grad for example.")

    uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)
    ds = xr.open_dataset(cst.DEFAULT_NC)
    xp.sep_plots(
        [
            ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX, pca=0).differentiate(
                cst.Y_COORD
            ),
            uvel_ds.UVEL.isel(time=cst.EXAMPLE_TIME_INDEX),
            ds.PCA_VALUES.isel(pca=0)
            .differentiate(cst.Y_COORD)
            .mean(dim=cst.T_COORD, skipna=True),
            uvel_ds.UVEL.mean(dim=cst.T_COORD, skipna=True),
        ],
        ["PC1 y-grad", r"$U$ (pcm s$^{-1}$)", "PC1 y-grad", r"$U$ (pcm s$^{-1}$)"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_y_grad.png"
    )
    plt.savefig(pc_y_grad_name)
    plt.clf()

    # uvel, pca1 y grad over time.
    logger.info("A: uvel/ y grad overtime.")

    uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)
    pca_ds = xr.open_dataset(cst.DEFAULT_NC).isel(pca=0).differentiate(cst.Y_COORD)

    cor_list = []

    for time_i in range(len(uvel_ds.coords[cst.T_COORD].values)):
        cor = ma.corrcoef(
            ma.masked_invalid(uvel_ds.isel(time=time_i).UVEL.values.ravel()),
            ma.masked_invalid(pca_ds.isel(time=time_i).PCA_VALUES.values.ravel()),
        )
        cor_list.append(cor[1, 0])

    plt.plot(uvel_ds.coords[cst.T_COORD].values, cor_list)
    plt.xlabel("Time")
    plt.ylabel("Correlation coefficient")

    plt.xlim(
        [uvel_ds.coords[cst.T_COORD].values[0], uvel_ds.coords[cst.T_COORD].values[59]]
    )
    plt.title("Correlation between PC1 y-grad and $U$")
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_y_grad_corr.png"
    )
    plt.savefig(pc_y_grad_name)
    plt.clf()

    #  compare correlations and make correlation graph.
    logger.info("A: vvel/ y grad over time.")

    cor = ma.corrcoef(
        ma.masked_invalid(
            uvel_ds.mean(dim=cst.T_COORD, skipna=True).UVEL.values.ravel()
        ),
        ma.masked_invalid(
            pca_ds.mean(dim=cst.T_COORD, skipna=True).PCA_VALUES.values.ravel()
        ),
    )
    print(cor)

    logger.info("A: vvel/ y grad in pc1 over time.")

    vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)
    pca_ds = xr.open_dataset(cst.DEFAULT_NC).isel(pca=0).differentiate(cst.X_COORD)

    cor_list = []

    for time_i in range(len(uvel_ds.coords[cst.T_COORD].values)):
        cor = ma.corrcoef(
            ma.masked_invalid(vvel_ds.isel(time=time_i).VVEL.values.ravel()),
            ma.masked_invalid(pca_ds.isel(time=time_i).PCA_VALUES.values.ravel()),
        )
        cor_list.append(cor[1, 0])

    plt.plot(uvel_ds.coords[cst.T_COORD].values, cor_list)
    plt.xlabel("Time")
    plt.ylabel("Correlation coefficient")
    plt.xlim(
        [uvel_ds.coords[cst.T_COORD].values[0], uvel_ds.coords[cst.T_COORD].values[59]]
    )
    plt.title("Correlation between PC1 x-grad and $V$")
    pc_x_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_x_grad_corr.png"
    )
    plt.savefig(pc_x_grad_name)
    plt.clf()

    # compare meridional velocity to gradient.
    logger.info("A: vvel/ y grad in pc1 at one time point.")

    vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=cst.EXAMPLE_Z_INDEX)
    xp.sep_plots(
        [
            ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX, pca=0).differentiate(
                cst.X_COORD
            ),
            vvel_ds.VVEL.isel(time=cst.EXAMPLE_TIME_INDEX),
            ds.PCA_VALUES.isel(pca=0)
            .differentiate(cst.X_COORD)
            .mean(dim=cst.T_COORD, skipna=True),
            vvel_ds.VVEL.mean(dim=cst.T_COORD, skipna=True),
        ],
        ["PC1 x-grad", r"$V$ (pcm s$^{-1}$)", "PC1 x-grad", r"$V$ (pcm s$^{-1}$)"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_x_grad.png"
    )
    plt.savefig(pc_y_grad_name)
    plt.clf()

    logger.info("A: finished.")
