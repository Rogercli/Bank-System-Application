# Bank-System-Application

## Overview

  In this project, I developed a banking application which users can interact with via command-line. Python OOP technqiues are incorporated to define classes and instantiate objects as well as form the logic to perform different operations between objects. For data storage, I chose a MySQL DB and connected it to the UI using a Python MySQL-Connector.


![Screenshot from 2021-09-13 16-33-22](https://user-images.githubusercontent.com/84752424/133170392-b0b8e32a-9b4d-4126-a4aa-ebb71f56fc64.png)

## Requirements

- MySQL DB: https://www.mysql.com/downloads/
- Python MySQL Connector:https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
- Python: https://www.python.org/downloads/

## Setup
**MySQL Configuration and Database Setup**
```
dbconfig={'host':'localhost',
        'user':'root',
        'password':'your_password',
        'auth_plugin':'mysql_native_password'}
```
- Bank_DB_Setup.py 
   - Add your information in the dbconfig and update the configuration in the file Bank_DB_Setup.py
   - Run the file, which creates the MySQL schema for the Bank System application



**MySQL Connector Configuration and Setup**
```
dbconfig={'host':'localhost',
        'user':'root',
        'password':'your_password',
        'database':'Bank_System',
        'auth_plugin':'mysql_native_password'}
```
- MySQL_Connector.py
    - Add your information in the dbconfig and update the configuration in the file MySQL_Connector.py

## Run
**Running the Application**
- Run Application.py file from the CLI with your selected Python interpreter

