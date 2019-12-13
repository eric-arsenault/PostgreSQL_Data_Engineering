
# This is a template for uploading large ammounts of new users from a CSV file into the database

import os 
import pandas as pd  
import itertools
import time
import psycopg2

# Create dataframe with CSV file 
os.chdir(r'csv file path')
df = pd.read_csv('csv file')

# Connect to database 
conn = psycopg2.connect(dbname='internal_users', user='admin', password='psw10203040')
cur = conn.cursor()
conn.autocommit = True

# Create batch proccessing function 
def batch_proccess(i, size, seconds):
    it = iter(i)
    while True:
        batch = tuple(itertools.islice(it, size))
        if not batch:
            break
        yield batch
        time.sleep(seconds)

# Function to create new users and store user data
def new_user(username):
    # Create random password
    import random
    elements = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()'
    new_password = str("".join(random.choice(elements) for x in range(10)))

    # Create and permission in SQL
    cur.execute("CREATE USER " + username + " WITH PASSWORD " + "'" + new_password + "'")  
    cur.execute("GRANT SELECT ON user_info TO " + username)

    # Create user ID 
    import pandas as pd
    df = pd.read_sql("SELECT user_id FROM user_info ORDER BY user_id DESC LIMIT 1", conn)
    ID = int(df['user_id'][0]) + 1

    # Store in SQL
    import datetime
    cur.execute("""INSERT INTO user_info(user_id, 
                                        username, 
                                        password, 
                                        permission, 
                                        date_created) 
                                        VALUES """ + str('('+"'"+ID+"'"+", "+"'"+username+"'"+", "+"'"+password+"'"+", "+"'"+"Read"+"'"+", "+str(datetime.datetime.now())+')'))
    return "User Created: " + username 

# Create new users in batches 
for i in batch_proccess(df['New_User_ID'], size=100, seconds = 60):
    for j in i:
        new_user(i)








