# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-30

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
                driver="{ODBC Driver 17 for SQL Server}"
            )

            print("Connected to: ", cls.__client)

    # Read user data from the database.
    @classmethod
    def read_users(cls):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        SELECT user_id, first_name, last_name, email, password_hash, username, role
        FROM dbo.users;
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

    # Drop data in the sandbox table "users2"
    # For development purposes only.
    # Remove from final code.
    @classmethod
    def drop_data(cls):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        IF OBJECT_ID('dbo.users2', 'U') IS NOT NULL
            DROP TABLE dbo.users2;
        """
        cursor.execute(sql)
        cls.__client.commit()
        print("Dropping table")

    # Rebuild data in the sandbox table "users2" from a known good dataset.
    # For development purposes only.
    # Remove from final code.
    @classmethod
    def rebuild_data(cls):
        # Parameters from the User class:
        # __first_name = ""
        # __last_name = ""
        # __email = ""
        # __username = ""
        # __password_hash = ""
        # __role = ""
        cls.connect()
        cls.drop_data()
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
        cls.__client.commit()

    # Check to see if the username exists in the database
    @classmethod
    def check_username(cls, username):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        SELECT * from dbo.users
        WHERE username = ?
        """
        param = username
        cursor.execute(sql, param)
        rows = cursor.fetchall()
        if not cursor.rowcount:
            # print("None")
            return None
        else:
            return rows

    # Check to see if email exists in the database
    @classmethod
    def check_email(cls, email):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        SELECT * from dbo.users
        WHERE email = ?
        """
        param = email
        cursor.execute(sql, param)
        rows = cursor.fetchall()
        if not cursor.rowcount:
            # print("None")
            return None
        else:
            return rows

    # Check to see if the combination of login credentials exists in the database
    # This function needs work!
    # The current SQL is invalid.
    @classmethod
    def check_login(cls, login_user, password_hash):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        SELECT * from dbo.users
        WHERE username OR email = ? AND password_hash = ?
        """
        params = (login_user, password_hash)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        if not cursor.rowcount:
            # print("None")
            return None
        else:
            return rows

    # Add a user to the database.
    @classmethod
    def add_user(cls, first_name, last_name, email, username, password_hash, role):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        INSERT INTO dbo.users
         (first_name, last_name, email, username, password_hash, role)
        VALUES
         (?, ?, ?, ?, ?, ?)
        """
        params = (first_name, last_name, email, username, password_hash, role)
        cursor.execute(sql, params)
        cls.__client.commit()

    # Method is for development purposes only.
    # Delete in final code.
    @classmethod
    def add_test_user(cls):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        INSERT INTO dbo.users
         (first_name, last_name, email, username, password_hash, role)
        VALUES
         ('Test','User','email1@email.com','TestUser','pass_hash', 'Subscriber');
        """
        cursor.execute(sql)
        cls.__client.commit()


if __name__ == "__main__":
    Database.rebuild_data()
    Database.read_users()
    # Database.add_test_user()


