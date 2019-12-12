# This script was written to pull user info in batches from a list of email addresses that were provided in a CSV file
# I decided that these should be pulled in batches because I was given about 20,000 email addresses to look up
 
import os 
import pandas as pd  
import pyodbc
import itertools
import time

# Create dataframe with CSV file 
os.chdir(r'csv file path')
df = pd.read_csv('csv file')

# Connect to SQL database 
sql_conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',

                            server='postgres',

                            database='postgres',

                            trusted_connection='yes')

# Create batch proccessing function 
def batch_proccess(i, size, seconds):
    it = iter(i)
    while True:
        batch = tuple(itertools.islice(it, size))
        if not batch:
            break
        yield batch
        time.sleep(seconds)

# Pull data in batches and append to a new list
for i in batch_proccess(df['E-mail'], size=100, seconds = 60):
    query = """SELECT u.user_id
                     ,u.username 
                     ,u.password 
                     ,u.permission 
                     ,u.date_created
                     ,e.user_email 
               FROM user_info u
               LEFT JOIN email_table e on e.id = u.user_id
               WHERE e.user_email in """ + str(i)
    
    
    
    
    q = pd.read_sql(query, sql_conn)
    print(q.head(10))