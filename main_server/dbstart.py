import configparser
import psycopg2
from psycopg2 import sql, extensions

# Read connection details from database.ini
config = configparser.ConfigParser()
config.read('database.ini')
#print(config.sections())
#print(config.options('database'))

dbname = config['database']['dbname']
dbuser = config['database']['dbuser']
dbpassword = config['database']['dbpassword']
host = config['database']['host']
port = config['database']['port']
tablename = config['database']['tablename']

try:
    # Check if the database 
    conn = psycopg2.connect(dbname='postgres', user=dbuser, password=dbpassword,host=host, port=port)
    conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT) #Let me create tables and I don't have to use excecute.commit.
    cursor = conn.cursor()
    cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = %s", (dbname,))
    exists = cursor.fetchone() #stores the result from the previous query if the database doesn't exist it will be null

    # If the database does not exist, create it
    if not exists:
        cursor.execute(sql.SQL(f"CREATE DATABASE {dbname}"))
        #conn.commit()  # Commit the transaction

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close the cursor and the connection
    cursor.close()
    conn.close()

#After closing the connection, Now I create the table I will use for the project
try:
    #connect to the new database created
    conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword,host=host, port=port)
    cursor = conn.cursor()
    # Check if the table already exists
    cursor.execute(sql.SQL(
    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)"
    ), (tablename,))
    table_exists = cursor.fetchone()[0]

    # If the table doesn't exist, create it
    if not table_exists:
    # Define the SQL query to create the table SERIAL is like INT auto-incrementing
        query = sql.SQL("""
            CREATE TABLE {} (
                id SERIAL PRIMARY KEY,
                deviceName VARCHAR(50),
                sensor VARCHAR(20),
                reading VARCHAR(20),
                protocol VARCHAR(20),
                status VARCHAR(20)
            )
        """).format(sql.Identifier(tablename))
        # Execute the query
        cursor.execute(query)
        # Commit the transaction
        conn.commit()

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close the cursor and the connection
    cursor.close()
    conn.close()