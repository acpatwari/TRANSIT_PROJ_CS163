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
income_df = pd.read_csv("ACS_Income_Data/ACSST1Y2025.S1901-Data.csv")

# wrangle income data
income_df = income_df.loc[:, ["GEO_ID", "NAME", "S1901_C01_012E"]]
income_df["GEO_ID"] = income_df["GEO_ID"].str.split("US").str[-1]

# combine datasets
joined = stops_df.merge(income_df, left_on="GEOID20", right_on="GEO_ID", how="left")

# scatterplot
sns.relplot(x='stop_count', y='S1901_C01_012E', data=joined)

plt.title('Transit Availability vs Median Income by Census Tract')
plt.xlabel('Number of Bus Stops in Tract')
plt.ylabel('Median Income')


# map
joined.plot(column="S1901_C01_012E", cmap="magma_r", legend=True)



