import mysql.connector
from loggers import logger


dbconfig={'host':'localhost',
        'user':'root',
        'password':'your_password',
        'database':'Bank_System',
        'auth_plugin':'mysql_native_password'}

def create_connection():
    try: 
        connection=mysql.connector.connect(
        host=dbconfig['host'],
        user=dbconfig['user'],
        password=dbconfig['password'],
        database=dbconfig['database'],
        auth_plugin=dbconfig['auth_plugin'])
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        logger.error(
            f"'{err}'\nCheck Database Connection Creation and Configuration")


def write_query(connection,query):
    cursor=connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        logger.error(
            f"'{err}'\nCheck Database Write Query")
    finally:
        cursor.close()

def read_query(connection, query,fetchone=False):
    cursor = connection.cursor()
    try:
        if fetchone==False:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
    except mysql.connector.Error as err:
            logger.error(
                f"'{err}'\nCheck Database Read Query")
            
def close_connection(connection):
    try:
        connection.close()
        print('Connection Closed')
    except mysql.connector.Error as err:
            print(f"Error: '{err}'")
            logger.error(
                f'Check Database Connection Closure\n')
            


