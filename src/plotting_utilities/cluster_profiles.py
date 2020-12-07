def profile_plot_cluster_comparison():
    """
    Originally from
    https://scitools.org.uk/iris/docs/v1.6/examples/graphics/atlantic_profiles.html
    A program to plot profiles, originally of the original components etc.
    https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
    """
    fig = plt.gcf()
    color_list = mps.replacement_color_list(len(data_d["theta_d"].values()))

    plt.subplot(1, 2, 1)

    ax1 = plt.gca()

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

    ax1.set_xlabel(
        r"Potential Temperature, $\theta$ / $^{\circ}\mathrm{C}$", color="black"
    )
    ax1.set_ylabel("(Negative) Depth / km")

    plt.ylim([-2.008, 0])

    plt.subplot(1, 2, 2)
    ax2 = plt.gca()

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
    plt.savefig(style_d["file_name"], bbox_inches="tight")
    plt.clf()
