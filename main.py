# import hydra
from src import constants

# from src.configs import config
import src.plotting_utilities.cluster_profiles as cp
import src.models.train_i_metric as tim

# import src.make_figures as mf

import matplotlib.pyplot as plt

# mf.make_all_figures_in_sequence()

m, ds = tim.train_on_interpolated_year(
    time_i=42,
    K=5,
    maxvar=3,
    min_depth=300,
    max_depth=2000,
    separate_pca=False,
    remove_init_var=False,
)

cp.profile_plot_cluster_comparison(ds)

"""

s3d.plot_fig2_mult(
    m._classifier.weights_, m._classifier.means_, m._classifier.covariances_, ds
)
plt.show()
plt.clf()
"""

# cp.profile_plot_cluster_comparison(ds)

# print(ds)
