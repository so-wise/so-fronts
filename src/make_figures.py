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
import src.plotting_utilities as pu
import src.data_loading.bsose_loading as bl


if __name__ == "main":

    da = run_through_plot(K=5)
    plot_on_one(da.isel(time=0))
    plt.savefig("../FBSO-Report/images/fig4-new.png", dpi=900, bbox_inches="tight")
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")

    da_temp = ds.PCA_VALUES.isel(time=40)
    sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1", "PC2", "PC3"],
    )
    plt.savefig("../FBSO-Report/images/fig1-new.png", dpi=900, bbox_inches="tight")

    sep_plots(
        [
            ds.IMETRIC.isel(Imetric=0, time=40),
            ds.IMETRIC.isel(Imetric=0).mean(dim="time", skipna=True),
        ],
        ["$\mathcal{I}$-metric ", "$\mathcal{I}$-metric"],
    )
    plt.savefig("../FBSO-Report/images/fig3-new.png", dpi=900, bbox_inches="tight")

    da_temp = ds.PCA_VALUES.isel(time=40).differentiate("YC")
    sep_plots(
        [da_temp.isel(pca=0), da_temp.isel(pca=1), da_temp.isel(pca=2)],
        ["PC1 y-grad", "PC2 y-grad", "PC3 y-grad"],
    )
    plt.savefig("../FBSO-Report/images/fig6-new.png", dpi=900, bbox_inches="tight")

    ### Appendix
    main_dir = "/Users/simon/fbso/fbso/bsose_monthly/"
    uvel = main_dir + "bsose_i106_2008to2012_monthly_Uvel.nc"
    uvel_ds = xr.open_dataset(uvel).isel(Z=15)
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")

    sep_plots(
        [
            ds.PCA_VALUES.isel(time=40, pca=0).differentiate("YC"),
            uvel_ds.UVEL.isel(time=40),
            ds.PCA_VALUES.isel(pca=0).differentiate("YC").mean(dim="time", skipna=True),
            uvel_ds.UVEL.mean(dim="time", skipna=True),
        ],
        ["PC1 y-grad", r"$U$ (m s$^{-1}$)", "PC1 y-grad", r"$U$ (m s$^{-1}$)"],
    )

    plt.savefig(
        "../FBSO-Report/images/compare-sobel-with-U.png", dpi=900, bbox_inches="tight"
    )
    uvel_ds = xr.open_dataset(uvel).isel(Z=15)
    pca_ds = (
        xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
        .isel(pca=0)
        .differentiate("YC")
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

    cor = ma.corrcoef(
        ma.masked_invalid(uvel_ds.mean(dim="time", skipna=True).UVEL.values.ravel()),
        ma.masked_invalid(
            pca_ds.mean(dim="time", skipna=True).PCA_VALUES.values.ravel()
        ),
    )
    print(cor)

    main_dir = "/Users/simon/fbso/fbso/bsose_monthly/"
    vvel = main_dir + "bsose_i106_2008to2012_monthly_Vvel.nc"
    vvel_ds = xr.open_dataset(vvel).isel(Z=15)
    ds = xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
    pca_ds = (
        xr.open_dataset("~/pyxpcm/nc/i-metric-joint-k-4-d-3.nc")
        .isel(pca=0)
        .differentiate("XC")
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
