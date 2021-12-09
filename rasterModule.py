# Set of functions to read and return usable raster data to other modules.
import matplotlib.pyplot as plt
import numpy.random
from osgeo import gdal
import numpy as np
import rasterio
import os
from mainModule import INPUT_PATH, OUTPUT_PATH, DEM_FILE_PATH, LULC_FILE_PATH


def calculate_slope(dem):
    # 'dem' is the file path to the raster file.
    # TODO: CrossCheck.
    gdal.DEMProcessing(os.path.join(OUTPUT_PATH, 'slope.tif'), dem, 'slope')
    with rasterio.open(os.path.join(OUTPUT_PATH, 'slope.tif')) as dataset:
        slope = dataset.read(1)
    return slope


def calculate_aspect(dem):
    # 'dem' is the file path to the raster file.
    # returns numpy array and NOT a raster file
    # TODO: CrossCheck.
    gdal.DEMProcessing(os.path.join(OUTPUT_PATH, 'aspect.tif'), dem, 'aspect')
    with rasterio.open(os.path.join(OUTPUT_PATH, 'aspect.tif')) as dataset:
        aspect = dataset.read(1)
    return aspect


def read_raster(raster_file_path):
    with rasterio.open(raster_file_path) as rasterfile:
        raster_data = rasterfile.read()
    return raster_data


def create_precipitation_raster(DEM_FILE_PATH):
    # This is a dummy precipitation raster
    raster_dem = rasterio.open(DEM_FILE_PATH)
    raster_dem_data = raster_dem.read()
    precipitation_data = numpy.random.rand(raster_dem_data.shape[0], raster_dem_data.shape[1], raster_dem_data.shape[2])
    precipitation_data = precipitation_data*raster_dem_data
    return precipitation_data





