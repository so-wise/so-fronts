from typing import Tuple, Sequence
import numpy as np
import xarray as xr
import src.data_loading.xr_values_loader as xvl
import src.constants as cst

xr.set_options(keep_attrs=True)


def make_all_pair_i_metric(
    cart_prod, i_metric, sorted_version, threshold
) -> Tuple[list]:
    if True:
        pair_i_metric_list = []

        pair_list = []

        for pair in cart_prod:
            print("pair", pair)
            temp_list = make_one_pair_i_metric(
                pair, i_metric, sorted_version, threshold
            )
            if temp_list[2] == True:
                pair_list.append(temp_list[0])
                pair_i_metric_list.append(temp_list[1])
            # time, YC, XC
            # shape (60, 2, 588, 2160)
    print("pair_list", pair_list)

    return pair_i_metric_list, pair_list


# @jit(nopython=True)
def make_one_pair_i_metric(
    pair, i_metric, sorted_version, threshold
) -> Sequence[np.array]:
    shape = np.shape(sorted_version)
    print("shape", shape)
    # shape (60, 2, 588, 2160)
    at_least_one_point = False
    # float32 changed from np.zeros
    pair_i_metric = np.zeros([shape[0], shape[2], shape[3]])  # , dtype='float64'
    pair_i_metric[:, :, :] = np.nan
    for i in range(shape[0]):  # 60
        for j in range(shape[2]):  # 588
            for k in range(shape[3]):  # 2160
                if np.array_equal(pair, sorted_version[i, :, j, k]):
                    # sorted_version (60, 2, 588, 2160)
                    if i_metric[i, j, k] >= threshold:
                        # i_metric (60, 588, 2160)
                        pair_i_metric[i, j, k] = i_metric[i, j, k]
                        at_least_one_point = True
    return [pair, pair_i_metric, at_least_one_point]


def pair_i_metric(ds: xr.Dataset, threshold: float = 0.05) -> xr.DataArray:
    """
    # new loading order (to be changed)
    ds.A_B.values.shape (2, 12, 60, 240)
    sorted_version.shape (2, 12, 60, 240)
    i_metric (12, 60, 240)
    list_no [0, 1, 2, 3, 4]
    https://numpy.org/doc/stable/reference/generated/numpy.swapaxes.html
    https://numpy.org/doc/stable/reference/generated/numpy.moveaxis.html
    "time"].values.shape[0]),
    ("rank", dataarray.coords["rank"].values.shape[0]),
    ("x", dataarray.coords["XC"].values.shape[0]),
    ("y", dataarray.coords["YC"]
    """

    A_B_values = xvl.order_indexes(
        ds.A_B, [cst.T_COORD, "rank", cst.Y_COORD, cst.X_COORD]
    )
    sorted_version = np.sort(A_B_values, axis=1)
    i_metric = xvl.order_indexes(
        ds.IMETRIC.isel(Imetric=0), [cst.T_COORD, cst.Y_COORD, cst.X_COORD]
    )
    print("i_metric", i_metric.shape)
    # i_metric (60, 588, 2160)
    list_no = [i for i in range(int(np.nanmax(sorted_version)) + 1)]
    print("list_no", list_no)
    cart_prod = [
        np.array([a, b]) for a in list_no for b in list_no if a <= b and a != b
    ]
    print("cart_prod", cart_prod)

    pair_i_metric_list, pair_list = make_all_pair_i_metric(
        cart_prod, i_metric, sorted_version, threshold
    )
    print("pair_i_metric_list", pair_i_metric_list)
    print("pair_i_metric_list len", len(pair_i_metric_list))
    print("pair_list", pair_list)
    print("pair_list len", len(pair_list))
    shape = np.shape(sorted_version)
    # shape (60, 2, 588, 2160)
    pair_i_metric_array = np.zeros(
        [len(pair_i_metric_list), shape[0], shape[2], shape[3]]
    )

    for i in range(len(pair_i_metric_list)):
        pair_i_metric_array[i, :, :, :] = pair_i_metric_list[i][:, :, :]

    pair_str_list = []

    for i in range(len(pair_list)):
        pair_str_list.append(
            str(pair_list[i][0] + 1) + " to " + str(pair_list[i][1] + 1)
        )

    da = xr.DataArray(
        pair_i_metric_array,
        dims=[cst.P_COORD, cst.T_COORD, cst.Y_COORD, cst.X_COORD],
        coords={
            cst.X_COORD: ds.coords[cst.X_COORD].values,
            cst.Y_COORD: ds.coords[cst.Y_COORD].values,
            cst.T_COORD: ds.coords[cst.T_COORD].values,
            cst.P_COORD: pair_str_list,
        },
    )

    return da
