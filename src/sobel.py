"""Test sobel vs gradient."""
import os
from typing import Tuple
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cmocean.cm as cmo
import src.constants as cst
import src.plot_utils.xarray_panels as xp
import src.time_wrapper as twr
from scipy import signal


def sobel_np(values: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sobel operator on np array.

    Args:
         values (np.ndarray): values to differentiate.

    Returns:
        Tuple[np.ndarray, np.ndarray]: gx, gy
    """
    sobel = np.array(
        [
            [1 + 1j, 0 + 2j, -1 + 1j],
            [2 + 0j, 0 + 0j, -2 + 0j],
            [1 - 1j, 0 - 2j, -1 - 1j],
        ]
    )  # Gx + j*Gy
    grad = signal.convolve2d(values, sobel, boundary="pad", mode="same")
    return np.real(grad), np.imag(grad)


@twr.timeit
def sobel_vs_grad() -> None:
    """
    Sobel versus dimension.
    """
    ds = xr.open_dataset(cst.DEFAULT_NC)
    da_temp = ds.PCA_VALUES.isel(time=cst.EXAMPLE_TIME_INDEX)
    print(da_temp.isel(pca=0))
    print("shape", da_temp.isel(pca=0).values.shape)
    pc1_x = da_temp.isel(pca=0)
    pc1_x.values = sobel_np(pc1_x.values)[0]
    pc1_x.plot(vmin=-50, vmax=50, cmap=cmo.balance)
    plt.savefig("example-x.png")
    plt.clf()
    pc1_y = da_temp.isel(pca=0)
    pc1_y.values = sobel_np(pc1_y.values)[1]
    pc1_y.plot(vmin=-50, vmax=50, cmap=cmo.balance)
    plt.savefig("example-y.png")
    xp.sep_plots([pc1_x, pc1_y], ["PC1 $G_x$", "PC1 $G_y$"], [[-40, 40], [-40, 40]])
    plt.savefig("example-pc.png")
    plt.clf()
    # print(sobel_np(da_temp.isel(pca=1).values)[0])
    # print(sobel_np(da_temp.isel(pca=2).values)[0])


def sobel_scharr_test():
    """Test scharr."""
    da = xr.DataArray(np.random.randn(15, 30), dims=[cst.X_COORD, cst.Y_COORD])
    # kernel = xr.DataArray(filter, dims=["kx", "ky"])
    # da_new = da.rolling(XC=3, YC=3).construct(XC="kx", YC="ky").dot(kernel)
    val = da.values
    print("val", val)

    # print(da_new)
    scharr = np.array(
        [
            [-3 - 3j, 0 - 10j, +3 - 3j],
            [-10 + 0j, 0 + 0j, +10 + 0j],
            [-3 + 3j, 0 + 10j, +3 + 3j],
        ]
    )  # Gx + j*Gy
    sobel = np.array(
        [
            [1 + 1j, 0 + 2j, -1 + 1j],
            [2 + 0j, 0 + 0j, -2 + 0j],
            [1 - 1j, 0 - 2j, -1 - 1j],
        ]
    )  # Gx + j*Gy

    for filt in [sobel, scharr]:

        grad = signal.convolve2d(val, filt, boundary="symm", mode="same")

        gx = np.real(grad)
        gy = np.imag(grad)

        print(gx)
        print(gy)
        # print(grad)

        _, (ax_orig, ax_mag, ax_ang) = plt.subplots(3, 1, figsize=(6, 15))
        ax_orig.imshow(val, cmap="gray")
        ax_orig.set_title("Original")
        ax_orig.set_axis_off()
        ax_mag.imshow(np.absolute(grad), cmap="gray")
        ax_mag.set_title("Gradient magnitude")
        ax_mag.set_axis_off()
        ax_ang.imshow(np.angle(grad), cmap="hsv")  # hsv is cyclic, like angles
        ax_ang.set_title("Gradient orientation")
        ax_ang.set_axis_off()
        # fig.show()
        plt.savefig("example.png")


def grad_v() -> None:
    """Gradient in v direction."""
    ds = xr.open_dataset(cst.DEFAULT_NC)
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


if __name__ == "__main__":
    sobel_vs_grad()
    # python3 src/sobel.py
