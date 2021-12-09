# Set of functions for routing the runoff.
# Answers the question, where does the runoff from each pixel go?
# Route the 'total surface runoff'.
# 'total surface runoff' in this module accounts for base flow and surface runoff.

# Add surface only runoff from the 'surfaceRunoffModule' and
# base flow from 'baseFlowModule' to get 'total surface runoff'


from pysheds.grid import Grid
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# TODO: CAUTION!!! THIS IS EXTREMELY UNSATISFACTORY. CHECK ALL OUTPUTS FROM THIS POINT FORWARD.


def total_runoff_single_timeperiod(surface_only_runoff_var, base_flow_only_runoff):
    # Pass values returned from 'surfaceRunoffModule' and 'basFlowModule' here.
    total_surface_runoff_var = surface_only_runoff_var + base_flow_only_runoff
    return total_surface_runoff_var


def total_surface_runoff(time_period, single_day_total_surface_runoff):
    # TODO: check if time period argument is correct. Is timeperiod passed here. CAUTION!! Logical error?
    total_surface_runoff_var = single_day_total_surface_runoff
    for i in range(0, time_period):
        total_surface_runoff_var = total_surface_runoff_var + single_day_total_surface_runoff
    return total_surface_runoff_var


def flow_routing(DEM_FILE_PATH, PRECIPITAITON_RASTER):
    # This function receives 'total runoff' in each pixel. Then routes to another pixel.
    # Intended use: In a single day, where does all the flow go to?
    # TODO:
    #  CHECK_LOGICAL_ERRORS
    #       a. if each pixel contains only rainfall then it is immediately routed to nearest pixel using slope values.
    #       b. if a pixel gets snow then use meltModule to get runoff. Route it immediately?
    #       c. if a pixel still has snow from point number 'b.' then add it to the next day?
    #       d. if a pixel still has snow for a long time (define time period?) convert to ice?
    #       e. if a pixel already has ice then increase ice that was got from point 'd.'
    #       f. if point 'd.' is true and if landtype is not ice or debris then?
    #       g. if point 'd.' is not true what happens to accumulated snow? Does it melt completely in summer where t > 0
    #          based on the 'meltModule'
    #       h. USE GIS ALGORITHM TO GET FLOW PATH? AND ROUTE IT THAT WAY?

    return None
