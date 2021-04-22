"""Make figures: run through all the paper figures and make them.

Takes roughly 5 minutes the first time it is run.
"""
import os
import numpy.ma as ma
import xarray as xr
import matplotlib.pyplot as plt
import src.constants as cst
import src.plotting_utilities.latex_style as lsty
import src.plotting_utilities.xarray_panels as xp
import src.models.train_i_metric as tim
import src.plotting_utilities.spec_i_clusters_3d_comp as s3d
import src.plotting_utilities.i_cluster_map_comp as icm
import src.plotting_utilities.cluster_profiles as cp
import src.models.to_pair_i_metric as tpi
import src.data_loading.io_name_conventions as io
import src.time_wrapper as twr


@twr.timeit
def return_pair_i_metric(
    K: int = cst.K_CLUSTERS, pca: int = cst.D_PCS, save_nc: bool = True
) -> xr.DataArray:
    """Return pair i metric.

    Args:
        K (int, optional): [description]. Defaults to cst.K_CLUSTERS.
        pca (int, optional): [description]. Defaults to cst.D_PCS.
        save_nc (bool, optional): [description]. Defaults to True.

    Returns:
        xr.DataArray: [description]
    """
    link_to_netcdf = io._return_name(K, pca) + ".nc"
    ds = xr.open_dataset(link_to_netcdf)
    print(ds.__str__())
    batch_size = 2
    for i in range(40, 42, batch_size):
        print("running", i)
        if save_nc:
            da = tpi.pair_i_metric(
                ds.isel(time=slice(i, i + batch_size)), threshold=0.05
            )
            print("not saving")
        else:
            da = (
                xr.open_dataset(io._return_pair_name(K, pca) + "..nc")
                .to_array()
                .isel(time=slice(i, i + batch_size))
            )

    return da


@twr.timeit
def other() -> None:
    xp.plot_several_pair_i_metrics(
        [return_pair_i_metric(K=2).isel(time=0), return_pair_i_metric(K=4).isel(time=0)]
    )
    # "../FBSO-Report/images/fig5-new.png"
    plt.tight_layout()
    imetric_comp_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_comp.png"
    )
    plt.savefig(imetric_comp_name, dpi=900, bbox_inches="tight")
    plt.clf()


def nother() -> None:
    # FIGURE 6
    example_time_index = 40
    ds = xr.open_dataset("~/pyxpcm_sithom/nc/i-metric-joint-k-5-d-3.nc")
    da_temp = ds.PCA_VALUES.isel(time=example_time_index).differentiate(cst.Y_COORD)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1 y-grad", "PC2 y-grad", "PC3 y-grad"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_y_grad.png"
    )
    # "../FBSO-Report/images/fig6-new.png"
    plt.savefig(pc_y_grad_name, dpi=900, bbox_inches="tight")
    plt.clf()


@twr.timeit
def make_all_figures_in_sequence() -> None:

    print("Starting make_all_figures_in_sequence, should take about about 8 minutes.")

    example_time_index = 40

    print("settings:", "example_time_index", example_time_index, "cst.SEED", cst.SEED)

    # FIGURE 1

    ds = xr.open_dataset("~/pyxpcm_sithom/nc/i-metric-joint-k-5-d-3.nc")

    da_temp = ds.PCA_VALUES.isel(time=example_time_index)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1", "PC2", "PC3"],
    )
    pc_maps_name = os.path.join(cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_map.png")
    plt.savefig(pc_maps_name, dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 1.5 ## make panels.

    temp_name = os.path.join(cst.DATA_PATH, "RUN_" + cst.RUN_NAME + "_temp.nc")
    profiles_name = os.path.join(
        cst.DATA_PATH, "RUN_" + cst.RUN_NAME + "_profiles_temp.nc"
    )
    m, ds = tim.train_on_interpolated_year(
        time_i=42,
        K=cst.K_CLUSTERS,
        maxvar=cst.D_PCS,
        min_depth=cst.MIN_DEPTH,
        max_depth=cst.MAX_DEPTH,
        separate_pca=False,
        remove_init_var=False,
    )

    ds.to_netcdf(path=temp_name)
    ds = xr.open_dataset(temp_name)
    profile_ds = cp.make_cluster_profiles(ds)
    profile_ds.to_netcdf(path=profiles_name)
    profile_ds = xr.open_dataset(profiles_name)

    print(profile_ds)

    cp.plot_profiles_dataset(profile_ds)
    profiles_plot_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_profiles.png"
    )

    plt.savefig(profiles_plot_name, bbox_inches="tight", dpi=700)
    plt.clf()

    # FIGURE 2

    s3d.plot_fig2_mult(
        m._classifier.weights_, m._classifier.means_, m._classifier.covariances_, ds
    )
    s3d_plot_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_s3d_clusters.png"
    )
    # "../FBSO-Report/images/fig2-3d.png"
    plt.savefig(s3d_plot_name, bbox_inches="tight", dpi=700)
    plt.clf()

    # FIGURE 3

    ds = xr.open_dataset("~/pyxpcm_sithom/nc/i-metric-joint-k-5-d-3.nc")
    xp.sep_plots(
        [
            ds.IMETRIC.isel(Imetric=0, time=example_time_index),
            ds.IMETRIC.isel(Imetric=0).mean(dim=cst.T_COORD, skipna=True),
        ],
        [r"$\mathcal{I}$-metric ", r"$\mathcal{I}$-metric"],
    )
    imetric_dual_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_dual.png"
    )
    # "../FBSO-Report/images/fig3-new.png"
    plt.savefig(imetric_dual_name, dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 4

    da = return_pair_i_metric(K=5)
    xp.plot_single_i_metric(da.isel(time=0))
    imetric_single_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_single.png"
    )
    # "../FBSO-Report/images/fig4-new.png"
    plt.savefig(imetric_single_name, dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 4
    da = return_pair_i_metric(K=5).isel(time=0)
    da_i = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-5-d-3.nc").A_B.isel(
        rank=0, time=40
    )
    print(da)
    icm.plot_map_imetric_clusters(da_i, da)
    imetric_single_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_map_i_comp.png"
    )
    # "../FBSO-Report/images/fig4-new.png"
    plt.savefig(imetric_single_name, dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 5

    xp.plot_several_pair_i_metrics(
        [return_pair_i_metric(K=2).isel(time=0), return_pair_i_metric(K=4).isel(time=0)]
    )
    # "../FBSO-Report/images/fig5-new.png"
    plt.tight_layout()
    imetric_comp_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_i_metric_comp.png"
    )
    plt.savefig(imetric_comp_name, dpi=900, bbox_inches="tight")
    plt.clf()

    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-5-d-3.nc")

    # FIGURE 6
    da_temp = ds.PCA_VALUES.isel(time=example_time_index).differentiate(cst.Y_COORD)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1 y-grad", "PC2 y-grad", "PC3 y-grad"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_y_grad.png"
    )
    # "../FBSO-Report/images/fig6-new.png"
    plt.savefig(pc_y_grad_name, dpi=900, bbox_inches="tight")
    plt.clf()

    # Appendix
    uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=15)
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-5-d-3.nc")
    xp.sep_plots(
        [
            ds.PCA_VALUES.isel(time=example_time_index, pca=0).differentiate(
                cst.Y_COORD
            ),
            uvel_ds.UVEL.isel(time=example_time_index),
            ds.PCA_VALUES.isel(pca=0)
            .differentiate(cst.Y_COORD)
            .mean(dim=cst.T_COORD, skipna=True),
            uvel_ds.UVEL.mean(dim=cst.T_COORD, skipna=True),
        ],
        ["PC1 y-grad", r"$U$ (m s$^{-1}$)", "PC1 y-grad", r"$U$ (m s$^{-1}$)"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_y_grad.png"
    )
    plt.savefig(pc_y_grad_name, dpi=900, bbox_inches="tight")
    plt.clf()
    uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=15)
    pca_ds = (
        xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-5-d-3.nc")
        .isel(pca=0)
        .differentiate(cst.Y_COORD)
    )

    cor_list = []

    for time_i in range(0, 60):
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
    plt.savefig(pc_y_grad_name, dpi=900, bbox_inches="tight")
    plt.clf()

    cor = ma.corrcoef(
        ma.masked_invalid(
            uvel_ds.mean(dim=cst.T_COORD, skipna=True).UVEL.values.ravel()
        ),
        ma.masked_invalid(
            pca_ds.mean(dim=cst.T_COORD, skipna=True).PCA_VALUES.values.ravel()
        ),
    )
    print(cor)

    vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=15)
    pca_ds = (
        xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
        .isel(pca=0)
        .differentiate(cst.X_COORD)
    )

    cor_list = []

    for time_i in range(0, 60):
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
    plt.savefig(pc_x_grad_name, dpi=900, bbox_inches="tight")
    plt.clf()

    vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=15)
    xp.sep_plots(
        [
            ds.PCA_VALUES.isel(time=example_time_index, pca=0).differentiate(
                cst.X_COORD
            ),
            vvel_ds.VVEL.isel(time=example_time_index),
            ds.PCA_VALUES.isel(pca=0)
            .differentiate(cst.X_COORD)
            .mean(dim=cst.T_COORD, skipna=True),
            vvel_ds.VVEL.mean(dim=cst.T_COORD, skipna=True),
        ],
        ["PC1 x-grad", r"$V$ (m s$^{-1}$)", "PC1 x-grad", r"$V$ (m s$^{-1}$)"],
    )
    pc_y_grad_name = os.path.join(
        cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_x_grad.png"
    )
    plt.savefig(pc_y_grad_name, dpi=900, bbox_inches="tight")
    plt.clf()
