# 3: MBTA & Tracts & Population viz
#       - scatterplot of # of stops vs population for each tract
#       - map w stops and population?

# read in packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# read in data
stops_df = gpd.read_file("combined_bus_loc.shp") # ["TRACTCE20", "POP20", "GEOID20", "stop_count", "geometry"]]

