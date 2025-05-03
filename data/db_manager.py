# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-5-2

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

    # @classmethod
    # def read_user(cls, username):
    #     cls.connect()
    #     user_dict = cls.__users_collection.find_one({'_id': username.lower()})
    #     if user_dict is None:
    #         return None
    #     else:
    #         return User.build(user_dict)

    # Check email/username and password
    @classmethod
    def check_login(cls, login_user, login_password):
        cls.connect()
        sql = """
        SELECT * 
        FROM more_users
        WHERE email = ?
        OR username = ?
        AND password = ?
        """
        params = (login_user, login_user, login_password)
        cursor = cls.__client.cursor()
        cursor.execute(sql, params)

    # Close the database connection.
    @classmethod
    def close_connection(cls):
        cls.__client.close()
        print("Connection closed")

    # Drop data in the sandbox tables.
    # Testing DDL code.
    # Change to real tables for final code.
    @classmethod
    def drop_data(cls):
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
        IF OBJECT_ID('dbo.more_templates', 'U') IS NOT NULL
            DROP TABLE dbo.more_templates;
        IF OBJECT_ID('dbo.more_notifications', 'U') IS NOT NULL
            DROP TABLE dbo.more_notifications;
        IF OBJECT_ID('dbo.more_users', 'U') IS NOT NULL
            DROP TABLE dbo.more_users;
        """
        cursor.execute(sql)
        cls.__client.commit()
        print("Dropping table")

    # Rebuild data in the sandbox tables.
    # Testing DDL code.
    # Change to real tables for final code.
    @classmethod
    def rebuild_data(cls):
        # Attributes of User entity:
        # user_id, first_name, last_name, email, username, password_hash, role

        # Attributes of Notification entity:
        # id, sender_id, subject, message, date_sent, num_subscribers

        # Attributes of Template entity:
        # template_id, creator_id, name, subject, message, (tags??), created_date
        cls.connect()
        cls.drop_data()
        cursor = cls.__client.cursor()
        sql = """
        CREATE TABLE dbo.more_users
            (user_id INTEGER NOT NULL IDENTITY PRIMARY KEY,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            email NVARCHAR(100) NOT NULL UNIQUE,
            username NVARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role='Subscriber' OR role='Staff' OR role='Manager'),
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
        INSERT INTO dbo.more_users 
            (first_name, last_name, email, username, password_hash, role)
        VALUES
            ('Rebecca', 'Nixon', 'rnixon@pcc.edu', 'rnixon','password_hash', 'Subscriber'),
            ('Chad', 'Summerhays', 'chads@pcc.edu', 'chads', 'password_hash','Subscriber'),
            ('Travis','Corbin','tcorbin@pcc.edu','tcorbin','password_hash','Subscriber'),
            ('Jeff','Popham','jpopham@pcc.edu','jpopham','password_hash','Subscriber'),
            ('Stephanie','Tran', 'stran@pcc.edu','stran','password_hash','Subscriber');

        CREATE TABLE dbo.more_notifications
            (id INTEGER NOT NULL IDENTITY PRIMARY KEY,
            sender_id INTEGER NOT NULL REFERENCES users(user_id),
            subject NVARCHAR(255) NOT NULL,
            message NVARCHAR(MAX) NOT NULL,
            date_sent DATETIME DEFAULT CURRENT_TIMESTAMP,
            num_subscribers INTEGER
            );
            
        INSERT INTO dbo.more_notifications 
            (sender_id, subject, message, num_subscribers)
        VALUES 
            (
            1,
            'New Muffins in Stock',
            'Hello students, currently we have new muffins in stock. Please visit your
            nearest location to pick up.',
            3
            ),
            (
            1,
            'Hurry! {{low_stock_item}} Running Low at {{campus_location}}',
            'Dear Students,  Heads up! Our stock of {{low_stock_item}} at the {{campus_location}} pantry is running 
            low.  If you rely on this item, please try to visit the pantry soon to pick some up before it’s gone.  
            Thank you for your continued engagement with our services.  Regards, PCC Pantry Management Team',
            3
            ),
            (
            1,
            'Fresh {{food_item}} Just Arrived at {{campus_location}}!',
            'Dear Students,  Good news! We’ve just received a fresh batch of {{food_item}} at the {{campus_location}} 
            pantry. These items will be available starting from {{availability_start}} through {{availability_end}}, or 
            while supplies last.  Make sure to stop by and pick some up during our open hours. Thank you for being a 
            part of the PCC pantry community!  Regards, PCC Pantry Management Team',
            3
            );

        CREATE TABLE dbo.more_templates
            (template_id INTEGER NOT NULL IDENTITY PRIMARY KEY,
            creator_id INTEGER NOT NULL REFERENCES users(user_id),
            name NVARCHAR(100) NOT NULL UNIQUE,
            subject NVARCHAR(255) NOT NULL,
            message NVARCHAR(MAX) NOT NULL,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );

        INSERT INTO dbo.more_templates
            (creator_id, name, subject, message)
        VALUES
            (
            1,
            'Special Offer',
            'Limited Time Offer on {{item_name}} – Only at {{campus_location}}!',
            'Dear Students,  Exciting news! We’re offering a limited-time discount of {{discount}} on {{item_name}} at
            the {{campus_location}} pantry.  This offer is valid from {{start_date}} to {{end_date}} – so be sure to
            visit before it ends!  Quantities are limited, and items are available on a first-come, first-served basis.
            We hope you take advantage of this special offer to support your needs.
            Regards, PCC Pantry Management Team'
            ),
            (
            1,
            'Pantry Closure',
            'Pantry Closed on {{closure_date}} – Reopening on {{reopening_date}}',
            'Dear Students,  Please be advised that the pantry at {{campus_location}} will be closed on {{closure_date}}
             due to {{reason}}.  We apologize for any inconvenience this may cause. The pantry will reopen on
             {{reopening_date}}.  Thank you for your understanding.    Regards, PCC Pantry Management Team'
            );
        """
        cursor.execute(sql)
        cls.__client.commit()
        print("Database rebuilt")

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
    # Database.read_users()
    # Database.add_test_user()
