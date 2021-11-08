"""Run key scripts."""
# from src.animate import animate_imetric
import src.move_figures as mov
import src.make_figures as mf

mf.make_all_figures()
mov.move()

# animate_imetric(video_path="gifs/boundaries-k5.gif", k_clusters=5)
# animate_imetric(video_path="gifs/boundaries-k4.gif", k_clusters=4)
# animate_imetric(video_path="gifs/boundaries-k2.gif", k_clusters=2)

"""
git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch
figures/RUN_010_pc_x_sobel_comp.pdf
figures/RUN_010_pc_y_sobel_comp.pdf
figures/RUN_010_i_metric_comp.pdf
figures/RUN_010_y_sobel.pdf
figures/RUN_010_pc_map.pdf
figures/RUN_010_i_metric_comp.pdf
figures/RUN_010_i_metric_single.pdf
figures/RUN_010_map_i_comp.pdf
figures/RUN_010_x_sobel.pdf
figures/RUN_010_pc_map.pdf' -- --all
    """
