"""Test sobel vs gradient."""
import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import src.constants as cst
import src.plot_utils.xarray_panels as xp
import src.time_wrapper as twr
from scipy import signal


@twr.timeit
def sobel_vs_grad() -> None:
    """
    Sobel versus dimension.
    """
    # filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    scharr_test()


def scharr_test():
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

        print(grad)
        fig, (ax_orig, ax_mag, ax_ang) = plt.subplots(3, 1, figsize=(6, 15))
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
