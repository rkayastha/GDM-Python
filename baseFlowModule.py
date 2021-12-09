from math import exp as exp

# Calculate Potential evapotranspiration from thorn waite equations
# Thornwaite equations
# Jan = 0 and dec = 11 in all code


def j_parameter(t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11):
    # TODO: This must be a separate calculation. And we get a constant 'j' valur for our basin?
    #       OR, j parameter is for individual month. Calculate for a particular month
    #       Should be a single value? CROSSCHECK.
    # Jan = 0 and dec = 11 in all calculations
    j = 0
    for temp in [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]:
        j = j + (temp / 5) ** 1.514
    return j


def a_parameter(j):
    a = ((0.0675 * j ** 3) - (7.71 * j ** 2) + (1792 * j) + 49239) * 10 ** (-5)
    return a


def so_parameter():
    # Average sunshine.
    # Below table is icimod values.
    # TODO: find a better way to calculate 'so' based in lat lon.
    # TODO: possible sunshine hours formula in wikipedia., each basin gets new value. This can be automated.
    #       Read lat lon from DEM. Pass it to sunshine formula and get new values.
    so = [6.75, 7.25, 7.25, 7.75, 7.75, 5.5, 3.5, 4, 4, 7.25, 7.25, 7.5]
    return so


def thornwaite(n, so, t, j, a):
    # TODO: if single day time step, does 'n' matter?
    #       Is 'n' single day? Why?
    pet = ((0.533 * n * so) / 12) * ((10 * t) / j) ** a
    return pet

# Classification of landtypes
# Return 'c' values for each land type
# Total land type:


"""
0 = Grass land (0.14 to 0.5)
1 = Agriculture land (0.14 to 0.5)
2 = Shrub Land (0.08 – 0.25)
3 = Forest (0.08 – 0.25)
4 = Barren Land (0.1 – 0.3)
5 = Settlement (0.1 – 0.3)
6 = Water bodies (0.7 - 0.95)
7 = Clean ice/ debris (#TODO:c value?)
"""


def c_value_for_landtype(landtype):
    # default c
    # TODO: Potential pitfall. Default values may cause logical errors.
    c = 0
    if landtype == 0:
        c = 0.2
    elif landtype == 1:
        c = 0.2
    elif landtype == 2:
        c = 0.2
    elif landtype == 3:
        c = 0.2
    elif landtype == 4:
        c = 0.2
    elif landtype == 5:
        c = 0.2
    elif landtype == 6:
        c = 0.2
    elif landtype == 7:
        c = 0.2
    else:
        c = 0
    return c


# Set of functions to calculate base flow for the given DEM.

# i is precipitation in ?? m/h? mm/h? TODO: precipitaiton units. We give daily data so this is in 'mm'
# a is area of pixel. Unit is m2.
# c is runoff coeff
# pet is potential evapotranspiration and is only used to check if precipitation exceeds the evapotranspiration
# if precipitation is more then evapotranspiration has to be subtracted
# if it is not then ?? TODO: when i < pet what to do? 0?
# runoff and total water are returned on m3/s


def total_water_tw(i, a):
    # Pass area of pixel here.
    # TODO: Confirm units of i and a?
    tw = i * a
    return tw/86400


def runoff(landtype, a, c, i, pet):
    # Pass area of pixel here.
    # TODO: Confirm units of i and a?

    # For 'landtype' argument pass pixel data from LULC raster.
    # Check if pixel is barrenland.
    if landtype == 4:
        q = c * i * a

    # TODO: Except barrenland, For everything else formula is same?
    else:
        if i > pet:
            q = c * (i - pet) * a
        else:
            q = c * i * a
    return q/86400


def w_seep(tw, tr):
    # 'tw' is output of 'total_water_tw' function. Pass it here.
    # 'tr' is output of 'runoff' function. Pass it here.
    ws = tw - tr
    return ws

# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
# TODO: Check values returned by individual functions here


def del_gw_sh():
    return 19


def alpha_gw_sh():
    return 0.09


def del_gw_dp():
    return 60


def alpha_gw_dp():
    return 0.5


def beta_dp():
    return 0.6
# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
# SWAT BASE FLOW EQUATIONS
# EACH FUNCTION RETURN VALUE FOR A SINGLE TIME PERIOD AS PER EXCEL FILE. REMEMBER WHILE PASSING VALUES.


def w_rchrg_i(w_rchrg_i_var, del_gw_sh_var, w_seep_var, i):
    # TODO: 'del_gw_sh_var' to be set in calibration.
    # i is time in days. TODO: Verify if i is time in days?
    # w_seep_var is in mm/day
    # del_gw_sh_var is in days. TODO: 30? '30' comes from rakesh dai's excel. Crosscheck.
    # Do not forget to initialie 'w_rchrg_i_var' while calling this function.
    for j in range(0, i):
        w_rchrg_i_var = (1 - exp(-1 / del_gw_sh_var)) * w_seep_var + exp(-1 / del_gw_sh_var) * w_rchrg_i_var
    return w_rchrg_i_var


def w_seep_dp(beta_dp_var, w_rchrg_i_var):
    # Pass values from previous functions.
    w_seep_dp_var = beta_dp_var * w_rchrg_i_var
    return w_seep_dp_var


def w_rchrg_sh(w_rchrg_i_var, w_seep_dp_var):
    w_rchrg_sh_var = w_rchrg_i_var - w_seep_dp_var
    return w_rchrg_sh_var


def w_rchrg_dp(w_rchrg_dp_var, del_gw_dp_var, w_seep_dp_var):
    # TODO: Check units and values?
    # Do not forget to initialize 'w_rchrg_dp_var' while calling this function.
    # Once initialize feed the return value of this function to the same argument.
    w_rchrg_dp_var = w_rchrg_dp_var * exp(-1 / del_gw_dp_var) + w_seep_dp_var * (1 - exp(-1 / del_gw_dp_var))
    return w_rchrg_dp_var


def q_b_sh_i(q_b_sh_i_var, w_rchrg_sh_var, alpha_sh_var, del_t=0.9):
    # TODO: Check units and values?
    # DO not forget to initialize 'q_b_sh_i_var' while calling this function.
    # Once initialize feed the return value of this function to the same argument.
    q_b_sh_i_var = q_b_sh_i_var * exp(- alpha_sh_var * del_t) + w_rchrg_sh_var * (1-exp(-alpha_sh_var * del_t))
    return q_b_sh_i_var


def q_b_dp_i(q_b_dp_i_var, w_rchrg_dp_var, alpha_dp_var, del_t=0.9):
    # TODO: Check units and values?
    # Do not forget to initialize 'q_b_dp_i_var' while calling this function.
    # Once initialize feed the return value of this function to the same argument.
    q_b_dp_i_var = q_b_dp_i_var * exp((-alpha_dp_var * del_t)) + w_rchrg_dp_var * (1 - exp(-alpha_dp_var * del_t))
    return q_b_dp_i_var


def total_base_flow(q_b_sh_i_var, q_b_dp_i_var, a):
    # This is for a single time period. For single and deep aquifer. Loop this to get over a peroid of time.
    # TODO: Check units and values?
    # Pass area of a pixel here in m2
    # returns values in m3/s
    totalbaseflow = (((q_b_sh_i_var + q_b_dp_i_var)/1000)*a)/86400
    return totalbaseflow
# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

