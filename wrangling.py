'''
Alina Patwari
18 November 2026

Loading and combining data to prepare for analysis.
'''

# read in packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

def load_data():
    '''
    Reads in all the data needed for this project besides 
    the income dataset, then selects only the relevant columns.
    '''

    # read in data
    mbta_df = gpd.read_file("mbtabus/MBTABUSSTOPS_PT.shp")
    rta_df = gpd.read_file("RTA_Stops/RTA_Stops.shp")
    tracts_df = gpd.read_file("CENSUS2020/CENSUS2020TRACTS_POLY.shp")

    # for each:
    # select variables and explain significance
    mbta_df = mbta_df.loc[:, ["STOP_NAME", "geometry"]]
    rta_df = rta_df.loc[:, ["stop_name", "Agency", "geometry"]]
    tracts_df = tracts_df.loc[:, ["TRACTCE20", "POP20", "GEOID20", "geometry"]]

    return mbta_df, tracts_df, rta_df


def income_wrangle():
    '''
    Reads in and wrangles the median income dataset 
    to prepare in for merging with other datasets
    '''

    income_df = pd.read_csv("ACS_Income_Data/ACSST5Y2024.S1901-Data.csv", 
                            skiprows=[1])
    income_df = income_df.loc[:, ["GEO_ID", "NAME", "S1901_C01_012E"]]

    # fix geo_id and median income columns
    income_df["GEO_ID"] = income_df["GEO_ID"].str.split("US").str[-1]
    income_df["S1901_C01_012E"] = income_df["S1901_C01_012E"].replace({"250,000+": "250000",
                                                                       "2,500-": "2500"})
    income_df["S1901_C01_012E"] = pd.to_numeric(income_df["S1901_C01_012E"],
                                                errors="coerce")

    return income_df


def combine_stops(ran: bool):
    '''
    If ran is True, then returns exisiting combined stops file.
    If ran is false,then it reads in all the data and combines
    mbta and rta data with census tract spatial data to create
    a dataset with the number of bus stops in each census tract.
    '''

    if ran == True:
        return gpd.read_file("combined_bus_loc.shp")

    mbta_df, tracts_df, rta_df = load_data()

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

    # fill tracts that had no bus stops with zero
    tracts_df["stop_count"] = tracts_df["stop_count"].fillna(0)

    # save file
    tracts_df.to_file("combined_bus_loc.shp")

    return tracts_df


def combine_income():
    '''
    Combines median income data with total bus stop data
    by census tracts in Massachussets. Returns the combined
    dataset.
    '''

    # read in data
    stops_df = combine_stops(False)
    income_df = income_wrangle()

    # combine datasets
    joined = stops_df.merge(income_df, left_on="GEOID20", right_on="GEO_ID", how="left")

    return joined


def main():

    mbta_df, tracts_df, rta_df = load_data()
    income_df = income_wrangle()
    stops_df = combine_stops(False)
    income_tracts = combine_income()


if __name__ == '__main__':
    main()
