# This is a basic template for a posgreSQL database with a table to store the users.  At the end of the script 
# I created a function that takes in a username as well as the admin users password, and the output is creating 
# a new user in the database as well as storing the user info on a user_info table in the database 

import psycopg2

#Connect
conn = psycopg2.connect(dbname='postgres', user='postgres')
cur = conn.cursor()
conn.autocommit = True

#create internal_user database
cur.execute('CREATE DATABASE internal_users')
cur.execute("CREATE USER admin WITH PASSWORD 'psw10203040'")  

# Reconnect to new database 
conn = psycopg2.connect(dbname='internal_users', user='admin', password='psw10203040')
conn.autocommit = True
cur = conn.cursor()

#create user table
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

#Manage privileges and close connection
cur.execute("GRANT SELECT, INSERT, UPDATE ON user_info TO admin")
conn.close()

#reconnect with admin user 
conn = psycopg2.connect(dbname='internal_users', user='admin', password='psw10203040')
cur = conn.cursor()
conn.autocommit = True

#Function to create new users and store user info
def new_user(username):
    #create random password
    import random
    elements = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()'
    new_password = str("".join(random.choice(elements) for x in range(10)))

    #create and permission in SQL
    cur.execute("CREATE USER " + username + " WITH PASSWORD " + "'" + new_password + "'")  
    cur.execute("GRANT SELECT ON user_info TO " + username)

    #create user ID 
    import pandas as pd
    df = pd.read_sql("SELECT user_id FROM user_info ORDER BY user_id DESC LIMIT 1", conn)
    ID = int(df['user_id'][0]) + 1

    #store in SQL
    import datetime
    cur.execute("""INSERT INTO user_info(user_id, 
                                        username, 
                                        password, 
                                        permission, 
                                        date_created) 
                                        VALUES """ + str('('+"'"+ID+"'"+", "+"'"+username+"'"+", "+"'"+password+"'"+", "+"'"+"Read"+"'"+", "+str(datetime.datetime.now())+')'))
    return "User Created: " + username 

#create new users
new_user('username1')
new_user('username2')
new_user('username3')

#bulk upload function
def bulk_upload(list):
    for i in list:
        new_user(i)

#create users in bulk
list = ['username4', 'username5', 'username6', 'username7', 'username8', 'username9', 'username10']
bulk_upload(list)

