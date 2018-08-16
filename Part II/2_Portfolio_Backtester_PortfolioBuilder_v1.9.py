"""

v1.9 adds matching of INDEX to PORTFOLIO name.

"""
import pandas as pd
import numpy as np
import glob, os
import datetime
import warnings
import sys

#prevent stackoverflow with number of recursions that the program can do
sys.setrecursionlimit(4000)

#ignores warning that is irrelvant to code
def fxn():
    warnings.warn("deprecated", FutureWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()


#if one index, input = False, if multiple then input = True
multi_index = True

# load df_master created from Part I
df = pd.read_csv(#"E:file_path...\df_master.csv")
##DO NOT CHANGE
df = df.set_index('Date')

#load necessary portfolio folder (change as necessary)
path = #r"E:file_path...\Portfolios"
#set path to where calculated portfolios will end up in
path2 = #r"E:file_path...\Calculated Portfolios"
#set path to where the rebalance dates will be
path3 =  #r"E:file_path...\Rebalance Dates"

#set path to reference

initialPV = 1000000

all_pfiles = glob.glob(path + "/*.csv")
all_rfiles = glob.glob(path2 + "/*.csv" )
list_stocks = list(df)

#loop around all files
for file in all_pfiles:
    #set initial portfolio value. change as needed, no commas etc (if $1,000,000 set as 1000000)
    file_split = file.split("AWAM-")
    condition = file_split[len(file_split) - 1]
    if multi_index == True:
        ref_path = r"E:\AWAM Equity Portfolio Backtester (Edward Lee)\Specs\Ref_Data\INDEX-" + condition
    else:
        ref_path = r"E:\AWAM Equity Portfolio Backtester (Edward Lee)\Specs\Ref_Data\INDEX-10YrVCompQ1_20160325_Q.csv"
    dfPort = pd.read_csv(file)
    list_port_stocks = dfPort['Symbol'].tolist()
    parts = os.path.splitext(os.path.basename(file.replace('\\', os.sep)))[0].split('_')
    portName = parts[0]
    tempDate = datetime.datetime.strptime(parts[1], "%Y%m%d").strftime("%Y-%m-%d")     
    inceptionDate = tempDate
    frequency = parts[2]
    name = "calculated_%s_%s_%s.csv" % (portName, inceptionDate, frequency)
    name2 = "RebalanceDate_%s_%s_%s.csv" % (portName, inceptionDate, frequency)
    name3 = "%s_%s_%s.csv" % (portName, inceptionDate, frequency)
    name4 = "MissingSymbols_%s_%s_%s.csv" % (portName, inceptionDate, frequency)
    
    
    #check to see if stocks in portfolio exist in master dataframe
    missingStocks = np.setdiff1d(list_port_stocks, list_stocks)
    if missingStocks.size == 0:
        print("%s has no missing stocks." % name3)
    else:    
        missingStocks = missingStocks.tolist()
        print("%s Missing from Master DF: %s" % (name3, missingStocks))
        dfMS = pd.DataFrame({'Missing Symbols': missingStocks})
        dfMS = dfMS.set_index('Missing Symbols')
        dfMS.to_csv(os.path.join(path3, name4))

    


    #creates new dataframe that takes only the companies that are inside the portfolio
    dfmain = df.loc[inceptionDate:,dfPort.iloc[:,0]]
    dfmain = dfmain.fillna(0)
    count = len(dfmain.index)
    v = 1 
    q = 0
    
    #holds stock value for early ending stocks until next rebalance date
    def close_gap(q):
        global v
        while v < len(splitArray):
            size = np.size(splitArray[0], 1)
            b = list(range(0, size))
            size2 = (np.size(splitArray[0], 0)) - 1
            for value in b:
               
                a = splitArray[v][0][value]
                b = splitArray[v-1][size2][value]
                if a != 0 and b == 0:
                    splitArray[v-1][size2][value] = a    
            v += 1
            close_gap(q + 1)
   
    
    
    l = 0
    k = 0
    number_list = []
    value_list = []
    #handles problem with stock ending week before rebalance date
    def stock_end(l):
        global k
        while k < len(splitArray) - 1:
            size2 = (np.size(splitArray[0], 0)) - 1
            a = splitArray[l]#[size2]
            b = splitArray[l+1]#[0]
            c = a[:, a[size2] != 0] 
            d = b[:, b[0] != 0]
            before = c[size2] 
            after = d[0]
            if len(before) != len(after):
                before_list = a[size2].tolist()
                after_list = b[0].tolist()
                m = 0
                for value in after_list:
                    if value == 0:
                        before_list[m] = 0
                        m += 1
                    else:
                        m += 1
                o = k + 1
                before_list = list(filter(lambda a: a != 0, before_list))
                before_array = np.asarray(before_list)
                number_list.append(o)
                value_list.append(before_array)
            k += 1
            stock_end(l + 1)
       
    
    #split the array depending on the frequency
    def chunk_arr(arr, ch):
        x = arr.shape[0]
        return np.split(array, np.arange(ch, x, ch))

    #implementation of creating portfolio values
    finishedList = []
    final = []
    numShares = []
    updatedPV = []

    x = 0
    y = 0
    special = 0
    def portfolio_maker(x):
        global y
        global special
        def fill_arr():
            myArray = splitArrayA
            for k, c in enumerate(myArray.T):
                idx = np.flatnonzero(c == 0)
                if idx.size > 0 and idx[0] > 0:
                    myArray[idx, k] = myArray[idx[0] - 1, k]
            return
        while x < count:
            if x == 0:
                change = number_list[special]
                splitArrayA = splitArray[y]
                splitArrayB = np.split(splitArrayA, len(splitArrayA)/1)
                count2 = len(splitArrayB)
                splitArrayC = splitArrayB[0]
                splitArrayD = splitArrayB[0]
                unique, counts = np.unique(splitArrayD, return_counts = True)
                z = dict(zip(unique, counts))
                a = list(z.values())
                b = a[0]
                if 0 in splitArrayC:
                    dividedPV = (initialPV)/((len(dfPort) - b))
                else:
                    dividedPV = (initialPV)/((len(dfPort)))
                d = splitArrayA[:, splitArrayA[count2 -1] != 0]
                e = d[count2 - 1]
                fill_arr()
                if y == change:
                    temp = value_list[special]
                    shareArray = dividedPV/temp
                    numShares.append(shareArray)
                    special += 1
                else:
                    c = splitArrayA[:, splitArrayA[0] != 0]
                    shareArray = dividedPV/c
                    numShares.append(shareArray[0])
                
                for i in splitArrayA:
                    result = numShares[y] * c
                summed = np.sum(result, axis = 1)
                finishedList.append(summed)
                rebalance = len(summed)
                updatedPV.append(summed[rebalance -1])
                l = splitArrayB[rebalance - 1]
                splitArrayC = l[l != 0]
                final.append(e)
                y += 1
                portfolio_maker(x+rebalance)
                return x
            else:
                change = number_list[special]
                splitArrayA = splitArray[y]
                splitArrayB = np.split(splitArrayA, len(splitArrayA)/1)
                count2 = len(splitArrayB)
                splitArrayC = splitArrayB[count2 - 1]
                splitArrayD = splitArrayB[0]
                unique, counts = np.unique(splitArrayD, return_counts = True)
                z = dict(zip(unique, counts))
                a = list(z.values())
                b = a[0]
                if 0 in splitArrayC:
                    dividedPV = (updatedPV[y-1])/((len(dfPort) - b))
                else:
                    dividedPV = (updatedPV[y-1])/((len(dfPort)))
                d = splitArrayA[:, splitArrayA[count2 -1] != 0]
                e = d[count2 - 1]
                if y == change:
                    temp = value_list[special]
                    shareArray = dividedPV/temp
                    numShares.append(shareArray)
                    if (len(number_list) -1) != special:
                        special += 1
                else:
                    shareArray = dividedPV/(final[y-1])
                    numShares.append(shareArray)
                fill_arr()
                c = splitArrayA[:, splitArrayA[0] != 0]
                for i in splitArrayA:
                    result = numShares[y] * c
                    
                    

                summed = np.sum(result, axis = 1)
                finishedList.append(summed)
                rebalance = len(summed)

                updatedPV.append(summed[rebalance - 1])
                for k, c in enumerate(splitArrayA.T):
                    idx = np.flatnonzero(c == 0)
                    if idx.size > 0 and idx[0] > 0:
                        splitArrayA[idx, k] = splitArrayA[idx[0] - 1, k]
                l = splitArrayB[rebalance - 1]
                #splitArrayC = l[l != 0]
    
                final.append(e)
                y += 1

                    
                portfolio_maker(x + rebalance)
                return x    
    #monthly rebalancing
    if frequency == "M": 
        array = dfmain.values
        splitArray = chunk_arr(array, 4)
        size = np.size(splitArray[0],1)
        close_gap(q)
        stock_end(l)
        if len(number_list) == 0:
            number_list = [1000000000000]
        portfolio_maker(x)

        
    #quarterly rebalancing
    elif frequency == "Q":
        array = dfmain.values
        splitArray = chunk_arr(array, 13)
        size = np.size(splitArray[0],1)
        close_gap(q)
        stock_end(l)
        if len(number_list) == 0:
            number_list = [1000000000000]
        portfolio_maker(x)
        

    #no rebalancing
    else:
        #creates an array of the the dfmain
        finishedList = [] #empty list to temporarily store PV of each week
        array = dfmain.values #create numpy array of main dataframe
        splitArray = np.vsplit(array, len(array)/1) #split Array into individual arrays to do calculations
        final = [] #empty list to temporarily store updated PV values
        numShares = [] #empty list to temporarily store numShares (have to use the weeks before) thus needed
        x = 0 #counter variable to loop weekly_update while x < count
        y = 0 #counter variable that updates to iterate over splitArray
        def no_update(x):
            splitArrayB = array[0]
            unique, counts = np.unique(splitArrayB, return_counts = True)
            z = dict(zip(unique, counts))
            a = list(z.values())
            b = a[0]
            if 0 in splitArrayB:
                dividedPV = (initialPV)/((len(dfPort) - b))
            else:
                dividedPV = (initialPV)/((len(dfPort)))
            c = array[:, array[0] != 0]
            shareArray = dividedPV/c
            numShares.append(shareArray[0])
            d = np.vsplit(c, len(c)/1)
            for i in array:
                result = numShares[0] * d
            summed = np.sum(result, axis = 1)
            summed2 = np.sum(summed, axis = 1)
            finishedList.append(summed2)
            return x
        no_update(x)

#    print(number_list)
#    print(value_list)    
    total = np.concatenate(finishedList)
    updatedPVdf = pd.DataFrame(updatedPV, columns = ["Portfolio Value"])
    total.shape = (count, 1)

    #Reference Stock Conversion
    df2 = pd.read_csv(ref_path)
    closeRef = df2[' Close'].values
    closeRef.astype(float)
    g = 0
    lenRef = len(closeRef)
    refList = [0]
    def create_values(g):
        while g < lenRef - 1:
            refReturn = ((closeRef[g + 1]/closeRef[g]) - 1)
            refList.append(refReturn)
            return create_values(g + 1)
    create_values(g)
    df2['Daily Returns'] = refList
    df2['Date'] = pd.to_datetime(df2['Date'])
    temp1 = df2.index[df2['Date'] == inceptionDate].tolist()
    if not temp1:
        print("**Please check to make sure date on Portfolio exists as a date in the Reference Data**")
    value1 = temp1[0]
    value2 = len(df2.index)
    df2 = df2[value1:value2]
    
    dailyRef = df2['Daily Returns'].values
    lenDaily = len(dailyRef)
    compoundedList = [initialPV]
    m = 0
    def compound_values(m):
        while m < lenDaily - 1:
            refCompound = ((compoundedList[m] * (1 + dailyRef[m + 1])))
            compoundedList.append(refCompound)
            return compound_values(m + 1)
    compound_values(m)



    dfTotal = pd.DataFrame(total, index= dfmain.index, columns = ["Portfolio Value"])
    if len(dfTotal) != len(compoundedList):
        print("**Error: length of reference data does not match length of returns**")
        print("Length of Reference Data:", len(compoundedList))
        print("Length of Returns:", len(dfTotal))
    dfRebalanceA = updatedPVdf.merge(dfTotal.reset_index(), on='Portfolio Value').set_index('Date')
    dfRebalanceB = pd.to_datetime(dfRebalanceA.index) + pd.DateOffset(7)
    dfRebalanceC = dfRebalanceB.strftime("%Y-%m-%d").tolist()
    dfRebalanceD = pd.DataFrame(dfRebalanceC)    
    dfTotal['Reference Values'] = compoundedList

    #changes the file name to whatever the variables (portname etc) were given 

    dfTotal.to_csv(os.path.join(path2, name))
    dfRebalanceD.to_csv(os.path.join(path3, name2))