# This is a template for a posgreSQL database with a table to store the users.  At the end of the script 
# I have created a function that takes in a username and uses it to create a new user and store the user data 
# in the user_info table in the database.   

import psycopg2

# Connect
conn = psycopg2.connect(dbname='postgres', user='postgres')
cur = conn.cursor()
conn.autocommit = True

# Create internal_user database
cur.execute('CREATE DATABASE internal_users')
cur.execute("CREATE USER admin WITH PASSWORD 'psw10203040'")  

# Connect to new database 
conn = psycopg2.connect(dbname='internal_users', user='admin', password='psw10203040')
conn.autocommit = True
cur = conn.cursor()

# Create user table
cur.execute(
    """
    CREATE TABLE user_info (
        user_id INTEGER PRIMARY KEY,
        username VARCHAR(10)
        password VARCHAR(10)
        permission VARCHAR(32)
        date_created TIMESTAMP
        )
    """
)

# Manage privileges and close connection
cur.execute("GRANT SELECT, INSERT, UPDATE ON user_info TO admin")
conn.close()

# Reconnect with admin user 
conn = psycopg2.connect(dbname='internal_users', user='admin', password='psw10203040')
cur = conn.cursor()
conn.autocommit = True

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

# Create new users
new_user('username1')
new_user('username2')
new_user('username3')

# Bulk upload function
def bulk_upload(user_list):
    for i in user_list:
        new_user(i)

# Create users
new_usernames = ['username4', 'username5', 'username6', 'username7', 'username8', 'username9', 'username10']
bulk_upload(new_usernames)

