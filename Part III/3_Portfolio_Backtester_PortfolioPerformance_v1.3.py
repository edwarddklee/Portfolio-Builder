"""
Implementation of Analyzing Performance of Portfolios

VARIABLES:
    
**path** is to where the part II calculated data is

**path_csv** is to where the Returns implementation will go to.

**workbook** line 68, place where excel file will go

## = code below is new area of focus

# = subsegement of said focus
"""
import pandas as pd
import numpy as np
import glob, os
import xlsxwriter
from dateutil.relativedelta import *
from datetime import datetime

#month_range of data pulled from date. Please comment out if needed full date range. 
month_range = 48


## File paths

#path is the file to the Part II calculated Returns 
path = #r"file_path\Calculated Portfolios" 

#path_csv is the file where the Returns implemented will go
path_csv = #r"file_path\Returns" 
all_files = glob.glob(path + "/*.csv")



##loop through each file in folder
for file in all_files:
    ##set up basic info needed
    df = pd.read_csv(file)
    df.set_index('Date', inplace = True)
    start_date = df.index[0]
    try:
        datetime_start = datetime.strptime(start_date, "%Y-%m-%d")
        datetime_end = datetime_start + relativedelta(months=+month_range)
        strtime_end = str(datetime_end)
        final = strtime_end[:10]
        df = df.loc[start_date:final]
    except NameError or KeyError:
        df = df
    count = (len(df.index))
    a = str(df.index[1])
    a_four = a[:4]
    b = str(df.index[count - 1])
    b_four = b[:4]    
    
    
    ##set up name for files
    parts = os.path.splitext(os.path.basename(file.replace('\\', os.sep)))[0].split('_')
    portName = parts[1]
    inceptionDate = parts[2]
    frequency = parts[3]
    name = "%s_%s_%s" % (portName, inceptionDate, frequency)
    
    print("Calculating Performance of:", name)

    ##set up excel files
    workbook = xlsxwriter.Workbook(#"E:\file_path\Performance\Performance_"+name+".xlsx")
    worksheet = workbook.add_worksheet("PortfolioPerformance")
    bold = workbook.add_format({'bold' : 1})

    
    
    ##create basic frame of excel files
    worksheet.write('J1', name, bold)
    worksheet.write('I39', 'Portfolio Returns', bold)
    worksheet.write('C40', 'Jan', bold)
    worksheet.write('D40', 'Feb', bold)
    worksheet.write('E40', 'Mar', bold)
    worksheet.write('F40', 'Apr', bold)
    worksheet.write('G40', 'May', bold)
    worksheet.write('H40', 'Jun', bold)
    worksheet.write('I40', 'Jul', bold)
    worksheet.write('J40', 'Aug', bold)
    worksheet.write('K40', 'Sep', bold)
    worksheet.write('L40', 'Oct', bold)
    worksheet.write('M40', 'Nov', bold)
    worksheet.write('N40', 'Dec', bold)
    worksheet.write('O40', 'Year', bold)
    ##structure to create year range in monthly returns
    year_list = range(int(a_four), (int(b_four) + 1))
    printed_list = ["{0}".format(year) for year in year_list]
    count2 = len(printed_list) 
    row = 40
    col = 1
    x = 0
    for year in printed_list:
        worksheet.write(row, col, printed_list[x])
        x += 1
        row += 1
    
    
    
    ##time-series graph    
    chart = workbook.add_chart({'type': 'line'})
    
    data1 = df.index.tolist()
    data2 = df['Portfolio Value'].tolist()
    data3 = df['Reference Values'].tolist()
    
    #create data
    worksheet2 = workbook.add_worksheet("PortfolioData") 
    headings = ['Date', 'Portfolio Value', 'Reference Values']
    worksheet2.write_row('A1', headings, bold)
    worksheet2.write_column('A2', data1)
    worksheet2.write_column('B2', data2)
    worksheet2.write_column('C2', data3)
    max_row = len(df) + 1

    #find min/max of y-axis
    max_PORT= df['Portfolio Value'].max()
    min_PORT = df['Portfolio Value'].min()
    max_Ref = df['Reference Values'].max()
    min_Ref = df['Reference Values'].min()

    
    if max_PORT > max_Ref:
        max_y = max_PORT + 100000
    else:
        max_y = max_Ref + 100000
    if min_PORT < min_Ref:
        min_y = min_PORT - 100000
    else:
        min_y = min_Ref - 100000
    
    #set up chart frame
    chart.set_title ({'name': 'Results of Portfolio'})
    chart.set_x_axis({'name': 'Date', 'date_axis' : True})
    chart.set_y_axis({'name': 'Portfolio Value', 'major_gridlines' : {'visible' : False}})
    chart.set_legend({'position': 'right'})
    chart.set_y_axis({'min': min_y, 'max': max_y})
    chart.set_chartarea({'border': {'none': True}})

    #for loop that adds the data together    
    for i in range(len(['Portfolio Value', 'Reference Values'])):
        col = i + 1
        chart.add_series({
                'name':       ['PortfolioData', 0, col],
                'categories': ['PortfolioData', 2, 0, max_row, 0],
                'values':     ['PortfolioData', 2, col, max_row, col],
                'line':       {'width': 1.00},
        })
    
    #insert chart into excel
    worksheet.insert_chart('B3', chart, {'x_scale': 2.5, 'y_scale': 2.5})
    
    
    ##implementation of monthly returns
    df3 = df.copy()
    df3.reset_index(level=0, inplace=True)
    df3.Date = pd.to_datetime(df3.Date, errors='coerce')
    df4 = df3.set_index('Date')
    monthlist = np.concatenate(pd.Series(df4.index.month).groupby(df4.index.year).unique().values).tolist()
    a = df3.sort_values('Date').groupby([df3.Date.dt.year, df3.Date.dt.month]).last()
    b = a.values



#    if len(b) % 2 != 0:
#        a = a[:-1]
#        b = b[:-1]

    
    count = len(b)
    c = b[:, 1]
    c = c.tolist()
    initialPV = df3['Portfolio Value'].iloc[0]

    
    firstPV = a['Portfolio Value'].iloc[0]
    
    if initialPV != firstPV:    
        c = [initialPV] + c
    x = 0
    y = 0

    #function to calculate monthly returns
    finished_returns = []
    def monthly_returns(x):
        global y
        while x < (count - 1):
            d = (c[y+1]/c[y]) - 1
            finished_returns.append(d)
            y += 1
            monthly_returns(x+1)
            return x
    
    monthly_returns(x)
    len_return = len(finished_returns)
    
    #implementation of reference monthly returns    
    ref_c = b[:, 2]
    ref_c = ref_c.tolist()
    initialPV = df3['Portfolio Value'].iloc[0]
    k = 0
    l = 0
    ref_returns = []
    def reference_returns(k):
        global l
        while k < (count - 1):
            d = (ref_c[l+1]/ref_c[l]) - 1
            ref_returns.append(d)
            l += 1
            reference_returns(k+1)
            return k
    reference_returns(k)
    len_ref = len(ref_returns)
    range_alpha = list(range(0, len_ref))

    #implementation of alpha returns
    alpha_returns = []
    flat_alpha = []
    for value in range_alpha:
        alpha = finished_returns[value] - ref_returns[value]
        flat_alpha.append(alpha)
        percent_alpha = l = "{:.4f}".format(alpha)
        percent_alpha = float(percent_alpha)
        alpha_returns.append(percent_alpha)

    #function to change returns to percentages
    q = 0
    percent_return = []
    def percent_change(x):
        global q
        while x < len_return:
            l = "{:.4f}".format(finished_returns[q])
            l = float(l)
            percent_return.append(l)
            q += 1
            percent_change(x+1)
            return x
    
    percent_change(x)
    #function to change reference data returns to percentages
    q = 0
    r = 0
    percent_ref = []
    def ref_change(r):
        global q
        while r < len_ref:
            l = "{:.4f}".format(ref_returns[q])
            l = float(l)
            percent_ref.append(l)
            q += 1
            ref_change(r+1)
            return r
    ref_change(r)
    
    len_month = len(monthlist)
    len_percent = len(percent_return)

    row = 40
    col = 2
    m = 0
    #add percentage returns to excel file
    for data in finished_returns:
        if m < 2: 
            if monthlist[m] == 1: #jan
                worksheet.write(row, col + 1, percent_return[m])            
            elif monthlist[m] == 2:
                worksheet.write(row, col + 2, percent_return[m])
            elif monthlist[m] == 3:
                worksheet.write(row ,col + 3, percent_return[m])
            elif monthlist[m] == 4:
                worksheet.write(row, col + 4, percent_return[m])
            elif monthlist[m] == 5:
                worksheet.write(row, col + 5, percent_return[m])
            elif monthlist[m] == 6:
                worksheet.write(row, col + 6, percent_return[m])
            elif monthlist[m] == 7:
                worksheet.write(row, col + 7, percent_return[m])
            elif monthlist[m] == 8:
                worksheet.write(row, col + 8, percent_return[m])
            elif monthlist[m] == 9:
                worksheet.write(row, col + 9, percent_return[m])
            elif monthlist[m] == 10:
                worksheet.write(row, col + 10, percent_return[m])
            elif monthlist[m] == 11:
                worksheet.write(row , col + 11, percent_return[m])
            else: 
                worksheet.write(row, col, percent_return[m])
            m+= 1
        else:
            if monthlist[m] == 1: #dec
                worksheet.write(row, col + 1, percent_return[m])            
            elif monthlist[m] == 2:
                worksheet.write(row, col + 2, percent_return[m])
            elif monthlist[m] == 3:
                worksheet.write(row, col + 3, percent_return[m])
            elif monthlist[m] == 4:
                worksheet.write(row, col + 4, percent_return[m])
            elif monthlist[m] == 5:
                worksheet.write(row, col + 5, percent_return[m])
            elif monthlist[m] == 6:
                worksheet.write(row, col + 6, percent_return[m])
            elif monthlist[m] == 7:
                worksheet.write(row, col + 7, percent_return[m])
            elif monthlist[m] == 8:
                worksheet.write(row, col + 8, percent_return[m])
            elif monthlist[m] == 9:
                worksheet.write(row, col + 9, percent_return[m])
            elif monthlist[m] == 10:
                worksheet.write(row, col + 10, percent_return[m])
            elif monthlist[m] == 11:
                worksheet.write(row , col + 11, percent_return[m])
            else:
                row += 1
                worksheet.write(row, col, percent_return[m])
            m += 1    

    
    
    row_title = row + 1
    worksheet.write(row_title, 8, 'Reference Returns', bold)
    m = 0 
    row_index = row_title + 1
    year_ref = row_index
    x = 0
    row_year = row_index
    for year in printed_list:
        worksheet.write(row_year, 1, printed_list[x])
        x += 1
        row_year += 1    
    
    for data in ref_returns:
        if m < 2: 
            if monthlist[m] == 1: #jan
                worksheet.write(row_index, col + 1, percent_ref[m])            
            elif monthlist[m] == 2:
                worksheet.write(row_index, col + 2, percent_ref[m])
            elif monthlist[m] == 3:
                worksheet.write(row_index ,col + 3, percent_ref[m])
            elif monthlist[m] == 4:
                worksheet.write(row_index, col + 4, percent_ref[m])
            elif monthlist[m] == 5:
                worksheet.write(row_index, col + 5, percent_ref[m])
            elif monthlist[m] == 6:
                worksheet.write(row_index, col + 6, percent_ref[m])
            elif monthlist[m] == 7:
                worksheet.write(row_index, col + 7, percent_ref[m])
            elif monthlist[m] == 8:
                worksheet.write(row_index, col + 8, percent_ref[m])
            elif monthlist[m] == 9:
                worksheet.write(row_index, col + 9, percent_ref[m])
            elif monthlist[m] == 10:
                worksheet.write(row_index, col + 10, percent_ref[m])
            elif monthlist[m] == 11:
                worksheet.write(row_index , col + 11, percent_ref[m])
            else: 
                worksheet.write(row_index, col, percent_ref[m])
            m+= 1
        else:
            if monthlist[m] == 1: #dec
                worksheet.write(row_index, col + 1, percent_ref[m])            
            elif monthlist[m] == 2:
                worksheet.write(row_index, col + 2, percent_ref[m])
            elif monthlist[m] == 3:
                worksheet.write(row_index, col + 3, percent_ref[m])
            elif monthlist[m] == 4:
                worksheet.write(row_index, col + 4, percent_ref[m])
            elif monthlist[m] == 5:
                worksheet.write(row_index, col + 5, percent_ref[m])
            elif monthlist[m] == 6:
                worksheet.write(row_index, col + 6, percent_ref[m])
            elif monthlist[m] == 7:
                worksheet.write(row_index, col + 7, percent_ref[m])
            elif monthlist[m] == 8:
                worksheet.write(row_index, col + 8, percent_ref[m])
            elif monthlist[m] == 9:
                worksheet.write(row_index, col + 9, percent_ref[m])
            elif monthlist[m] == 10:
                worksheet.write(row_index, col + 10, percent_ref[m])
            elif monthlist[m] == 11:
                worksheet.write(row_index, col + 11, percent_ref[m])
            else: 
                row_index += 1
                worksheet.write(row_index, col, percent_ref[m])
            m += 1    

    row_title = row_index + 1
    worksheet.write(row_title, 8, 'Alpha Returns', bold)
    m = 0 
    row_alpha = row_title + 1
    year_alpha = row_alpha
    x = 0
    row_year = row_alpha
    for year in printed_list:
        worksheet.write(row_year, 1, printed_list[x])
        x += 1
        row_year += 1
    for data in ref_returns:
        if m < 2: 
            if monthlist[m] == 1: #jan
                worksheet.write(row_alpha, col + 1, alpha_returns[m])            
            elif monthlist[m] == 2:
                worksheet.write(row_alpha, col + 2, alpha_returns[m])
            elif monthlist[m] == 3:
                worksheet.write(row_alpha, col + 3, alpha_returns[m])
            elif monthlist[m] == 4:
                worksheet.write(row_alpha, col + 4, alpha_returns[m])
            elif monthlist[m] == 5:
                worksheet.write(row_alpha, col + 5, alpha_returns[m])
            elif monthlist[m] == 6:
                worksheet.write(row_alpha, col + 6, alpha_returns[m])
            elif monthlist[m] == 7:
                worksheet.write(row_alpha, col + 7, alpha_returns[m])
            elif monthlist[m] == 8:
                worksheet.write(row_alpha, col + 8, alpha_returns[m])
            elif monthlist[m] == 9:
                worksheet.write(row_alpha, col + 9, alpha_returns[m])
            elif monthlist[m] == 10:
                worksheet.write(row_alpha, col + 10, alpha_returns[m])
            elif monthlist[m] == 11:
                worksheet.write(row_alpha, col + 11, alpha_returns[m])
            else: 
                worksheet.write(row_alpha, col,      alpha_returns[m])
            m+= 1
        else:
            if monthlist[m] == 1: #dec
                worksheet.write(row_alpha, col + 1, alpha_returns[m])            
            elif monthlist[m] == 2:
                worksheet.write(row_alpha, col + 2, alpha_returns[m])
            elif monthlist[m] == 3:
                worksheet.write(row_alpha, col + 3, alpha_returns[m])
            elif monthlist[m] == 4:
                worksheet.write(row_alpha, col + 4, alpha_returns[m])
            elif monthlist[m] == 5:
                worksheet.write(row_alpha, col + 5, alpha_returns[m])
            elif monthlist[m] == 6:
                worksheet.write(row_alpha, col + 6, alpha_returns[m])
            elif monthlist[m] == 7:
                worksheet.write(row_alpha, col + 7, alpha_returns[m])
            elif monthlist[m] == 8:
                worksheet.write(row_alpha, col + 8, alpha_returns[m])
            elif monthlist[m] == 9:
                worksheet.write(row_alpha, col + 9, alpha_returns[m])
            elif monthlist[m] == 10:
                worksheet.write(row_alpha, col + 10, alpha_returns[m])
            elif monthlist[m] == 11:
                worksheet.write(row_alpha, col + 11, alpha_returns[m])
            else:
                row_alpha += 1
                worksheet.write(row_alpha, col, alpha_returns[m])
            m += 1        


    ##annual returns
    l = 0
    returnsList = []
    for returns in percent_return:
        if l == 0:
            returnsList.append(returns)
            l += 1
        else:
            if monthlist[l] == 12:
                returnsList.append(0)
                returnsList.append(returns)
            else:
                returnsList.append(returns)
            l += 1
    
    lenList = len(returnsList)
    returnsArray = np.asarray(returnsList)
    returnsArray.shape = (lenList, 1)
    
    returnsArray = np.split(returnsArray, np.where(returnsArray[:, 0]== 0.)[0][0:])
    f = 0
    x = 0
    lenArray = len(returnsArray)
    annualReturns = []
    def yearly_returns(x):
        global f 
        q = 0
        while x < lenArray:
            lensubArray = len(returnsArray[f])
            yearList = []
            while q < lensubArray:
                myArray = returnsArray[f]
                year_return = (1 + myArray[q])
                yearList.append(year_return)
                q += 1
            result = (np.prod(yearList)) - 1
            annualReturns.append(result)
            f += 1
            yearly_returns(x + 1)
            return x
    yearly_returns(x)
    lenAnnual = len(annualReturns)
    percentAnnual = []
    r = 0
    def percent_annual(x):
        global r
        while x < lenAnnual:
            l = "{:.4f}".format(annualReturns[r])
            l = float(l)
            percentAnnual.append(l)
            r += 1
            percent_annual(x+1)
            return x
    
    percent_annual(x)
    row = 40
    col = 14
    for annual in percentAnnual:
        worksheet.write(row, col, percentAnnual[x])
        x += 1
        row += 1
        

    ##annual returns for reference data
    l = 0
    returnsList = []
    for returns in percent_ref:
        if l == 0:
            returnsList.append(returns)
            l += 1
        else:
            if monthlist[l] == 12:
                returnsList.append(0)
                returnsList.append(returns)
            else:
                returnsList.append(returns)
            l += 1
    
    lenList = len(returnsList)
    returnsArray = np.asarray(returnsList)
    returnsArray.shape = (lenList, 1)
    
    returnsArray = np.split(returnsArray, np.where(returnsArray[:, 0]== 0.)[0][0:])
    
    f = 0
    x = 0
    lenArray = len(returnsArray)
    annualReturns = []
    def yearly_returns(x):
        global f 
        q = 0
        while x < lenArray:
            lensubArray = len(returnsArray[f])
            yearList = []
            while q < lensubArray:
                myArray = returnsArray[f]
                year_return = (1 + myArray[q])
                yearList.append(year_return)
                q += 1
            result = (np.prod(yearList)) - 1
            annualReturns.append(result)
            f += 1
            yearly_returns(x + 1)
            return x
    yearly_returns(x)
    
    lenAnnual = len(annualReturns)
    percentAnnual = []
    
    r = 0
    def percent_annual(x):
        global r
        while x < lenAnnual:
            l = "{:.4f}".format(annualReturns[r])
            l = float(l)
            percentAnnual.append(l)
            r += 1
            percent_annual(x+1)
            return x
    
    percent_annual(x)
    col = 14
    for annual in percentAnnual:
        worksheet.write(year_ref, col, percentAnnual[x])
        x += 1
        year_ref += 1
        
    ##annual returns for alpha
    l = 0
    returnsList = []
    for returns in flat_alpha:
        if l == 0:
            returnsList.append(returns)
            l += 1
        else:
            if monthlist[l] == 12:
                returnsList.append(0)
                returnsList.append(returns)
            else:
                returnsList.append(returns)
            l += 1
    
    lenList = len(returnsList)
    returnsArray = np.asarray(returnsList)
    returnsArray.shape = (lenList, 1)
    
    returnsArray = np.split(returnsArray, np.where(returnsArray[:, 0]== 0.)[0][0:])
    
    f = 0
    x = 0
    lenArray = len(returnsArray)
    annualReturns = []
    def yearly_returns(x):
        global f 
        q = 0
        while x < lenArray:
            lensubArray = len(returnsArray[f])
            yearList = []
            while q < lensubArray:
                myArray = returnsArray[f]
                year_return = (1 + myArray[q])
                yearList.append(year_return)
                q += 1
            result = (np.prod(yearList)) - 1
            annualReturns.append(result)
            f += 1
            yearly_returns(x + 1)
            return x
    yearly_returns(x)
    
    lenAnnual = len(annualReturns)
    percentAnnual = []
    
    r = 0
    def percent_annual(x):
        global r
        while x < lenAnnual:
            l = "{:.4f}".format(annualReturns[r])
            l = float(l)
            percentAnnual.append(l)
            r += 1
            percent_annual(x+1)
            return x
    
    percent_annual(x)

    col = 14
    for annual in percentAnnual:
        worksheet.write(year_alpha, col, percentAnnual[x])
        x += 1
        year_alpha += 1

    worksheet.write(year_alpha + 2, 2, 'Cumulative Returns', bold)
    worksheet.write(year_alpha + 3, 1, 'Portfolio', bold)
    worksheet.write(year_alpha + 4, 1, 'Reference Data', bold)
    worksheet.write(year_alpha + 2, 5, 'Standard. Deviation', bold)

    ##implementation of standard deviation
    arrayPort = df['Portfolio Value'].values
    arrayRef  = df['Reference Values'].values
    
    #numpy standard deviation calculation
    stdPort = np.std(arrayPort)
    stdRef  = np.std(arrayRef)
    
    worksheet.write(year_alpha + 3, 5, stdPort)
    worksheet.write(year_alpha + 4, 5, stdRef)
 
    
    ##implementation of return from inception 
    df2 = df.copy()
    df2.reset_index(level=0, inplace=True)
    df2.Date = pd.to_datetime(df2.Date, errors='coerce')

    a = df2.drop('Reference Values', 1)
    s = a.head(n=1)   
    t = s.iloc[0]['Date']
    u = df2.tail(n=1)
    x = u.iloc[0]['Date']
    y = x - t
    y = str(y)
    y = y.split(' ', 1)
    z = y[0]
    z = int(y[0])
    n = z/365

    startPV = s.iloc[0]['Portfolio Value']
    endPV = u.iloc[0]['Portfolio Value']

    return_from_inception = ((endPV/startPV)**(1/n)) - 1
    percent_inception = "{:.2%}".format(return_from_inception)
    worksheet.write(year_alpha + 3, 3,  percent_inception)
    

    ##Reference data return from inception
    df2 = pd.read_csv(file)
    df2.Date = pd.to_datetime(df2.Date, errors='coerce')


    a = df2.drop('Portfolio Value', 1)
    s = a.head(n=1)   
    t = s.iloc[0]['Date']
    u = df2.tail(n=1)
    x = u.iloc[0]['Date']
    y = x - t
    y = str(y)
    y = y.split(' ', 1)
    z = y[0]
    z = int(y[0])
    n = z/365

    startPV = s.iloc[0]['Reference Values']
    endPV = u.iloc[0]['Reference Values']

    return_from_inception2 = ((endPV/startPV)**(1/n)) - 1
    percent_inception2 = "{:.2%}".format(return_from_inception2)
    worksheet.write(year_alpha + 4, 3, percent_inception2)

    workbook.close()
    
    #implementation of csv data file
    len_months = len(monthlist)
    range_month = list(range(0,18))
    q = 0
    r = 0
    index_list = []
    len_print = len(printed_list)
    monthlist = monthlist[:-1]
    for month in monthlist:
        month = str(month)
        if month == "12":
            str_month = "January "
            if q == 0:
                str_year = printed_list[r]
            else:
                r += 1
                str_year = printed_list[r]  
            index_list.append(str_month + str_year)
            q += 1
        elif month == "1":
            str_month = "February "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "2":
            str_month = "March "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "3":
            str_month = "April "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "4":
            str_month = "May "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "5":
            str_month = "June "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "6":
            str_month = "July "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "7":
            str_month = "August "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "8":
            str_month = "September "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "9":
            str_month = "October "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        elif month == "10":
            str_month = "November "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
        else:
            str_month = "December "
            str_year = printed_list[r]
            index_list.append(str_month + str_year)
            q += 1
    
    labels = ['Date', name, 'RefData', 'Alpha']
    df_csv = pd.DataFrame()
    df_csv['Date'] = index_list
    df_csv[name] = percent_return
    name3 = name[4:]

    df_csv['RefData'+name3] = percent_ref
    df_csv['Alpha'+name3] = alpha_returns
    df_csv = df_csv.set_index('Date')
    name2 = "Returns_"+name+".csv"

    df_csv.to_csv(os.path.join(path_csv, name2))           
 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    