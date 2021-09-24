"""Move figures."""
import os
import src.constants as cst
import src.time_wrapper as twr


@twr.timeit
def move(copy_command: str = "cp") -> None:
    """
    Move the files to the project.

    Args:
        copy_command (str, optional): which command is needed to move files in operating
            system. Defaults to "cp".

    """
    run_name = "010"
    final_loc = cst.FINAL_LOC
    fig_prefix = os.path.join(cst.FIGURE_PATH, "RUN_" + run_name)
    name_dict = {
        fig_prefix + "_pc_map" + cst.FIGURE_TYPE: "figure-1" + cst.FIGURE_TYPE,
        fig_prefix + "_s3d_clusters" + cst.FIGURE_TYPE: "figure-2" + cst.FIGURE_TYPE,
        fig_prefix + "_i_metric_dual" + cst.FIGURE_TYPE: "figure-3" + cst.FIGURE_TYPE,
        fig_prefix + "_map_i_comp" + cst.FIGURE_TYPE: "figure-4" + cst.FIGURE_TYPE,
        fig_prefix + "_profiles" + cst.FIGURE_TYPE: "figure-5" + cst.FIGURE_TYPE,
        fig_prefix + "_y_sobel" + cst.FIGURE_TYPE: "figure-6" + cst.FIGURE_TYPE,
        fig_prefix + "_i_metric_comp" + cst.FIGURE_TYPE: "figure-7" + cst.FIGURE_TYPE,
        fig_prefix + "_i_metric_single" + cst.FIGURE_TYPE: "figure-8" + cst.FIGURE_TYPE,
        fig_prefix + "_pc_y_sobel_comp" + cst.FIGURE_TYPE: "figure-A1" + cst.FIGURE_TYPE,
        fig_prefix + "_pc_y_sobel_corr" + cst.FIGURE_TYPE: "figure-A2" + cst.FIGURE_TYPE,
        fig_prefix + "_pc_x_sobel_comp" + cst.FIGURE_TYPE: "figure-A3" + cst.FIGURE_TYPE,
        fig_prefix + "_pc_x_sobel_corr" + cst.FIGURE_TYPE: "figure-A4" + cst.FIGURE_TYPE,
        fig_prefix + "_mean_plot" + cst.FIGURE_TYPE: "figure-B1" + cst.FIGURE_TYPE,
        fig_prefix + "_pca_real_space_plot" + cst.FIGURE_TYPE: "figure-B2" + cst.FIGURE_TYPE,
    }
    for key in name_dict:
        os.system(
            copy_command + " " + key + " " + os.path.join(final_loc, name_dict[key])
        )
