'''
Implmentation of creating master dataframe


*****MUST HAVE VARIABLES THAT NEEDS TO BE CHANGED ON A CASE BY CASE BASIS:******

variable **path** must lead to the data of stocks (file/folder where the all stock data is held)

variable **path_ref** must lead to the reference stock data (currently at SPY)

variable **dateStart* must be the start date of which you want your master dataframe to begin 
        format of dateStart must be "YYYY-MM-DD" ex. "2015-02-04"



'''

import pandas as pd
from pandas import DataFrame, read_csv, Series
import numpy as np
import glob, os

## Path the the reference file to use in joining data on Date.
path_ref = #r"path to reference file goes here" 

## Path to data files.
path = #r"path to stock data goes here" 
    

## Start Date of when datafile should begin, change as needed
## format is "YYYY-MM-DD"
dateStart = "2005-01-07" 

## Create a list of all .csv files in the path
all_files = glob.glob(path + "/*.csv")

## Load reference file into a df. This established the Index for the joined dfs.
df_start = pd.read_csv(path_ref, index_col='Date', parse_dates=['Date'], header=0)
df_master = df_start.loc[dateStart:]

del (df_master['Close'])


## Loop thru each file and concat
for fname in all_files:

    ## Load each file into a df
    dfs = pd.read_csv((fname), index_col = 'Date')

    ## Get symbol name
    symName = dfs['Symbol'][1]
    print("Loading Symbol:  ",symName)

    ## Rename Close col to symName then drop Symbol col
    dfs.rename(columns={'Close': symName}, inplace=True)
    del (dfs['Symbol'])

    ## Join the df with the master (reference) df on Date.
    df_master = pd.merge(df_master, dfs, left_index=True, right_index=True, how='left')
    
    df_master[(df_master.isnull()) & (df_master.shift().isnull())]


## Delete reference symbol from the joined df
del (df_master['Symbol'])


## Handle missing values.  Hold last value for up to 1 period.  Thereafter, the time series is assumed to end.
df_master = df_master.fillna(method='ffill', limit=1)


df_master.to_csv('df_master.csv',encoding='utf-8')