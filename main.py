import src.models.train_i_metric


m, ds = src.models.train_i_metric.train_on_interpolated_year(
    time_i=42,
    K=5,
    maxvar=3,
    min_depth=300,
    max_depth=2000,
    separate_pca=False,
    remove_s_and_t=True,
)

print(ds)
