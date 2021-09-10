"""Make graphs to show how the preprocessing step has worked."""
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
    axs[1].legend(
        bbox_to_anchor=(0, 1.05, 0, 0),
        loc="lower right",
        ncol=2,
        mode="expand",
        borderaxespad=0.0,
        frameon=False,
    )
    axs[0].set_ylim(min(ZS), max(ZS))
    gp.label_subplots(axs,x_pos=-0.05, y_pos=1.1, fontsize=14)

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
        mn + std * pcm_ob._reducer["all"].components_[0, :LZ],
        ZS,
        color="red",
        label="+1 Unit of PC",
    )
    axs[0, 1].plot(mn + std * pcm_ob._reducer["all"].components_[1, :LZ], ZS, color="red")
    axs[0, 2].plot(mn + std * pcm_ob._reducer["all"].components_[2, :LZ], ZS, color="red")
    axs[0, 0].plot(
        mn - std * pcm_ob._reducer["all"].components_[0, :LZ],
        ZS,
        color="blue",
        label="-1 Unit of PC",
    )
    axs[0, 1].plot(mn - std * pcm_ob._reducer["all"].components_[1, :LZ], ZS, color="blue")
    axs[0, 2].plot(mn - std * pcm_ob._reducer["all"].components_[2, :LZ], ZS, color="blue")
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
    axs[1, 0].plot(mn + std * pcm_ob._reducer["all"].components_[0, LZ:], ZS, color="red")
    axs[1, 1].plot(mn + std * pcm_ob._reducer["all"].components_[1, LZ:], ZS, color="red")
    axs[1, 2].plot(mn + std * pcm_ob._reducer["all"].components_[2, LZ:], ZS, color="red")
    axs[1, 0].plot(mn - std * pcm_ob._reducer["all"].components_[0, LZ:], ZS, color="blue")
    axs[1, 1].plot(mn - std * pcm_ob._reducer["all"].components_[1, LZ:], ZS, color="blue")
    axs[1, 2].plot(mn - std * pcm_ob._reducer["all"].components_[2, LZ:], ZS, color="blue")
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
    lsty.set_dim(fig, fraction_of_line_width=1.1, ratio=(5 ** 0.5 - 1)+0.1)
    gp.label_subplots([axs[0,0], axs[1, 0]],x_pos=-0.05, y_pos=1.1, fontsize=14)
    plt.tight_layout()
