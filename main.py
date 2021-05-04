"""Run key scripts."""
import src.make_figures as mf
import src.move_figures as mov

# from src.animate import animate_imetric

mf.make_all_figures()

mov.move()

# import src.plotting_utilities.ko_plot as ko

# ko.run_so_map()

# animate_imetric(video_path="gifs/boundaries-k2.gif", k_clusters=2)
# animate_imetric(video_path="gifs/boundaries-k4.gif", k_clusters=4)
# animate_imetric(video_path="gifs/boundaries-k5.gif", k_clusters=5)
# animate_imetric(video_path="gifs/boundaries-k5.mp4", k_clusters=5)
# animate_imetric(video_path="gifs/boundaries-k10.gif", k_clusters=10)
