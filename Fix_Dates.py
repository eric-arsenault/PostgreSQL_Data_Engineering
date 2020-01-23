#%%
########################################################################################################
########################################################################################################
# I wrote these functions to fix the way dates came out of a databases that I was using for this project.
# The goal of these functions is to write the date in a format that excel will format as a date, 
# so the end user can change date formats and filter by date.
#
# Date format from DB1 is:
#    -2020-01-01 01:01:01.111
#
# Date formats from DB2 are:
#    -Jan 15 2020 11:06AM
#    -2020-01-01 01:01:01.111
########################################################################################################
########################################################################################################

#this function is used when iterating through columns and date format is: 2020-01-01 01:01:01.111
def excel_date(x):
    return datetime.datetime.strptime(x, '%m/%d/%Y').date()

#this function treats an entire column that is in format: 2020-01-01 01:01:01.111
def fix_short_date(df, column):
    df[column] = pd.to_datetime(df[column])
    df[column] = df[column].dt.date
    df[column] = pd.to_datetime(df[column]).dt.strftime('%m-%d-%Y')
    df[column] = df[column].astype(str)
    new_list = []
    for i in df[column]:
        if str(i) == "":
            new_list.append("")  
        elif str(i) == "nan":
            new_list.append("")
        elif str(i) == "NaT":
            new_list.append("")
        else: new_list.append(datetime.datetime.strptime(i, '%m-%d-%Y').date())   
    df.drop(columns = column, inplace = True)
    df[column] = new_list

#this function treats an entire column that is in format: Jan 15 2020 11:06AM
def fix_long_date(df, column):
    df[column] = df[column].astype(str)
    df2 = df[column].str.split(n = 1, expand = True)
    df3 = df2[1].str.split(n = 1, expand = True)
    df4 = df3[1].str.split(n = 1, expand = True)
    d = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12' }
    df2[0] = df2[0].map(d)
    df2[2] = df2[0] + "/" + df3[0] + "/" + df4[0]
    new_list = []
    for i in df2[2]:
        if str(i) == "":
            new_list.append("")  
        elif str(i) == "nan":
            new_list.append("")
        elif str(i) == "NaT":
            new_list.append("")
        else: new_list.append(datetime.datetime.strptime(i, '%m/%d/%Y').date())
    df.drop(columns = column, inplace = True)
    df[column] = new_list
