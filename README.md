# Portfolio-Backtester
3-part code created as a Python Developer for hedge fund: Autumn Winds Asset Management during Summer of 2018. 

# Overview

What this program attempts to accomplish in a three step process is to: 

1. Take 1700+ stock data and merge it into a master dataframe given a start date.

2. Determine portfolio growth of certain stocks using position sizing analysis rebalancing at either monthly, quarterly, or annualy.

3. Take the growth of portfolio and calculate performance. 


# Step 1: Portfolio_Backtester_Build_Px_Data.py:

What this program does:
This takes all the stock data from one folder and merges them into a master dataframe for use in the second step of the portfolio performance analysis. 

Important Variables:

path_ref: file path to the reference data that will be the basis of the merge

path: path to the folder with the data files of the individual stocks that will be merged

dateStart: start date of where the master dataframe will start and continue to end of file. Format 
     should be “YYYY-MM-DD” i.e. “2005-01-07”


Errors that can cause the Program to Crash:

path_ref must have its path to a specific csv file with the chosen reference data.

path must lead to a folder not a specific csv file

dateStart must follow the “YYYY-MM-DD” format


Output of Program:

df_master_AWAM_Universe.csv: Master Dataframe for use in part II of the Portfolio Backtester 



# Step 2: Portfolio_Backtester_PortfolioBuilder.py

What this program does:

This takes the master dataframe created from Part I and takes portfolios created in a folder (essentially a symbol list) and does a position sizing analysis to determine portfolio growth from an initial portfolio value.

Important Variables:

multi_index: set to either True or False, True if each portfolio has a custom index and False if the portfolio is set to a single Index. 
df: load the master_dataframe created from Part I into the pd.read_csv

path: file path to where the portfolios are 

path2: file path to where the calculated portfolios will go after the execution of Part II

path3: file path to where the rebalance date into one csv per portfolio will go.

initialPV: integer price of start amount of Portfolio. (i.e. for $1,000,000 it should be formatted as 
     1000000).

Errors that can cause the Program to Crash:

multi_index must have proper Boolean statement for index

if statement : "**Error: length of reference data does not match length of returns**" occurs then 
please check that the reference data ends on the same date as the master dataframe 
and make sure there is no extra commas in either the master dataframe or index. 

If statement:"**Please check to make sure date on Portfolio exists as a date in the Reference 
Data**" then check to make sure the Reference Index starts on the same day as 
the master dataframe. 

Make sure to check that the multi-index has format of file path to this: ..filepath…\INDEX-“ + condition. Example: ref_path = r"E:\AWAM Equity Portfolio Backtester (Edward Lee)\Specs\Ref_Data\INDEX-" + condition

Make sure the else statement of the single index leads to a single reference file. 


Output of Program:

calculated_AWAM..: calculated portfolio for use in Part III to chart Performance
RebalanceDate_AWAM..: csv file for each portfolio where the rebalance date happens to use for 
        regression tests. 



# Step 3: Portfolio_Backtester_PortfolioPerformance.py


What this program does:

Takes the data from Part II, and calculates performance, returning a line-graph with the growth of both the Portfolio and the Index, calculates monthly and annual returns of the portfolio, reference data, and alpha. Lastly, it creates return from inception, which is all in one excel file.


Important Variables:

month_range: the months of data that is being requested to be pulled, if to end of data from Part 
II, comment out month_range as so: #month_range…

path: path to where the calculated returns folder is from the result of Part II.

path_csv: path to where the returns from the monthly data will go in a csv format.


Errors that can cause the Program to Crash: 

path must lead to a folder not a specific crash/



Output of Program:

Performance_AWAM…: the final output of the program, the visible and tangible result of all the data that is calculated.
Returns_AWAM: the output of monthly returns of portfolio, reference data, and alpha that will be used for later needs.


