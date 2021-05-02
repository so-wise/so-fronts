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
    name_dict = {
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_pc_map.png"
        ): "figure-1.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_s3d_clusters.png"
        ): "figure-2.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_i_metric_dual.png"
        ): "figure-3.png",
        os.path.join(
            cst.FIGURE_PATH,
            "RUN_" + run_name + "_map_i_comp.png",
        ): "figure-4.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_profiles.png"
        ): "figure-5.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_y_sobel.png"
        ): "figure-6.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_i_metric_comp.png"
        ): "figure-7.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_i_metric_single.png"
        ): "figure-8.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_y_sobel.png"
        ): "figure-A1.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_pc_y_grad_corr.png"
        ): "figure-A2.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_x_sobel.png"
        ): "figure-A3.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + run_name + "_pc_x_grad_corr.png"
        ): "figure-A4.png",
    }
    for key in name_dict:
        os.system(
            copy_command + " " + key + " " + os.path.join(final_loc, name_dict[key])
        )
