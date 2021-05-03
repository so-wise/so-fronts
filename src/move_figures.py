"""Move figures."""
import os
import src.constants as cst
import src.time_wrapper as twr


@twr.timeit
def move(copy_command: str = "cp") -> None:  # this is ok for unix.
    """
    Move the files to the project.

    Args:
        copy_command (str, optional): which command is needed to move files in operating
            system. Defaults to "cp".

    """
    run_name = "010"
    final_loc = "../FBSO/images"
    fig_prefix = os.path.join(cst.FIGURE_PATH, "RUN_" + run_name)
    name_dict = {
        fig_prefix + "_pc_map.png": "figure-1.png",
        fig_prefix + "_s3d_clusters.png": "figure-2.png",
        fig_prefix + "_i_metric_dual.png": "figure-3.png",
        fig_prefix + "_map_i_comp.png": "figure-4.png",
        fig_prefix + "_profiles.png": "figure-5.png",
        fig_prefix + "_y_sobel.png": "figure-6.png",
        fig_prefix + "_i_metric_comp.png": "figure-7.png",
        fig_prefix + "_i_metric_single.png": "figure-8.png",
        fig_prefix + "_y_sobel.png": "_pc_y_sobel_grad_comp.png",
        fig_prefix + "_pc_y_grad_corr.png": "figure-A2.png",
        fig_prefix + "_pc_x_sobel_grad_comp.png": "figure-A3.png",
        fig_prefix + "_pc_x_grad_corr.png": "figure-A4.png",
    }
    for key in name_dict:
        os.system(
            copy_command + " " + key + " " + os.path.join(final_loc, name_dict[key])
        )
