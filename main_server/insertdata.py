import configparser
import psycopg2
from psycopg2 import sql


def insertdata(payload):
    # Load the database information to save the queries in the database
    # Structure of the payload: String:"deviceName,sensor,value,value2*,protocol,status"
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
        # Connect to the database using the configuration for that
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword,host=host, port=port)
        cursor = conn.cursor()

        # Define the query structure to insert the values I will get from the payload variable
        insert_query = """
            INSERT INTO {} (deviceName, sensor, value, protocol, status)
            VALUES (%s, %s, %s, %s, %s)
        """.format(tablename)

        data = payload.split(",") #separate the values from the payload into an array by ,
                                    #-> [deviceName,sensor,value,protocol,status]

        device_name = data[0]
        sensor = data[1]


        #The sensor temperature and humidity has two values, therefore, the string is different
        #"deviceName,sensor,valuet,valueh,protocol,status"
        if sensor == 'tandh_sensor':
            valuet = data[2]
            valueh = data[3]
            protocol = data[4]
            status = data[5]

            # Execute the query with the values, because it is temperature and humidity, I create two queries
            cursor.execute(insert_query, (device_name, sensor, valuet, protocol, status))
            cursor.execute(insert_query, (device_name, sensor, valueh, protocol, status))
            # Commit the transaction
            conn.commit()

        else:
            value = data[2]
            protocol = data[3]
            status = data[4]

            # Execute the query with the values
            cursor.execute(insert_query, (device_name, sensor, value, protocol, status))
            
            # Commit the transaction
            conn.commit()

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()