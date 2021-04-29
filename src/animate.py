"""Animate da."""
import os
from typing import Callable
import numpy as np
import xarray as xr
from tqdm import tqdm
import matplotlib.pyplot as plt
import imageio
from src.plot_utils.gen_panels import time_title
from src.plot_utils.latex_style import mpl_params
import src.plot_utils.xarray_panels as xp
import src.constants as cst
import src.data_loading.io_name_conventions as io

mpl_params(use_tex=False, dpi=200)


# @timeit
def animate_imetric(
    video_path: str = "output.gif",
) -> None:
    """Animate an `xr.DataArray`.

    Args:
        video_path (str, optional): Video path. Defaults to "output.mp4".
    """

    def gen_frame_func() -> Callable:
        """Create imageio frame function for `xarray.DataArray` visualisation.

        Returns:
            make_frame (Callable): function to create each frame.
        """

        def make_frame(index: int) -> np.array:
            """Make an individual frame of the animation.

            Args:
                index (int): The time index.

            Returns:
                image (np.array): np.frombuffer output that can be fed into imageio
            """
            fig, ax1 = plt.subplots(1, 1)

            da = io.return_pair_i_metric(k_clusters=cst.K_CLUSTERS, t_index=index)
            xp.plot_single_i_metric(da.isel(time=0))
            time_title(ax1, da.time.values[0])
            plt.tight_layout()

            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            plt.close()

            return image

        return make_frame

    def xarray_to_video(
        video_path: str,
        fps: int = 5,
    ) -> None:
        """Generate video of an `xarray.DataArray`.

        Args:
            video_path (str, optional): output path to save.
            fps (int, optional): frames per second.
        """
        video_indices = list(range(59))
        make_frame = gen_frame_func()
        imageio.mimsave(
            video_path,
            [make_frame(index) for index in tqdm(video_indices, desc=video_path)],
            fps=fps,
        )
        print("Video " + video_path + " made.")

    xarray_to_video(video_path, fps=5)


if __name__ == "__main__":
    animate_imetric(video_path="output2.gif")
    # python3 src/animate.py
