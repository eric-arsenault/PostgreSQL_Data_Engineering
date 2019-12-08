# This is a basic template for a posgreSQL database with a table to store the users.  At the end of the script 
# I created a function that takes in a username as well as the admin users password, and the output is creating 
# a new user in the database as well as storeing the users information on a user table in the database 

from datetime import datetime
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

#Function to create and store new users 
def new_user(username, adminpassword):
    #create random password
    elements = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()'
    new_password = str("".join(random.choice(elements) for x in range(10)))

    #create in SQL
    conn = psycopg2.connect(dbname='internal_users', user='admin', password=adminpassword)
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("CREATE USER " + username + " WITH PASSWORD " + "'" + new_password + "'")  
    cur.execute("GRANT SELECT ON user_info TO " + username + '"')

    #create user ID 
    df = pd.read_sql_query("SELECT user_id FROM user_info LIMIT 1 DESC",conn)
    ID = int(df['user_id'][0]) + 1

    #store in SQL
    cur.execute("INSERT INTO user_info(user_id, username, password, permission, date_created) VALUES " + ID + " ," + username + " ," + password + " ," + "Read" + " ," + datetime.now())
    conn.close()
    

#create new users
new_user('fakeemail1@gmail.com')
new_user('fakeemail2@gmail.com')
new_user('fakeemail3@gmail.com')


