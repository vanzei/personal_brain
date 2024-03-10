# %%
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')

try:
    conn = psycopg2.connect(database = f"{POSTGRES_DBNAME}", 
                            user = f"{POSTGRES_USER}", 
                            host= 'localhost',
                            password = f"{POSTGRES_PASSWORD}",
                            port = 5432)
except:
    print("I am unable to connect to the database") 
cursor = conn.cursor()

# %%

try:
    cursor.execute("CREATE TABLE adm_users (id serial PRIMARY KEY, name varchar, username varchar UNIQUE, password varchar, email varchar UNIQUE, country varchar);")
except:
    print('Table already exists')

try:
    cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, name varchar, username varchar UNIQUE, password varchar, email varchar UNIQUE, user_field varchar, years int, country varchar);")
except:
    print('Table already exists')



# %%
conn.commit() # <--- makes sure the change is shown in the database
conn.close()
cursor.close()
# %%

try:
    conn = psycopg2.connect(database = f"{POSTGRES_DBNAME}", 
                            user = f"{POSTGRES_USER}", 
                            host= 'localhost',
                            password = f"{POSTGRES_PASSWORD}",
                            port = 5432)
except:
    print("I am unable to connect to the database") 
cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO adm_users (name, username, password, email, country) VALUES ('admin', 'admin', 'admin', 'admin', 'admin');")
except:
    print('User already exists')

conn.commit() # <--- makes sure the change is shown in the database
conn.close()
cursor.close()