"""
make_figures.py

Every plot made in the exploratory notebook should be made
by this code (ideally).

This would require the data to have been made and put in the
right place.

TODO: It would also require the functions to be rewritten with imports
relating to the new repository.

TODO: change from hard coded to non-hardcoded links.

i.e move most of the file-names to the first repository.
"""
import os
import numpy as np
import numpy.ma as ma
import xarray as xr
import matplotlib.pyplot as plt
import src.plotting_utilities as pu
import src.data_loading.bsose_loading as bl
import src.constants as cst
import src.plotting_utilities.latex_style as lsty
import src.plotting_utilities.xarray_panels as xp
import src.models.train_i_metric as tim
import src.plotting_utilities.spec_i_clusters_3d_comp as s3d
import src.plotting_utilities.cluster_profiles as cp
import src.models.to_pair_i_metric as tpi

# import src.plotting_utilities.

# import src.plotting_utilities.
import src.data_loading.io_name_conventions as io


def return_pair_i_metric(K=5, pca=3, save_nc=True):

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
            da = xr.open_dataset(
                io._return_pair_folder(K, pca) + str(i) + ".nc"
            ).to_array()

    return da


def make_all_figures_in_sequence():

    # FIGURE 1

    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")

    da_temp = ds.PCA_VALUES.isel(time=40)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1", "PC2", "PC3"],
    )
    plt.savefig("../FBSO-Report/images/fig1-new.png", dpi=900, bbox_inches="tight")

    plt.clf()

    ##### FIGURE 1.5 ## make panels.
    temp_name = os.path.join(cst.DATA_PATH, "RUN_" + cst.RUN_NAME + "_temp.nc")
    profiles_name = os.path.join(
        cst.DATA_PATH, "RUN_" + cst.RUN_NAME + "_profiles_temp.nc"
    )
    m, ds = tim.train_on_interpolated_year(
        time_i=42,
        K=5,
        maxvar=3,
        min_depth=300,
        max_depth=2000,
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
    plt.clf()

    # FIGURE 2
    s3d.plot_fig2_mult(
        m._classifier.weights_, m._classifier.means_, m._classifier.covariances_, ds
    )
    plt.clf()

    ##### FIGURE 3
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
    xp.sep_plots(
        [
            ds.IMETRIC.isel(Imetric=0, time=40),
            ds.IMETRIC.isel(Imetric=0).mean(dim=cst.TIME_NAME, skipna=True),
        ],
        ["$\mathcal{I}$-metric ", "$\mathcal{I}$-metric"],
    )
    plt.savefig("../FBSO-Report/images/fig3-new.png", dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 4
    da = return_pair_i_metric(K=5)
    xp.plot_single_i_metric(da.isel(time=0))
    plt.savefig("../FBSO-Report/images/fig4-new.png", dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 5
    xp.plot_several_pair_i_metrics(
        [return_pair_i_metric(K=2).isel(time=0), return_pair_i_metric(K=4).isel(time=0)]
    )
    plt.tight_layout()
    plt.savefig("../FBSO-Report/images/fig5-new.png", dpi=900, bbox_inches="tight")
    plt.clf()

    # FIGURE 6
    da_temp = ds.PCA_VALUES.isel(time=40).differentiate(cst.Y_COORD)
    xp.sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1 y-grad", "PC2 y-grad", "PC3 y-grad"],
    )
    plt.savefig("../FBSO-Report/images/fig6-new.png", dpi=900, bbox_inches="tight")
    plt.clf()

    ### Appendix
    uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=15)
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
    plt.clf()

    xp.sep_plots(
        [
            ds.PCA_VALUES.isel(time=40, pca=0).differentiate(cst.Y_COORD),
            uvel_ds.UVEL.isel(time=40),
            ds.PCA_VALUES.isel(pca=0)
            .differentiate(cst.Y_COORD)
            .mean(dim=cst.TIME_NAME, skipna=True),
            uvel_ds.UVEL.mean(dim=cst.TIME_NAME, skipna=True),
        ],
        ["PC1 y-grad", r"$U$ (m s$^{-1}$)", "PC1 y-grad", r"$U$ (m s$^{-1}$)"],
    )

    plt.savefig(
        "../FBSO-Report/images/compare-sobel-with-U.png", dpi=900, bbox_inches="tight"
    )
    plt.clf()

    uvel_ds = xr.open_dataset(cst.UVEL_FILE).isel(Z=15)
    pca_ds = (
        xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
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

    plt.plot(range(0, 60), cor_list)
    plt.xlabel("Time")
    plt.ylabel("Correlation coefficient")
    plt.xlim([0, 59])
    plt.title("Correlation between PC1 y-grad and $U$")
    # plt.savefig('')

    plt.clf()

    cor = ma.corrcoef(
        ma.masked_invalid(
            uvel_ds.mean(dim=cst.TIME_NAME, skipna=True).UVEL.values.ravel()
        ),
        ma.masked_invalid(
            pca_ds.mean(dim=cst.TIME_NAME, skipna=True).PCA_VALUES.values.ravel()
        ),
    )
    print(cor)

    vvel_ds = xr.open_dataset(cst.VVEL_FILE).isel(Z=15)
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
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

    plt.plot(range(0, 60), cor_list)
    plt.xlabel("Time")
    plt.ylabel("Correlation coefficient")
    plt.xlim([0, 59])
    plt.title("Correlation between PC1 x-grad and $V$")
    plt.clf()
