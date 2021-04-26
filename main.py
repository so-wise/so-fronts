"""Run key scripts."""
import src.make_figures as mf
import src.move_figures as mov

mf.make_all_figures()

mov.move()

# import src.plotting_utilities.ko_plot as ko

# ko.run_so_map()

# pylint: disable=pointless-string-statement
"""
# import hydra
# from src import constants
# from src.configs import config
# import os
# import src.plotting_utilities.cluster_profiles as cp
# import src.models.train_i_metric as tim
# import src.constants as cst
# import xarray as xr
temp_name = os.path.join(cst.DATA_PATH, "run_" + cst.RUN_NAME + "temp.nc")
profiles_name = os.path.join(cst.DATA_PATH, "run_" + cst.RUN_NAME + "profiles_temp.nc")
m, ds = tim.train_on_interpolated_year(
    time_i=42,
    K=5,
    maxvar=3,
    min_depth=300,
    max_depth=2000,
    separate_pca=False,
    remove_init_var=False,
)
ds.to_netcdf(path=temp_name)
ds = xr.open_dataset(temp_name)
profile_ds = cp.make_cluster_profiles(ds)
profile_ds.to_netcdf(path=profiles_name)
profile_ds = xr.open_dataset(profiles_name)
print(profile_ds)
cp.plot_profiles_dataset(profile_ds)
s3d.plot_fig2_mult(
    m._classifier.weights_, m._classifier.means_, m._classifier.covariances_, ds
)
plt.show()
plt.clf()
# cp.profile_plot_cluster_comparison(ds)
# print(ds)
"""
