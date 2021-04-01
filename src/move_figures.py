import os
import src.constants as cst
import src.time_wrapper as twr


@twr.timeit
def move(copy_command: str = "cp") -> None:  # this is ok for unix.
    RUN_NAME = "001"
    final_loc = "../FBSO-Report/images"
    name_dict = {
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_pc_map.png"
        ): "fig1-new.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_profiles.png"
        ): "fig1.5-new.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_s3d_clusters.png"
        ): "fig2-new.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_i_metric_dual.png"
        ): "fig3-new.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_i_metric_single.png"
        ): "fig4-new.png",
        os.path.join(
            cst.FIGURE_PATH,
            "RUN_"
            + "010"
            + "_map_i_comp.png",  # "RUN_" + cst.RUN_NAME + "_map_i_comp.png"
        ): "fig4-comp.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_i_metric_comp.png"
        ): "fig5-new.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + RUN_NAME + "_y_grad.png"
        ): "fig6-new.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_y_grad.png"
        ): "figA1.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_y_grad_corr.png"
        ): "figA2.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_x_grad_corr.png"
        ): "figA3.png",
        os.path.join(
            cst.FIGURE_PATH, "RUN_" + cst.RUN_NAME + "_pc_x_grad.png"
        ): "figA4.png",
    }
    for key in name_dict:
        os.system(
            copy_command + " " + key + " " + os.path.join(final_loc, name_dict[key])
        )
