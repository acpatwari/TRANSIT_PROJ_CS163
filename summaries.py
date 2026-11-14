# IMPLEMENT ONE MODULE HERE
# each module:
# 0: summary of all datasets
# 1: MBTA & Population viz
# 2: MBTA & Vehicle & Income viz
# 3: MBTA & Population & Income viz
# 10: testing

# read in packages
import pandas as pd
import geopandas as gpd

# read in data
mbta_df = gpd.read_file("mbtabus/MBTABUSSTOPS_PT.shp")
pop_df = pd.read_csv("ACS_Population_Data/ACSDP5Y2024.DP05-Data.csv")
tracts_df = gpd.read_file("CENSUS2020/CENSUS2020TRACTS_POLY.shp")
income_df = pd.read_csv("ACS_Income_data/ACSST5Y2024.S1902-Data.csv")

# find size of each dataset
print(mbta_df.shape)
print(pop_df.shape)
print(tracts_df.shape)
print(income_df.shape) # want just total med income and tract variable

# for each:
# select variables and explain significance
pop_df = pop_df.loc[:, ["GEO_ID", "NAME", "DP05_0001E"]]
mbta_df = mbta_df.loc[:, ["STOP_NAME", "TOWN", "geometry"]]
tracts_df = tracts_df.loc[:, ["TRACTCE20", "POP20", "GEOID20", "geometry"]]
income_df = income_df.loc[:, ["GEO_ID", "NAME", "S1902_C03_001E"]]

# summary of variables
pop_df.describe(include='all') 
mbta_df.describe(include='all') 
tracts_df.describe(include='all') 
income_df.describe(include='all') 

# check for missing data
pop_df.isna().sum()
mbta_df.isna().sum()
tracts_df.isna().sum()
income_df.isna().sum()