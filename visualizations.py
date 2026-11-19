'''
Alina Patwari
18 November 2026

Creating visualizations to understand my datasets.
'''

# read in packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

from wrangling import combine_stops, combine_income

sns.set_theme()

def question1():
    '''
    Creates a map and a histogram intending to answer
    my first research question: What neighborhoods have 
    the most transit stops/frequency? 
    '''
    
    tracts_df = combine_stops(False)

    # make map
    tracts_df.plot(column="stop_count", cmap="magma_r", legend=True)
    plt.title("MA Bus Stops")

    # make bar plot
    sns.histplot(data=tracts_df, x="stop_count", bins=60)

    plt.xlabel("Number of Stops in Tract")
    plt.ylabel("Number of Tracts")
    plt.title("Massachusetts Distribution of Bus Stops per Tract")
    plt.show()


def question2():
    '''
    Creates a scatterplot and a map intending to answer
    my second research question: Is transit correlated 
    with median income?
    '''
    
    # read in data
    stops_df = combine_stops(False)
    income_df = combine_income()

    # combine datasets
    joined = stops_df.merge(income_df, left_on="GEOID20", right_on="GEO_ID", how="left")

    # scatterplot
    sns.relplot(x='stop_count', y='S1901_C01_012E', data=joined)

    plt.title('Transit Availability vs Median Income by Census Tract')
    plt.xlabel('Number of Bus Stops in Tract')
    plt.ylabel('Median Income')


    # map
    joined.plot(column="S1901_C01_012E", cmap="magma_r", legend=True)
    plt.title('Massachusetts Median Income by Census Tract')


def question3():
    '''
    Creates a scatterplot and a map intending to answer
    my third research question: How many people live within 
    tracts that have a high volume of bus stops?
    '''

    # read in data
    stops_df = combine_stops()

    # scatterplot
    sns.relplot(x='stop_count', y='POP20', data=stops_df)

    plt.title('Transit Availability vs Population of Census Tract')
    plt.xlabel('Number of Bus Stops in Tract')
    plt.ylabel('Population')

    # map
    stops_df.plot(column="POP20", cmap="magma_r", legend=True)


def main():
    
    question1()
    question2()
    question3()


if __name__ == '__main__':
    main()
