"""Make graphs to show how the preprocessing step has worked.

These are graphs B1 and B2 in appendix B of the paper."""
import numpy as np
import matplotlib.pyplot as plt
import pyxpcm
import src.plot_utils.gen_panels as gp
import src.plot_utils.latex_style as lsty
from src.constants import ZS, LZ


def mean_std_plot(pcm_ob: pyxpcm.pcm) -> None:
    """Plot the mean and the standard deviation of the profiles.

    Args:
        pcm_ob (pyxpcm.pcm): The fitted pyxpcm object.
    """
    _, axs = plt.subplots(1, 2, sharey=True)
    mn = pcm_ob._scaler["THETA"].mean_
    std = np.sqrt(pcm_ob._scaler["THETA"].var_)
    axs[0].plot(mn, ZS)
    axs[0].set_xlabel(r"Temperature [$^{\circ}$C]")
    axs[0].set_ylabel(r"Depth [m]")
    axs[0].fill_betweenx(ZS, mn - std, mn + std, alpha=0.5)
    mn = pcm_ob._scaler["SALT"].mean_
    std = np.sqrt(pcm_ob._scaler["SALT"].var_)
    axs[1].plot(mn, ZS, label="Mean of samples")
    axs[1].set_xlabel(r"Salinity [psu]")
    axs[1].fill_betweenx(
        ZS, mn - std, mn + std, alpha=0.5, label="Standard deviation of samples"
    )
    axs[0].set_ylim(min(ZS), max(ZS))
    gp.label_subplots(axs, x_pos=-0.05, y_pos=1.1, fontsize=14)
    axs[1].legend(
        bbox_to_anchor=(0, 1.05, 0, 0),
        loc="lower right",
        ncol=2,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )


def pauth17_pca_profiles(pcm_ob: pyxpcm.pcm) -> None:
    """Pauthenet and Roquet 2017 Figure 4 replication.

    Args:
        pcm_ob (pyxpcm.pcm): The profile classification model.
    """
    fig, axs = plt.subplots(2, 3, sharey=True)
    std = np.sqrt(pcm_ob._scaler["THETA"].var_)
    mn = pcm_ob._scaler["THETA"].mean_
    axs[0, 0].plot(mn, ZS, color="black", label="Mean")
    axs[0, 1].plot(mn, ZS, color="black")
    axs[0, 2].plot(mn, ZS, color="black")
    axs[0, 0].plot(
        mn + std * pcm_ob._reducer["all"].components_[0, LZ:],
        ZS,
        color="red",
        label="+1 Unit of PC",
    )
    axs[0, 1].plot(
        mn + std * pcm_ob._reducer["all"].components_[1, LZ:], ZS, color="red"
    )
    axs[0, 2].plot(
        mn + std * pcm_ob._reducer["all"].components_[2, LZ:], ZS, color="red"
    )
    axs[0, 0].plot(
        mn - std * pcm_ob._reducer["all"].components_[0, LZ:],
        ZS,
        color="blue",
        label="-1 Unit of PC",
    )
    axs[0, 1].plot(
        mn - std * pcm_ob._reducer["all"].components_[1, LZ:], ZS, color="blue"
    )
    axs[0, 2].plot(
        mn - std * pcm_ob._reducer["all"].components_[2, LZ:], ZS, color="blue"
    )
    axs[0, 0].set_ylim(min(ZS), max(ZS))
    axs[0, 0].set_ylabel("Depth [m]")
    axs[0, 0].set_xlabel("PC1")
    axs[0, 1].set_xlabel("PC2")
    axs[0, 2].set_xlabel("PC3")
    std = np.sqrt(pcm_ob._scaler["SALT"].var_)
    mn = pcm_ob._scaler["SALT"].mean_
    axs[1, 0].plot(mn, ZS, color="black")
    axs[1, 1].plot(mn, ZS, color="black")
    axs[1, 2].plot(mn, ZS, color="black")
    axs[1, 0].plot(
        mn + std * pcm_ob._reducer["all"].components_[0, :LZ], ZS, color="red"
    )
    axs[1, 1].plot(
        mn + std * pcm_ob._reducer["all"].components_[1, :LZ], ZS, color="red"
    )
    axs[1, 2].plot(
        mn + std * pcm_ob._reducer["all"].components_[2, :LZ], ZS, color="red"
    )
    axs[1, 0].plot(
        mn - std * pcm_ob._reducer["all"].components_[0, :LZ], ZS, color="blue"
    )
    axs[1, 1].plot(
        mn - std * pcm_ob._reducer["all"].components_[1, :LZ], ZS, color="blue"
    )
    axs[1, 2].plot(
        mn - std * pcm_ob._reducer["all"].components_[2, :LZ], ZS, color="blue"
    )
    axs[1, 0].set_ylabel("Depth [m]")
    axs[1, 0].set_xlabel("PC1")
    axs[1, 1].set_xlabel("PC2")
    axs[1, 2].set_xlabel("PC3")
    axs[1, 0].set_ylim(min(ZS), max(ZS))
    axs[0, 1].set_title(r"Potential Temperature, $\theta$ [$^{\circ}$C]")
    axs[1, 1].set_title(r"Salinity, $S$ [psu]")
    axs[0, 0].legend(
        bbox_to_anchor=(0.25, 1.1, 3, 0),
        loc="lower right",
        ncol=3,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    lsty.set_dim(fig, fraction_of_line_width=1.1, ratio=(5 ** 0.5 - 1) + 0.1)
    gp.label_subplots([axs[0, 0], axs[1, 0]], x_pos=-0.05, y_pos=1.1, fontsize=14)
    plt.tight_layout()


def pauth17_pca_profiles_new(pcm_ob: pyxpcm.pcm) -> None:
    """Pauthenet and Roquet 2017 Figure 4 replication [corrected].

    Args:
        pcm_ob (pyxpcm.pcm): The profile classification model.


    # Comment from Etienne:

    And I wrote this next code to plot the deviation from the mean profile,
    you add or remove ‘EOFs_realc’. You can add a factor in front if you want
     to exaggerate the deviation from the mean profile (and mention it in the
     caption, in Pauthenet2017 we multiply modes 3 to 6 by a factor 2 to amplify
      the deformation and make the figure readable).
    """
    # the pca object.
    reducer = pcm_ob._reducer["ALL"]
    comp = {}
    comp["SALT"] = reducer.components_[:, LZ:]
    comp["THETA"] = reducer.components_[:, :LZ]
    ev = reducer.explained_variance_

    # mean and variance containing objects
    scaler = {}
    scaler["SALT"] = pcm_ob._scaler["SALT"]
    scaler["THETA"] = pcm_ob._scaler["THETA"]

    mean = {}
    std_dev = {}
    for key in scaler:
        mean[key] = scaler[key].mean_
        std_dev[key] = np.sqrt(scaler[key].var_)

    row = {"THETA": 0, "SALT": 1}

    fig, axs = plt.subplots(len(row.keys()), len(ev), sharey=True)
    labels = {
        "mean": {},
        "minus": {"label": "-1 Unit of PC"},
        "plus": {"label": "-1 Unit of PC"},
    }

    first = True

    for quantity in row:
        axs[row[quantity], 0].set_ylim(min(ZS), max(ZS))
        axs[row[quantity], 0].set_ylabel("Depth [m]")
        for i in range(len(ev)):
            axs[row[quantity], i].plot(
                mean[quantity], ZS, color="black", **labels["mean"]
            )
            axs[row[quantity], i].plot(
                mean[quantity] - std_dev[quantity] * scaler[quantity][i, :],
                ZS,
                color="blue",
                **labels["minus"]
            )
            axs[row[quantity], i].plot(
                mean[quantity] + std_dev[quantity] * scaler[quantity][i, :],
                ZS,
                color="blue",
                **labels["plus"]
            )
            axs[row[quantity], i].set_xlabel("PC" + str(i + 1))
            if first == True:
                labels = {"mean": {}, "minus": {}, "plus": {}}
                first = False

    axs[0, 1].set_title(r"Potential Temperature, $\theta$ [$^{\circ}$C]")
    axs[1, 1].set_title(r"Salinity, $S$ [psu]")
    axs[0, 0].legend(
        bbox_to_anchor=(0.25, 1.1, 3, 0),
        loc="lower right",
        ncol=3,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    lsty.set_dim(fig, fraction_of_line_width=1.1, ratio=(5 ** 0.5 - 1) + 0.1)
    gp.label_subplots([axs[0, 0], axs[1, 0]], x_pos=-0.05, y_pos=1.1, fontsize=14)
    plt.tight_layout()

    S = np.sqrt(
        reducer.explained_variance_ * Xn.shape[0]
    )  # These are the singular values
    Z = np.dot(
        Xn - reducer.mean_, np.transpose(reducer.components_)
    )  # This is simply Xr or the principal components
    Ztilde = Z / np.sqrt(S)  # Normalized PCs
    EOFs_realc = (
        np.dot(np.transpose(Ztilde), Xc) / Xc.shape[0]
    )  # Regression on any collection of profiles

    # Indexes to retrieve either Temperature or Salinity (for the plot)
    nd = 1001
    nn = np.array([range(0, nd), range(nd, (nd * 2))])
    fig, ax = plt.subplots(
        nrows=3,
        ncols=2,
        figsize=(8, 15),
        dpi=80,
        facecolor="w",
        edgecolor="k",
        sharey="row",
    )
    for ie in range(0, 3):  # Three first PCs
        for dd in range(0, 2):  # Temperature and salinity
            ax[ie, dd].plot(
                np.transpose(
                    scaler.mean_[
                        nn[
                            dd,
                        ]
                    ]
                ),
                DPTmodel,
                c="black",
            )
            ax[ie, dd].plot(
                np.transpose(
                    scaler.mean_[
                        nn[
                            dd,
                        ]
                    ]
                    + EOFs_realc[
                        ie,
                        [
                            nn[
                                dd,
                            ]
                        ],
                    ]
                ),
                DPTmodel,
                c="red",
            )
            ax[ie, dd].plot(
                np.transpose(
                    scaler.mean_[
                        nn[
                            dd,
                        ]
                    ]
                    - EOFs_realc[
                        ie,
                        [
                            nn[
                                dd,
                            ]
                        ],
                    ]
                ),
                DPTmodel,
                c="blue",
            )
            if dd == 0:
                ax[ie, dd].set_xlim([4, 26])
            if dd == 1:
                ax[ie, dd].set_xlim([34.8, 37.1])
            ax[ie, dd].set_ylabel("Depth")
            ax[ie, dd].grid(True)
            ax[ie, dd].set_title(
                "PC%i (%i %%)" % (ie + 1, round(np.array(V * 100)[ie], 1))
            )
    ax[2, 0].set_xlabel("Temperature (real units)")
    ax[2, 1].set_xlabel("Salinity (real units)")
