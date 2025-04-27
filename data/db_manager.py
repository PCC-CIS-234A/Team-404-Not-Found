# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-26

# Description:
# This module contains the Database class and connects the logic layer to the SQL database.
# *****************************************************

import pyodbc
from logic.user import User


class Database:
    """
    Author: R-Nixon
    Creation Date: 2025-04-17
    Purpose: This class contains methods to interact with the SQL database.
    """
    __client = None
    __all_users = None

    # Connect to the database.
    @classmethod
    def connect(cls):
        if cls.__client is None:
            cls.__client = pyodbc.connect(
                server="cisdbss.pcc.edu",
                database="CIS234A_404 Team Not Found",
                user="CIS234A_404 Team Not Found",
                password="NoErrors&2",
                trustservercertificate="Yes",
                driver="{ODBC Driver 18 for SQL Server}"
            )

            print("Connected to: ", cls.__client)

    # Read user data from the database.
    @classmethod
    def read_users(cls):
        cursor = cls.__client.cursor()
        sql = """
        SELECT user_id, first_name, last_name, email, password_hash, username, role
        FROM dbo.users2;
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    # Close the database connection.
    @classmethod
    def close_connection(cls):
        cls.__client.close()
        print("Connection closed")

    # Drop data in the database.
    @classmethod
    def drop_data(cls):
        cursor = cls.__client.cursor()
        sql = """
        IF OBJECT_ID('dbo.users2', 'U') IS NOT NULL
            DROP TABLE dbo.users2;
        """
        cursor.execute(sql)
        print("Dropping table")

    # Rebuild data in the database from a known good dataset.
    @classmethod
    def rebuild_data(cls):
        # Parameters from the User class:
        # __first_name = ""
        # __last_name = ""
        # __email = ""
        # __username = ""
        # __password_hash = ""
        # __role = ""
        cursor = cls.__client.cursor()
        sql = """
        CREATE TABLE dbo.users2
            (user_id INT NOT NULL IDENTITY PRIMARY KEY,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            email NVARCHAR(100) NOT NULL UNIQUE,
            username NVARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role='Subscriber' OR role='Staff' OR role='Manager')
            );
            
        INSERT INTO dbo.users2 
            (first_name, last_name, email, username, password_hash, role)
        VALUES
            ('Rebecca', 'Nixon', 'rnixon@pcc.edu', 'rnixon','password_hash', 'Subscriber'),
            ('Chad', 'Summerhays', 'chads@pcc.edu', 'chads', 'password_hash','Subscriber'),
            ('Travis','Corbin','tcorbin@pcc.edu','tcorbin','password_hash','Subscriber'),
            ('Jeff','Popham','jpopham@pcc.edu','jpopham','password_hash','Subscriber'),
            ('Stephanie','Tran', 'stran@pcc.edu','stran','password_hash','Subscriber');
            """
        cursor.execute(sql)

    # Add a user to the database.
    @classmethod
    def add_user(cls):
        cursor = cls.__client.cursor()
        sql = """
        INSERT INTO dbo.users2
         (first_name, last_name, email, password_hash, username, role)
        VALUES 
         ('Test', 'Staff', 'staff@test.com', 'staff_mypcc_2025_C$', 'T Staff', 'Staff')
        """
        cursor.execute(sql)


if __name__ == "__main__":
    Database.connect()
    Database.drop_data()
    Database.rebuild_data()
    Database.read_users()
    Database.add_user()
    Database.read_users()
    Database.close_connection()

