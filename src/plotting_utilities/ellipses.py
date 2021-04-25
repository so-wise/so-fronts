"""Ellipses."""
from typing import Tuple
import numpy as np
import numpy.linalg as la
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patches
import pyxpcm
import src.plotting_utilities.gen_panels as gp
import src.time_wrapper as twr


@twr.timeit
def plot_ellipsoid_test() -> None:
    """
    https://stackoverflow.com/questions/7819498/plotting-ellipsoid-with-matplotlib

    Plot ellipsoid test. Runs from unittest.

    """

    # your ellipsoid's covariance_matrix and mean in matrix form
    covariance_matrix: np.ndarray = np.array([[1, 0.5, 0], [0.2, 2, 0], [0, 0, 10]])
    covariance_matrix1: np.ndarray = np.array([[1, 0.1, 0], [0.2, 8, 0], [0, 0, 1]])

    mean: list = [-5, 0.3, 0.1]
    mean1: list = [0, -5, -4]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    fig = plot_ellipsoid(fig, ax, covariance_matrix, mean, 1, "b")
    plot_ellipsoid(fig, ax, covariance_matrix1, mean1, 1, "g")
    plt.xlabel("x")
    plt.ylabel("y")
    ax.set_zlabel("z")
    plt.tight_layout()
    plt.show()


@twr.timeit
def plot_ellipsoid(
    fig: matplotlib.figure.Figure,
    ax: matplotlib.axes.Axes,
    covariance_matrix: np.array,
    mean: np.array,
    weight: np.array,
    color: any,
    print_properties: bool = False,
    additional_rotation: np.array = np.identity(3),
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
    """
    A function for drawing 3d-multivariate guassians with method initially from:
    https://stackoverflow.com/questions/7819498/plotting-ellipsoid-with-matplotlib

    :param fig: The figure matplotlib.pyplot object
    :param ax: The axis matplotlib.pylot object with Axes3D extension
    :param covariance_matrix: A covariance matrix input from
        the multivariate guassian to be plotted.
    :param mean: ditto
    :param weight: ditto
    :param color: ditto
    :return: fig and ax so that they can be used by further plotting steps.
    """

    # I arbitrarily choose some levels to in the multivariate Gaussian to plot.

    if print_properties:
        print("weight", weight)
        print("mean", mean)
        print("covariance matrix", covariance_matrix)

    for sigma, alpha in [
        [3, 0.2 * weight],
        [2, 0.4 * weight],
        [1, 0.6 * weight],
    ]:
        # find the rotation matrix and radii of the axes
        _, s, rotation = la.svd(covariance_matrix)
        # Singular Value Decomposition from numpy.linalg
        # finds the variance vector s when the covariance
        # matrix has been rotated so that it is diagonal
        radii = np.sqrt(s) * sigma
        # s is the sigma*2 in each of the principal axes directions

        # now carry on with EOL's answer
        u = np.linspace(0.0, 2.0 * np.pi, 100)  # AZIMUTHAL ANGLE (LONGITUDE)
        v = np.linspace(0.0, np.pi, 100)  # POLAR ANGLE (LATITUDE)

        # COORDINATES OF THE SURFACE PRETENDING THAT THE
        # GAUSSIAN IS AT THE CENTRE & NON ROTATED
        x = radii[0] * np.outer(np.cos(u), np.sin(v))  # MESH FOR X
        y = radii[1] * np.outer(np.sin(u), np.sin(v))  # MESH FOR Y
        z = radii[2] * np.outer(np.ones_like(u), np.cos(v))  # MESH FOR Z

        # move so that the gaussian is actually rotated and on the right point.
        for i in range(len(x)):
            for j in range(len(x)):
                [x[i, j], y[i, j], z[i, j]] = (
                    np.dot([x[i, j], y[i, j], z[i, j]], rotation) + mean
                )
                [x[i, j], y[i, j], z[i, j]] = np.dot(
                    additional_rotation, [x[i, j], y[i, j], z[i, j]]
                )
        # plot the surface in a reasonable partially translucent way
        ax.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=alpha)

    return fig, ax


# plot_ellipsoid_trial()


def ellispes(pcm: pyxpcm.pcm, ax1: matplotlib.axes.Axes) -> None:
    """Plot ellipses.

    Args:
        pcm (pyxpcm.pcm): pcm object.
        ax1 (matplotlib.axes.Axes): axes.
    """
    # pylint: disable=protected-access
    for i in range(pcm._classifier.covariances_.shape[0]):
        # pylint: disable=protected-access
        weight = pcm._classifier.weights_[i]
        # pylint: disable=protected-access
        mean = pcm._classifier.means_[i]

        # pylint: disable=protected-access
        _, s, rotation = la.svd(pcm._classifier.covariances_[i])
        for frac_sigma, alpha in [
            [1 / 9, 0.5 * weight],
            [1 / 4, 0.7 * weight],
            [1, weight],
        ]:

            radii = np.sqrt(s / frac_sigma)
            angle = np.arctan2(rotation[1, 0], rotation[0, 0]) / np.pi * 180

            e1 = patches.Ellipse(
                mean,
                radii[0],
                radii[1],
                angle=angle,
                alpha=alpha,  # color=color_array[i]
            )
            ax1.add_patch(e1)
            gp.label_subplots([ax1], start_from=1)
