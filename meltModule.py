# Set of functions to calculate melt
# TODO: Proper degreeday definitions with their units and values.
# TODO: Check degree day units match with other passed values.
# TODO: From point temperature and precipitation data,
#  Prepare a raster in which each pixel represents temperature and precipitation.
#  This is currently done manually using GIS.
#  Lapse rate to be defined in that part


def degree_day_factors(elevation):
    # Returns a dictionary object. Use it accordingly.
    # TODO: Pass raster elevation data here and change values accordingly.

    # Default values
    # TODO: CAREFUL!!! WITH THESE DEFAULT VALUES. POSSIBLE LOGICAL ERROR SCENARIO.
    ks = 10
    kb = 10
    kd = 10

    if elevation > 5000:
        ks = 10
        kb = 10
        kd = 10
    else:
        ks = 10
        kb = 10
        kd = 10
    return {'ks': ks, 'kb': kb, 'kd': kd}


def melt(degree_day_factors_var, temperature, landusetype):
    # Pass values from the 'degree_day_factors' function here.
    # 'degree_day_factors' function returns a dict. Use it acordingly.
    # TODO: this piece of code maynot run asis. Change the code to reflect the dictionary object.
    # 'landusetype == 7' check for ice / debris.
    # TODO: multiple factors for multiple landuse type.

    melt_var = 0
    if landusetype == 7:
        if temperature > 0:
            melt_var = degree_day_factors_var * temperature
        else:
            melt_var = 0
    elif landusetype != 7:
        if temperature > 0:
            melt_var = degree_day_factors_var * temperature
        else:
            melt_var = 0
    return melt_var

