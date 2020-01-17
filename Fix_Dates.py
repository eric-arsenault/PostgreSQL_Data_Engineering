#%%
###################################################################
###################################################################
# I wrote these functions to fix the way dates came out of a database that I 
# was using for this project.   
###################################################################
###################################################################

def fix_DB1(dataframe):
    #Last Login
    new_last_login = []
    dataframe.fillna("", inplace = True)
    dataframe['date_login_succeeded'] = dataframe['date_login_succeeded'].astype(str)
    dataframe2 = dataframe['date_login_succeeded'].str.split(" ", expand = True )
    dataframe3 = dataframe2[0].str.split("-", expand = True )
    dataframe3[3] = dataframe3[1] + str("/") + dataframe3[2] + str("/") + dataframe3[0]
    dataframe3.fillna("", inplace = True)
    dataframe3[3] = dataframe3[3].astype(str)
    
    for i in dataframe3[3]:
        if i == "":
            new_last_login.append("")
        else: new_last_login.append(datetime.datetime.strptime(i, '%m/%d/%Y').date())
    
    dataframe.drop(columns = ['date_login_succeeded'], inplace = True)
    dataframe["Last Login"] = new_last_login
    
    #Date Created 
    new_date_created = []
    dataframe['date_created'] = dataframe['date_created'].astype(str)
    dataframe4 = dataframe['date_created'].str.split(" ", expand = True )
    dataframe5 = dataframe4[0].str.split("-", expand = True )
        
    dataframe5[3] = dataframe5[1] + str("/") + dataframe5[2] + str("/") + dataframe5[0]
    dataframe3.fillna("", inplace = True)
    dataframe5[3] = dataframe5[3].astype(str)
    
    for i in dataframe5[3]:
        if i == "":
            new_date_created.append("")
        else: new_date_created.append(datetime.datetime.strptime(i, '%m/%d/%Y').date())
    
    dataframe.drop(columns = ['date_created'], inplace = True)
    dataframe["Date Created"] = new_date_created
 
def fix_DB2(dataframe):
    #Last Login
    new_last_login = []
    dataframe.fillna("", inplace = True)
    dataframe['lastlogin'] = dataframe['lastlogin'].astype(str)
    dataframe2 = dataframe['lastlogin'].str.split(n=1, expand = True )
    dataframe3 = dataframe2[1].str.split(" ", expand = True)
    d = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    dataframe2[0] = dataframe2[0].map(d)
    dataframe2[6] = dataframe2[0] + str("/") + dataframe3[0] + str("/") + dataframe3[1]
    dataframe2.fillna("", inplace = True)   
    dataframe2[6] = dataframe2[6].astype(str)
    
    for i in dataframe2[6]:
        if i == "":
            new_last_login.append("")
        else: new_last_login.append(datetime.datetime.strptime(i, '%m/%d/%Y').date())
    
    dataframe.drop(columns = ['lastlogin'], inplace = True)
    dataframe["Last Login"] = new_last_login
    
    #Date Created
    new_date_created = []
    dataframe['Date Created'] = dataframe['Date Created'].astype(str)
    dataframe3 = dataframe['Date Created'].str.split(n = 1, expand = True )
    dataframe4 = dataframe3[0].str.split("-", expand = True ) 
    dataframe4[3] = dataframe4[1] + str("/") + dataframe4[2] + str("/") + dataframe4[0]
    dataframe4.fillna("", inplace = True)
    dataframe4[3] = dataframe4[3].astype(str)
   
    for i in dataframe4[3]:
        if i == "":
            new_date_created.append("")
        else: new_date_created.append(datetime.datetime.strptime(i, '%m/%d/%Y').date())
    
    dataframe.drop(columns = ['Date Created'], inplace = True)
    dataframe["Date Created"] = new_date_created



