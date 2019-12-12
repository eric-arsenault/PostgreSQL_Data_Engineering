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
sql_conn = pyodbc.connect(driver='{PostgreSQL Unicode}',
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

# Create empty dataframe for batches to be added to 
user_list = pd.DataFrame({user_id:[],
                          username:[], 
                          password:[], 
                          permission:[], 
                          date_created:[],
                          user_email:[]})

# Pull data in batches and concat with to a total list
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
    batch = pd.read_sql(query, sql_conn)
    frames = [user_list, batch]
    user_list = pd.concat(frames)
    
#Check Results 
print(user_list.head(10))
print(user_list.tail(10))