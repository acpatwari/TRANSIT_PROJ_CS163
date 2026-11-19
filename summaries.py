'''
Alina Patwari
18 November 2026

Summarizing combined data for analysis.
'''

# read in packages
import pandas as pd

from wrangling import combine_stops, combine_income


def summarize(df: pd.DataFrame):
    """
    Given a dataframe, prints summaries of all the columns.
    the number of missing values in each column, and the
    shape of the dataframe.
    """
    
    print(df.describe(include='all'))
    print(df.isna().sum())
    print(df.shape)


def main():

    # load data
    stops_df = combine_stops(False)
    income_df = combine_income()

    # summarize
    summarize(stops_df)
    summarize(income_df)
    

if __name__ == '__main__':
    main()
