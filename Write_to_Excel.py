#%%
###################################################################
###################################################################
# I wrote this functions to write data to excel sheets.   
###################################################################
###################################################################

def write_to_excel(dataframe, File_Path, File_Name):
    import os
    import datetime
    import openpyxl
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl import Workbook
    date_object = datetime.date.today()
    
    openpyxl.utils.dataframe.dataframe_to_rows(dataframe, index=False, header=True)
    wb = Workbook()
    ws = wb.active
    for row in dataframe_to_rows(dataframe, index=False, header=True) : ws.append(row)
    
    os.chdir(File_Path)
    wb.save(File_Name + " " + str(date_object) + '.xlsx')
