import src.models.train_i_metric
import src.plotting_utilities.spec_i_clusters_3d_comp as s3d

m, ds = src.models.train_i_metric.train_on_interpolated_year(
    time_i=42,
    K=5,
    maxvar=3,
    min_depth=300,
    max_depth=2000,
    separate_pca=False,
    remove_s_and_t=True,
)


s3d.plot_fig2_mult(
    m._classifier.weights_, m._classifier.means_, m._classifier.covariances_, ds
)
plt.show()

print(ds)
