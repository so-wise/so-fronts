import numpy as np
import gsw
import xarray as xr
import constants as cst

xr.set_options(keep_attrs=True)


def return_density(pt_values, practical_salt_values, lon_values, lat_values, z_values):
    """
    pt_values: grid
    pt_values: grid
    """

    lat_mesh, z_mesh = np.meshgrid(lat_values, z_values)
    pressure_mesh = gsw.p_from_z(z_mesh, lat_mesh)
    pressure_values = np.zeros(np.shape(pt_values))
    lat_grid = np.zeros(np.shape(pt_values))
    lon_grid = np.zeros(np.shape(pt_values))

    # TODO these two loops could be vectorized

    for i in range(np.shape(pt_values)[2]):
        pressure_values[:, :, i] = pressure_mesh[:, :]
        lat_grid[:, :, i] = lat_mesh[:, :]

    for i in range(np.shape(pt_values)[0]):
        for j in range(np.shape(pt_values)[1]):
            lon_grid[i, j, :] = lon_values[:]

    absolute_salinity = gsw.SA_from_SP(
        practical_salt_values, pressure_values, lon_grid, lat_grid
    )
    ct_values = gsw.conversions.CT_from_pt(absolute_salinity, pt_values)
    rho_values = gsw.density.rho(absolute_salinity, ct_values, pressure_values)

    # print(np.shape(rho_values))

    return rho_values, ct_values, pressure_values


def create_datarray(format_dataarray, values, name, v_attr_d):

    c_attr_d = {}
    coord_d = {}
    c_value_l = []
    dims_l = []
    for coord in format_dataarray.coords:
        if coord != "time":
            c_attr_d[coord] = format_dataarray.coords[coord].attrs
            c_value_l.append(format_dataarray.coords[coord].values)
            # dims_l.append(coord)

    # print(format_dataarray.dims)
    # print(c_value_l)
    c_value_l.reverse()

    # for item in c_value_l:
    #    print(np.shape(item))

    for dim_name in format_dataarray.dims:  # format_dataarray.dims:
        if dim_name != "time":
            coord_d[dim_name] = (dim_name, format_dataarray.coords[dim_name].values)

    da = xr.DataArray(
        values,
        dims=format_dataarray.dims,
        coords=coord_d
        # coords=c_value_l
    ).rename(name)

    for key in v_attr_d:
        da.attrs[key] = v_attr_d[key]

    for coord in c_attr_d:
        da.coords[coord].attrs = c_attr_d[coord]

    return da


def create_known_datarray(format_dataarray, values, name):
    # TODO Change so that all are more
    # compliant to CMIP6 protocol etec.

    v_attr_d_d = {
        "SALT": {
            "units": "psu",
            "long_name": "Salinity",
            "other_name": "sea_water_salinity",
            "standard_name": "SALT",
            "comment": "This is practical salinity (see TEOS-10)",
        },
        "THETA": {
            "units": "degC",
            "long_name": "Potential Temperature",
            "standard_name": "THETA",
        },
        "Pressure": {
            "unit": "Pa",
            "long_name": "Pressure at Model Full-Levels [Pa]",
            "standard_name": "pfull",
        },
        "PCA_VALUES": {"long_name": "PCM Values", "units": ""},
        "PCM_RANK": {"long_name": "PCM Rank", "units": ""},
        "Density": {
            "unit": "kg m-3",
            "long_name": "Density",
            "short_name": "rhopoto",
            "standard_name": "sea_water_potential_density",
        },
        "ct": {
            "units": "degC",
            "long_name": "Sea Water Conservative Temperature [degC]",
            "standard_name": "bigthetao",
        },
    }

    assert name in v_attr_d_d

    return create_datarray(format_dataarray, values, name, v_attr_d_d[name])


def test_density_da(time_i=42, max_depth=2000):

    main_dir = "/Users/simon/bsose_monthly/"
    salt = main_dir + "bsose_i106_2008to2012_monthly_Salt.nc"
    theta = main_dir + "bsose_i106_2008to2012_monthly_Theta.nc"

    salt_nc = xr.open_dataset(salt).isel(time=time_i)
    theta_nc = xr.open_dataset(theta).isel(time=time_i)
    big_nc = xr.merge([salt_nc, theta_nc])
    ds = big_nc.where(big_nc.coords["Depth"] > max_depth).drop(
        ["iter", "Depth", "rA", "drF", "hFacC"]
    )

    rho_values, ct_values, pressure_values = return_density(
        ds.where(ds.THETA != 0.0).THETA.values,
        ds.where(ds.SALT != 0.0).SALT.values,
        ds.XC.values,
        ds.YC.values,
        ds.Z.values,
    )

    # for coord in ds.THETA.coords:
    #    print(np.shape(ds.THETA.coords[coord].attrs))

    # print(np.shape(ds.THETA.values))
    # print(np.shape(rho_values))
    # print(np.shape(ct_values))

    density_da = create_known_datarray(ds.THETA, rho_values, "Density")
    ct_da = create_known_datarray(ds.THETA, ct_values, "ct")
    pressure_da = create_known_datarray(ds.THETA, pressure_values, "ct")

    return density_da, ct_da, pressure_da, ds.THETA


def create_whole_density_netcdf():

    main_dir = "/Users/simon/bsose_monthly/"
    salt = main_dir + "bsose_i106_2008to2012_monthly_Salt.nc"
    salt_nc = xr.open_dataset(salt)

    for time_i in range(salt_nc.dims["time"]):

        print(time_i)

        (density_da, ct_da, pressure_da, theta_da) = test_density_da(
            time_i=time_i, max_depth=0
        )

        density_da = density_da.expand_dims(dim="time", axis=None)

        density_da = density_da.assign_coords(
            {"time": ("time", [salt_nc.isel(time=time_i).coords["time"].values])}
        )

        density_da.coords["time"].attrs = salt_nc.coords["time"].attrs

        density_da.to_netcdf("nc/rho/density_" + str(time_i) + ".nc", format="netcdf4")


def merge_whole_density_netcdf():

    rho_da = xr.open_mfdataset(
        "nc/rho/*.nc",
        concat_dim="time",
        combine="by_coords",
        data_vars="minimal",
        coords="minimal",
        compat="override",
    )
    # this is too intense for memory

    return rho_da


def save_density_netcdf(rho_da):

    xr.save_mfdataset([rho_da], ["nc/Density.nc"], format="NETCDF4")


def reload_density_netcdf():

    return xr.open_dataset("nc/density.nc")


def x_grad():
    density_da = xr.open_mfdataset("nc/density.nc", decode_cf=False).astype("float32")
    grad_da = density_da.Density.differentiate("XC").astype("float32")
    density_da["x_grad"] = grad_da
    grad_ds = density_da.drop("Density").astype("float32")
    xr.save_mfdataset([grad_ds], ["nc/density_grad_x.nc"], format="NETCDF4")


def y_grad(set=False):
    density_da = xr.open_mfdataset(
        "nc/density.nc", decode_cf=False, parallel=True
    ).astype("float32")
    grad_da = density_da.Density.astype("float32").differentiate("YC").astype("float32")
    del density_da
    if not set:
        grad_da.to_netcdf("nc/density_grad_y_da.nc", engine="netcdf4")
    else:
        grad_ds = grad_da.to_dataset().astype("float32")
        # density_da['y_grad'] = grad_da
        # grad_ds = density_da.drop('Density')
        xr.save_mfdataset([grad_ds], ["nc/density_grad_y.nc"], format="NETCDF4")


def take_derivative_density(dimension="YC", typ="float32", engine="h5netcdf"):

    chunk_d = {"time": 1, "Z": 52, "YC": 588, "XC": 2160}

    density_ds = xr.open_mfdataset(
        "nc/density.nc",
        # engine=engine,
        # decode_cf=False,
        chunks=chunk_d,
        combine="by_coords",
        data_vars="minimal",
        coords="minimal",
        compat="override",
        parallel=True,
    ).astype(typ)

    grad_da = density_ds.Density.differentiate(dimension)
    # .astype(typ).chunk(chunks=chunk_d)

    name = "Density_Gradient_" + dimension
    grad_ds = grad_da.to_dataset().rename_vars({"Density": name})
    grad_ds[name].attrs["long_name"] = "Density Gradient " + dimension
    grad_ds[name].attrs["units"] = "kg m-3 box-1"

    # .astype(typ).chunk(chunks=chunk_d)
    xr.save_mfdataset(
        [grad_ds], ["nc/density_grad_" + dimension + ".nc"], format="NETCDF4"
    )
