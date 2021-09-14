
import mysql.connector
from loggers import logger

'''Database Configuration Information'''

dbconfig={'host':'localhost',
        'user':'root',
        'password':'your_password',
        'auth_plugin':'mysql_native_password'}



'''Creating Database Query'''

Create_Bank_DB='CREATE DATABASE IF NOT EXISTS Bank_System;'



'''Using Database Query'''

Use_Bank_DB='USE Bank_System;'



'''Creating Customers Table Query'''

Create_Customers_TB='''CREATE TABLE IF NOT EXISTS Customers(
	Cust_ID BIGINT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(64) NOT NULL,
    Password VARCHAR(64) NOT NULL,
    Social_Security CHAR(9) NOT NULL,
    PRIMARY KEY(Cust_ID));'''



'''Creating Accounts Table Query'''

Create_Accounts_TB='''CREATE TABLE IF NOT EXISTS Accounts(
    Acc_ID BIGINT NOT NULL AUTO_INCREMENT,
    Cust_ID BIGINT NOT NULL,
    Account_Type VARCHAR(16),
    Balance FLOAT,
    Approved_Credit FLOAT DEFAULT (0),
    Approved_Loan FLOAT DEFAULT (0),
    CD FLOAT DEFAULT (0),
    Investment FLOAT DEFAULT (0),
    PRIMARY KEY (Acc_ID),
    FOREIGN KEY (Cust_ID) REFERENCES Customers(Cust_ID));'''



'''Connecting to MySQL and Executing Queries'''
try: 
    connection=mysql.connector.connect(
    host=dbconfig['host'],
    user=dbconfig['user'],
    password=dbconfig['password'],
    auth_plugin=dbconfig['auth_plugin'])
    if connection.is_connected():
        cursor=connection.cursor()
        cursor.execute(Create_Bank_DB)
        cursor.execute(Use_Bank_DB)
        cursor.execute(Create_Customers_TB)
        cursor.execute(Create_Accounts_TB)
        connection.commit()
        cursor.close()
except mysql.connector.Error as err:
    logger.error(
            f"'{err}'\nCheck Database Write Query")
