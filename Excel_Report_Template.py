#%%
#########################################################################################################################################################
#This template:
    -Pulls a user list report from either DB1 or DB2, 
    -Transforms the date values to a form compatible with excel date format (short date and long date)  
    -Writes the data to an excel sheet
    -Uploads it to a file path.  
#########################################################################################################################################################
file_path = r"C:\Users\XXXXX\XXXXXX\XXXXX"
file_name = "Test"
system = 'DB1'  
query = """XXXXXX"""
#########################################################################################################################################################

def pull_fix_save_data(system, query, file_name, file_path):
    import numpy as np 
    import pandas as pd 
    import openpyxl
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl import Workbook
    import os
    import datetime
    import pyodbc
    now = datetime.date.today()

    if system == "DB1":
        sql_conn = pyodbc.connect(driver='XXXXX',
                                server='XXXXX',
                                database='XXXXX',
                                trusted_connection='yes')
        df = pd.read_sql(query, sql_conn)
        df.fillna("", inplace = True)
        
        column_names = [] 
        for i in df.columns:
            column_names.append(i.lower())
        for index, value in enumerate(column_names):
            if 'login' in value:
                x = index
                df2 = df.iloc[:, x].str.split(n = 1, expand = True)
                df3 = df2.iloc[:, 1].str.split(n = 1, expand = True)
                df4 = df3.iloc[:, 1].str.split(n = 1, expand = True)
                
                d = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12' }
                df2[0] = df2[0].map(d)
                df4[2] = df2[0] + "/" + df3[0] + "/" + df4[0] 
                df4[2] = df4[2].astype(str)
                df.drop(df.columns[x],axis=1,inplace=True)

                new_last_login = []
                for i in df4[2]:
                    if str(i) == 'nan':
                        new_last_login.append("")
                    elif str(i) == "":
                        new_last_login.append("")
                    else:new_last_login.append(str(datetime.datetime.strptime(i, '%m/%d/%Y').date()))
                
                df["Last Login"] = new_last_login
        
                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')
            else: 
                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')

        for index, value in enumerate(column_names):
            if 'create' in value:
                y = index
                df.iloc[:, y]  = df.iloc[:, y].astype(str)
                df5 = df.iloc[:, y].str.split("-", expand = True) 
                df6 = df5[2].str.split(" ", expand = True)
                df6[2] = df5[1] + '/' + df6[0] + '/' + df5[0] 
                
                new_create_date = []
                for i in df6[2]:
                    if str(i) == 'nan':
                        new_create_date.append("")
                    elif str(i) == "":
                        new_create_date.append("")
                    else: new_create_date.append(str(datetime.datetime.strptime(i, '%m/%d/%Y').date()))

                df.drop(df.columns[y],axis=1,inplace=True)
                df['Date Created'] = new_create_date

                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')
            else:                   
                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')

    elif system == "DB2":
        sql_conn = pyodbc.connect(driver='XXXXX',
                                    server='XXXXX',
                                    database='XXXXX',
                                    trusted_connection='yes')
        
        df = pd.read_sql(query, sql_conn)
        df.fillna("", inplace = True)
        
        column_names = [] 
        for i in df.columns:
            column_names.append(i.lower())
        for index, value in enumerate(column_names):
            if 'login' in value:
                x = index
                df.iloc[:, x] = df.iloc[:, x].astype(str)
                df2 = df.iloc[:, x].str.split("-", expand = True) 
                df3 = df2[2].str.split(" ", expand = True)
                df2[3] = df2[1] + '/' + df3[0] + '/' + df2[0]

                new_last_login = []
                for i in df2[3]:
                    if str(i) == 'nan':
                        new_last_login.append("")
                    elif str(i) == "":
                        new_last_login.append("")
                    else: new_last_login.append(str(datetime.datetime.strptime(i, '%m/%d/%Y').date()))
                
                df.drop(df.columns[x],axis=1,inplace=True)
                df['Last Login'] = new_last_login

                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')
            else:                   
                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')
       
        for index, value in enumerate(column_names):
            if 'create' in value:
                y = index
                df.iloc[:, y] = df.iloc[:, y].astype(str)
                df2 = df.iloc[:, y].str.split("-", expand = True) 
                df3 = df2[2].str.split(" ", expand = True)
                df2[3] = df2[1] + '/' + df3[0] + '/' + df2[0]
                
                new_create_date = []
                for i in df2[3]:
                    if str(i) == 'nan':
                        new_create_date.append("")
                    elif str(i) == "":
                        new_create_date.append("")
                    else: new_create_date.append(str(datetime.datetime.strptime(i, '%m/%d/%Y').date()))
                                
                df.drop(df.columns[y],axis=1,inplace=True)
                df["Date Created"] = new_create_date 

                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx')
            else:                   
                openpyxl.utils.dataframe.dataframe_to_rows(df, index=False, header=True)
                wb = Workbook()
                ws = wb.active
                for row in dataframe_to_rows(df, index=False, header=True) : ws.append(row)
                os.chdir(file_path)
                wb.save(file_name + "_" + str(now) + '.xlsx') 
    
             
pull_fix_save_data(system, query, file_name, file_path)  

             
