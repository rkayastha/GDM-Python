# Set of functions to calculate surface runoff
# Run these set of functions in each raster grid.

# import meltModule
# test_var = meltModule.melt(1, 1, 1)


def runoff_coefficients():
    # returns a dict object. Use it accordingly.
    # TODO: DOES 'rain_coefficient' and 'snow_coefficient' change with elevation. It does no? haina?
    #       If it does then check for elevation values here. ADD IT TO THE CODE.
    #       If it changes with Landuse ADD IT HERE!
    # TODO: Change coefficient values here.
    return {'rain_coefficient': 1, 'snow_coefficient': 1}


def surface_runoff(rain_discharge, rain_coefficient, snow_discharge, snow_coefficient, ice_melt):
    # 'ice_melt' is given by the 'meltModule'. Pass it here
    # TODO: CAUTION!!! DOES NOT INCLUDE BASEFLOW.
    # TODO: maynot run as is. Logical error? Pass function arguments from other modules.
    surface_runoff_var = rain_discharge * rain_coefficient + snow_discharge * snow_coefficient + ice_melt
    return surface_runoff_var


def total_surface_runoff(time_peroid, surface_runoff_var):
    # This function is intented to use for overall time period. This is just the surface runoff.
    # DOES NOT INCLUDE BASEFLOW.
    # Pass surface runoff from 'surface_runoff' function here.
    # TODO: check units and output. Possible logical error.
    total_surface_runoff_var = 0
    for del_t in range(0, time_peroid):
        total_surface_runoff_var = total_surface_runoff_var + surface_runoff_var
    return total_surface_runoff_var

