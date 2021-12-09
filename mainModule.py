# Main module of GDM
# All logics are here
# TODO: CAUTION !!! Lot of the code from this point forward have hardcoded values. CROSSCHECK.

import os
import matplotlib.pyplot as plt
import numpy
from pysheds.grid import Grid
import rasterio
import baseFlowModule

# Define Input and Output Path of the model.

INPUT_PATH = 'D:\\GDM FINAL\\Input\\'
OUTPUT_PATH = 'D:\\GDM FINAL\\Output\\'

DEM_FILE_PATH = 'D:\\GDM FINAL\\Input\\DEM\\dem_trishuli.tif'
LULC_FILE_PATH = 'D:\\GDM FINAL\\Input\\LULC\\lulc_trishuli.tif'
PPT_FILE_PATH = 'D:\\GDM FINAL\\Input\\PPT_TEMP\\ppt.tif'
TEMP_FILE_PATH = 'D:\\GDM FINAL\\Input\\PPT_TEMP\\temp.tif'

if os.path.exists(OUTPUT_PATH):
    pass
else:
    os.mkdir(OUTPUT_PATH)

# Calculate PET for each cell in DEM
# TODO: I dont think PET needs to be calculated at a cell level. This is constant? no?
#       However if sunshine is calculated at cell level then this might be okay? CHECK!!

demfile = rasterio.open(DEM_FILE_PATH)

# Cell size
rasterX = demfile.res[0]
rasterY = demfile.res[1]

# Cell Area
# TODO: CAUTION!!! While preparing DEM dataset in GIS
#  it is very important that the DEM is in proper projected coordinate system
#  If it is NOT this line will give error. This HAS to be in m2.
#  also the Landuse landcover raster must be in the same projected system.
#  There is no crosscheck mechanism in this model to verify if the DEM is in PCS.
cellArea = rasterX * rasterY

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# PET for each individual cell

# Get j values
# TODO: Pass the values for 'j_parameter' function in a separate file. So that all input data that are to be given
#       by the user are at a single place. Refer to the specific function if there are any caveats.
# TODO: CAUTION !!! Hardcoded temperature values for calculating 'j parameter'. CHANGE THIS TO REFLECT ORIGINAL DATA.
# TODO: j parameter is ocnstant for whole basin.
j = baseFlowModule.j_parameter(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

# Calculate 'a' parameter
a = baseFlowModule.a_parameter(j)

# Calculate sunshine hours
# TODO: when the current model runs for multiple months this value changes with the month.
#       Right now this is hardcoded to be a 'January' or any other CERTAIN month.
#       This data is to be coupled with precipitation and temperature data and the month is extracted from there.
#       Refer to the function's original page for further caveats!
so = baseFlowModule.so_parameter()[0]  # <-------- '[0]' indicates January. Chnage this to reflect as required month.

# Calculate PET
# TODO: CAUTION!!! 't' in the following argument is hardcoded this is to be checked accordingly.
#       The temperature values are long term averages for the basin. Change this accordingly.
#       Most probably 'long term average temperature' for the basin needs to be evaluated separately.
#       This then requires a separate function in the 'baseFlow' module
pet = baseFlowModule.thornwaite(n=1, a=a, j=j, so=so, t=1)


# Get a PET raster.
PET_FILE_PATH = os.path.join(OUTPUT_PATH, 'pet.tif')
with rasterio.open(DEM_FILE_PATH) as demfile:
    demfile_data = demfile.read()
    with rasterio.open(
            PET_FILE_PATH,
            'w',
            count=demfile_data.shape[0],
            height=demfile_data.shape[1],
            width=demfile_data.shape[2],
            dtype=demfile_data.dtype,
            crs=demfile.crs,
    ) as petfile:
        # The following line of code replaces all 'elevation' values with the 'pet' values.
        # This results in 'pet' being same for all the basin
        # TODO: discuss with rakesh dai.
        demfile_data[demfile_data > 0] = pet

        # The following code 'petfile.write(demfile_data)' writes all the data in the '1st band'.
        # When viewing in GIS choose accordingly.
        petfile.write(demfile_data)

# For testing purposes
# with rasterio.open(PET_FILE_PATH) as test:
#     petfile_data = test.read(1)
#     plt.imshow(petfile_data)
#     plt.show()

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# Get a 'baseflow' raster.

# 1. get total water 'tw', for each individial cell
with rasterio.open(PPT_FILE_PATH) as pptfile:
    # Read the data
    pptfile_data = pptfile.read()

    # Get number of rows and columns of the dataset
    pptfile_data_rows = pptfile.shape[0]
    pptfile_data_columns = pptfile.shape[1]

    # get other data
    raster_crs = pptfile.crs

    # Now that we have opened the 'ppt' raster file. Lets get all parameters required for calculation of the
    # base flow to each individual elements.
    # The way this is done is to vectorize each functions defined in the 'baseFlowModule' and apply to each elements
    # of the precipitaiaion raster.

    # Get 'tw'
    # But vectorize first.
    tw_vectorised = numpy.vectorize(baseFlowModule.total_water_tw)

    # 'tw' for wach individal cell.
    tw_final = tw_vectorised(pptfile_data, cellArea)

    # Write 'tw' in a raster.
    with rasterio.open(os.path.join(OUTPUT_PATH, 'tw.tif'),
                       'w',
                       count=1,
                       height=pptfile_data_rows,
                       width=pptfile_data_rows,
                       dtype='int16',
                       driver='GTiff',
                       crs=raster_crs) as tw_raster:
        tw_raster.write(tw_final)

with rasterio.open(LULC_FILE_PATH) as lulc_raster:
    lulc_raster_data = lulc_raster.read()

    # Get 'c' values for each pixel
    c_value_vectorized = numpy.vectorize(baseFlowModule.c_value_for_landtype)
    c_values = c_value_vectorized(lulc_raster_data)

    # Print Check
    print(c_values)

    with rasterio.open(PPT_FILE_PATH) as pptfile_data:
        pptfile_data = pptfile_data.read()

        # Get runoff.
        runoff = baseFlowModule.runoff(landtype=4, a=cellArea, c=c_values, i=pptfile_data, pet=1)

        # Print values
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44")
        print(runoff)

        # Get w_seep
        w_seep = baseFlowModule.w_seep(tw_final, runoff)
        print('W SEEP\n\n')
        print(w_seep)

        # Get w_rchrg_i
        # TODO: Pass same variable after initialising. Putting '0' will not work while looping.
        w_rchrg_i = baseFlowModule.w_rchrg_i(10, 30, w_seep, 1)

        print('W rchrg i\n\n')
        print(w_rchrg_i)

        # Get w_seep_dp
        w_seep_dp = baseFlowModule.w_seep_dp(baseFlowModule.beta_dp(), w_rchrg_i)
        print(w_seep_dp)

        # Get w_rchrg_sh_i
        w_rchrg_sh_i = baseFlowModule.w_rchrg_sh(w_rchrg_i, w_seep_dp)
        print(w_rchrg_sh_i)

        # Get q_b_sh_i
        # TODO: Pass same variable after initialising. Putting '0' will not work while looping.
        q_b_sh_i = baseFlowModule.q_b_sh_i(10, w_rchrg_sh_i, baseFlowModule.alpha_gw_sh())
        print(q_b_sh_i)

        # Get w_rchrg_dp_i
        # TODO: Pass same variable after initialising. Putting '0' will not work while looping.
        w_rchrg_dp_i = baseFlowModule.w_rchrg_dp(10, baseFlowModule.del_gw_dp(), w_seep_dp)
        print(w_rchrg_dp_i)

        # Get q_b_dp_i
        # TODO: Pass same variable after initialising. Putting '0' will not work while looping.
        q_b_dp_i = baseFlowModule.q_b_dp_i(10, w_rchrg_dp_i, baseFlowModule.alpha_gw_dp())
        print(q_b_dp_i)

        # Get q_b_i
        q_b_i = q_b_sh_i + q_b_dp_i
        print(q_b_i)

        with rasterio.open(os.path.join(OUTPUT_PATH, 'FINALFINAL.tif'),
                           'w',
                           count=1,
                           height=pptfile_data_rows,
                           width=pptfile_data_rows,
                           dtype='int16',
                           driver='GTiff',
                           crs=raster_crs) as FINAL_RASTER:
            FINAL_RASTER.write(q_b_i)

with rasterio.open('D:\\GDM FINAL\\Output\\FINALFINAL.tif') as test:
    final_data = test.read(1)
    plt.imshow(final_data)
    plt.show()
