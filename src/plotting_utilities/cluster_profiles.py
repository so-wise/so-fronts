import numpy as np
import matplotlib.pyplot as plt
import src.plotting_utilities.latex_style as lsty
import src.plotting_utilities.colors as col
import src.time_wrapper as twr


@twr.timeit
def profile_plot_cluster_comparison(ds):
    """

    :param ds: the dataset

    Dimensions:     (Imetric: 1, XC: 240, YC: 60, Z: 52, pca: 3, rank: 2, time: 12)
    Coordinates:
      * time        (time) datetime64[ns] 2011-08-01T15:12:00 ... 2012-07-01T09:36:00
      * Z           (Z) float32 -2.1 -6.7 -12.15 -18.55 ... -5000.0 -5400.0 -5800.0
      * YC          (YC) float64 -77.98 -77.16 -76.35 ... -31.35 -30.53 -29.72
      * XC          (XC) float64 0.08333 1.589 3.094 4.6 ... 355.4 356.9 358.4 359.9
    Dimensions without coordinates: Imetric, pca, rank
    Data variables:
        SALT        (time, Z, YC, XC) float64 nan nan nan nan ... 0.0 0.0 0.0 0.0
        THETA       (time, Z, YC, XC) float64 nan nan nan nan ... 0.0 0.0 0.0 0.0
        PCA_VALUES  (pca, time, YC, XC) float64 nan nan nan ... 8.643 9.195 8.525
        IMETRIC     (Imetric, time, YC, XC) float64 nan nan nan nan ... 0.0 0.0 0.0
        A_B         (rank, time, YC, XC) float64 nan nan nan nan ... 4.0 4.0 4.0 4.0
        PCM_LABELS  (time, YC, XC) float64 nan nan nan nan nan ... 3.0 3.0 3.0 3.0

    Originally from
    https://scitools.org.uk/iris/docs/v1.6/examples/graphics/atlantic_profiles.html
    A program to plot profiles, originally of the original components etc.
    https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html

    df.insert(3,'label_sorted',df['label'].map(di))

    # group profiles according to label
    grouped = df.groupby('label_sorted')

    # calculate mean of all profiles in each class
    dfg_means = grouped.mean()

    # calculate stdevs of all profiles in each class
    dfg_stds = grouped.std()

    # number or profiles in each class
    nprofs = grouped['x'].count().values

    print(dfg_means['15.0'])

    """
    fig = plt.gcf()

    # color_list = col.replacement_color_list(len(data_d["theta_d"].values()))

    plt.subplot(1, 2, 1)

    ax1 = plt.gca()

    """

    for key in data_d["depths_d"]:
        assert len(data_d["depths_d"][key]) == len(data_d["theta_d"][key])
        plt.plot(
            data_d["theta_d"][key],
            [x / 1000 for x in data_d["depths_d"][key]],
            mt_list[int(key)],
            color=color_list[-1 - int(key)],
            linewidth=1.0,
            markersize=1.4,
            alpha=0.5,
            label=("Cluster " + str(key + 1)),
        )

        std_dev = [np.sqrt(np.abs(x)) for x in data_d["theta_variance_d"][key]]

        for sig_mult, alpha in [[1, 0.4]]:  # [2, 0.2], [3, 0.1], [4, 0.1]
            plt.fill_betweenx(
                [x / 1000 for x in data_d["depths_d"][key]],
                data_d["theta_d"][key] - np.multiply(sig_mult, std_dev),
                data_d["theta_d"][key] + np.multiply(sig_mult, std_dev),
                alpha=alpha,
                color=color_list[-1 - int(key)],
            )

    if "theta_mean_vec" in data_d:
        plt.plot(
            data_d["theta_mean_vec"],
            [x / 1000 for x in data_d["depths_d"][key]],
            ",-",
            color="grey",
            alpha=0.5,
            label="Mean Profile",
        )
    """

    ax1.set_xlabel(
        r"Potential Temperature, $\theta$ / $^{\circ}\mathrm{C}$", color="black"
    )
    ax1.set_ylabel("(Negative) Depth / km")

    plt.ylim([-2.008, 0])

    plt.subplot(1, 2, 2)
    ax2 = plt.gca()

    """

    for key in data_d["depths_d"]:

        assert len(data_d["depths_d"][key]) == len(data_d["salinity_d"][key])
        plt.plot(
            data_d["salinity_d"][key],
            [x / 1000 for x in data_d["depths_d"][key]],
            mt_list[int(key)],
            color=color_list[-1 - int(key)],
            linewidth=1.0,
            markersize=1.4,
            alpha=0.5,
            label="Cluster " + str(key + 1) + r"-$S$",
        )
        std_dev = [np.sqrt(np.abs(x)) for x in data_d["salinity_variance_d"][key]]

        for sig_mult, alpha in [[1, 0.4]]:  # [2, 0.2], [3, 0.1], [4, 0.1]
            plt.fill_betweenx(
                [x / 1000 for x in data_d["depths_d"][key]],
                data_d["salinity_d"][key] - np.multiply(sig_mult, std_dev),
                data_d["salinity_d"][key] + np.multiply(sig_mult, std_dev),
                alpha=alpha,
                color=color_list[-1 - int(key)],
            )

    if "salt_mean_vec" in data_d:
        plt.plot(
            data_d["salt_mean_vec"],
            [x / 1000 for x in data_d["depths_d"][key]],
            ",-",
            color="grey",
            alpha=0.5,
            label="Mean Profile",
        )
    """

    ax2.set_xlabel(r"Salinity, $S$ / PSU", color="black")
    plt.ylim([-2.008, 0])
    plt.yticks([])
    plt.setp(ax2.get_yticklabels(), visible=False)

    ax1.legend(
        bbox_to_anchor=(0.0, 1.02, 2.05, 0.102),
        loc="lower left",
        ncol=2,
        mode="expand",
        borderaxespad=0.0,
    )

    plt.tight_layout()
    # plt.savefig(style_d["file_name"], bbox_inches="tight")
    # plt.clf()
    plt.show()
