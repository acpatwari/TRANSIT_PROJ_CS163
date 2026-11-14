# IMPLEMENTING MODULE 1 HERE
# 1: MBTA & Tract Visualizations
#       - map of # of stops for each tract
#       - bar plot of # of stops for each tract idk sum of stops per tract

# read in packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# read in data
mbta_df = gpd.read_file("mbtabus/MBTABUSSTOPS_PT.shp")
rta_df = gpd.read_file("RTA_Stops/RTA_Stops.shp")
tracts_df = gpd.read_file("CENSUS2020/CENSUS2020TRACTS_POLY.shp")

# select columns
mbta_df = mbta_df.loc[:, ["STOP_NAME", "geometry"]]
rta_df = rta_df.loc[:, ["stop_name", "Agency", "geometry"]]
tracts_df = tracts_df.loc[:, ["TRACTCE20", "POP20", "GEOID20", "geometry"]]

# make rtas the same crs
rta_df = rta_df.to_crs(tracts_df.crs)

# rework and combine bus stop datasets
mbta_df = mbta_df.rename(columns={"STOP_NAME": "stop_name"})
mbta_df = mbta_df.assign(Agency="MBTA")

stops_df = pd.concat([mbta_df, rta_df])

# spatial join with tracts
joined = gpd.sjoin(stops_df, tracts_df, how="inner", predicate="within")

# get stops per tracts
counts = joined.groupby("GEOID20")["stop_name"].count()
counts = counts.reset_index()
counts = counts.rename(columns={"stop_name": "stop_count"})

# merge with tracts and clean up columns
tracts_df = tracts_df.merge(counts, on="GEOID20", how="left")
tracts_df = tracts_df.loc[:, ["TRACTCE20", "POP20", "GEOID20", "stop_count", "geometry"]]

# make map
tracts_df.plot(column="stop_count", cmap="magma_r", legend=True)
plt.title("MA Bus Stops")

# make bar plot
sns.histplot(data=tracts_df, x="stop_count", bins=30)

plt.xlabel("Number of Stops in Tract")
plt.ylabel("Number of Tracts")
plt.title("Massachusetts Distribution of Bus Stops per Tract")
plt.show()

# write up file of combined bus stop locations
tracts_df.to_file("combined_bus_loc.shp")
