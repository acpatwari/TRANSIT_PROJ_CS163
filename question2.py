# IMPLEMENT MODULE TWO HERE
# 2: MBTA & Tracts & Income viz
#       - scatterplot of # of stops vs med income for each tract
#       - map w stops and income lol (low income?)

# read in packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# read in data
stops_df = gpd.read_file("combined_bus_loc.shp") # ["TRACTCE20", "POP20", "GEOID20", "stop_count", "geometry"]]
income_df = pd.read_csv("ACS_Income_data/ACSST5Y2024.S1902-Data.csv")
income_df = income_df.loc[:, ["GEO_ID", "NAME", "S1902_C03_001E"]]

# combine datasets
# mbta_veh_df = mbta_df.merge(vehicle_df, left_on="TOWN", 
#                             right_on="MUNICIPALITY", how="outer")
joined = stops_df.merge(income_df, left_on="GEOID20", right_on="GEO_ID", how="left")

# scatterplot
sns.relplot(x='stop_count', y='S1902_C03_001E', data=joined)

plt.title('Transit Availability vs Median Income by Census Tract')
plt.xlabel('Number of Bus Stops in Tract')
plt.ylabel('Median Income')


# map
joined.plot(column="S1902_C03_001E", cmap="magma_r", legend=True)



