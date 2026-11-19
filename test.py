'''
Alina Patwari
18 November 2026

Testing my code to ensure validity of results.
'''

# read in packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

from wrangling import combine_stops
from wrangling import combine_income
from wrangling import load_data


def test_stop_count_total(stops_df, rta_df, mbta_df):
    """
    Checks the stop count total = # of rows in rta and mbta df.
    9 stops are in bordering states and don't fall within MA tracts.
    """
    assert stops_df["stop_count"].sum() == (len(rta_df) + len(mbta_df) - 9)


def test_crs_match(mbta_df, tracts_df, rta_df):
    """
    Given two datasets, checks the CRS are the same.
    """
    assert (mbta_df.crs == tracts_df.crs) & (rta_df.crs == tracts_df.crs)


def test_income_range(income_df):
    """
    Check the income data range is reasonable.
    """
    assert (~income_df["S1901_C01_012E"].dropna().between(0, 250000)).sum() == 0


def test_unique_geoids(income_df):
    """
    Checks all GEOIDs are unique.
    """
    ids = income_df["GEOID20"]
    assert ids.is_unique


def main():
    stops_df = combine_stops(False)
    income_df = combine_income()
    mbta_df, tracts_df, rta_df = load_data()

    test_stop_count_total(stops_df, rta_df, mbta_df)
    test_crs_match(mbta_df, tracts_df, rta_df)
    test_income_range(income_df)
    test_unique_geoids(income_df)

    print("All tests passed")


if __name__ == "__main__":
    main()