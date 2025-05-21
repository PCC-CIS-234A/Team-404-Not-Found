"""
Author: R-Nixon
Creation Date: 2025-4-16
Last Modified: 2025-5-11

Description:
This module contains the Database class and connects the logic layer to the SQL database.

References:
https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary
"""

import pyodbc
import os
from logic.user import User
from logic.notification import Notification


class Database:
    """
    Author: R-Nixon
    Creation Date: 2025-04-16
    Purpose: This class contains methods to interact with the SQL database.
    """
    __client = None

    # Connect to the database.
    @classmethod
    def connect(cls):
        """
        Function: connect
        Author: R-Nixon
        Date Created: 2025-4-16

        Purpose: Connect to the SQL database.

        :param: cls: Database class
        :return: None
        """
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

    @classmethod
    def close_connection(cls):
        """
        Function: close_connection
        Author: R-Nixon
        Date Created: 2025-4-16

        Purpose: Close the database connection.

        :param: cls: Database class
        :return: None
        """
        cls.__client.close()
        print("Connection closed")

    @classmethod
    def drop_data(cls):
        """
        Function: drop_data
        Author: R-Nixon
        Date Created: 2025-5-3

        Purpose: Drop all tables in the SQL database.

        :param: cls: Database class
        :return: None
        """
        cls.connect()
        cursor = cls.__client.cursor()
        # Creates sandbox tables.
        # Change table names for final code.
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

    @classmethod
    def rebuild_data(cls):
        """
        Function: rebuild_data
        Author: R-Nixon
        Date Created: 2025-5-3

        Purpose: Recreate tables in the SQL database and insert known good data.

        :param: cls: Database class
        :return: None
        """
        # Attributes of User entity:
        # user_id, first_name, last_name, email, username, password_hash, role

        # Attributes of Notification entity:
        # id, sender_id, subject, message, date_sent, num_subscribers

        # Attributes of Template entity:
        # template_id, creator_id, name, subject, message, (tags??), created_date
        cls.connect()
        cls.drop_data()
        cursor = cls.__client.cursor()
        # Creates sandbox tables.
        # Change table names for final code.
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
            sender_id INTEGER NOT NULL REFERENCES dbo.more_users(user_id),
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
            creator_id INTEGER NOT NULL REFERENCES dbo.more_users(user_id),
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

    @classmethod
    def read_user(cls, username, email):
        """
        Function: read_user
        Author: R-Nixon
        Date Created: 2025-5-1

        Purpose: Read user data from the database given the username or email.

        :param: cls: Database class
        :param: username: str, user's username
        :param: email: str, user's email
        :return: None, or User object
        """
        # Fails to return a User object.
        # Not able to change the result of the query into a User object.
        cls.connect()
        cursor = cls.__client.cursor()
        sql = """
         SELECT first_name, last_name, email, username, password_hash, role
         FROM dbo.users
         WHERE username = ?
         OR email = ?;
         """
        params = (username, email)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        if not cursor.rowcount:
            print(" read user rows", rows)
            return None
        else:
            print(rows)
            users = []
            columns = [column[0] for column in cursor.description]
            for row in rows:
                user_dict = dict(zip(columns, row))
                users.append(User(**user_dict))
            print("USER:", users)
            return users

    @classmethod
    def check_username(cls, username):
        """
        Function: check_username
        Author: R-Nixon
        Date Created: 2025-4-26

        Purpose: Check to see if the username exists in the database.

        :param: cls: Database class
        :param: username: string, user's username
        :return: None, or Cursor object containing SQL result rows
        """
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
            print("rows", rows)
            return None
        else:
            return rows

    @classmethod
    def check_email(cls, email):
        """
        Function: check_username
        Author: R-Nixon
        Date Created: 2025-4-26

        Purpose: Check to see if the email exists in the database.

        :param: cls: Database class
        :param: email: string, user's email
        :return: None, or Cursor object containing SQL result rows
        """
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
            return None
        else:
            return rows

    @classmethod
    def check_hash(cls, login_user):
        """
        Function: check_hash
        Author: R-Nixon
        Date Created: 2025-4-26

        Purpose: Check for a password hash in the database.

        :param: cls: Database class
        :param: login_user: string, user credential for login, email or username
        :return: None, or Cursor object containing SQL result rows
        """
        cls.connect()
        sql = """
        SELECT password_hash
        FROM dbo.users
        WHERE email = ?
        OR username = ?
        """
        params = (login_user, login_user)
        cursor = cls.__client.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if not cursor.rowcount:
            return None
        else:
            print("row:", row[0])
            pass_hash = row[0]
            return pass_hash

    # Add a user to the database.
    @classmethod
    def add_user(cls, first_name, last_name, email, username, password_hash, role):
        """
        Function: add_user
        Author: R-Nixon
        Date Created: 2025-4-26

        Purpose: Insert values into the database users table to create a new user.

        :param: cls: Database class
        :param: first_name: string, user's first_name
        :param: first_name: string, user's first_name
        :param: email: string, user's email
        :param: username: string, user's username
        :param: password_hash: string, hashed value of the user's password
        :param: role: string, user's role in the pantry system
        :return: None
        """
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

    # Stub function for unit testing
    def insert_notification(subject, message, date_sent, recipient_email):
        print(f"Inserting: {subject}, {message}, {date_sent}, {recipient_email}")
        return True

    @classmethod
    def get_subscribers(cls):
        cls.connect()
        cursor = cls.__client.cursor()
        cursor.execute("SELECT first_name, email FROM dbo.users WHERE role = 'subscriber'")
        result = [{"first_name": row[0], "email": row[1]} for row in cursor.fetchall()]
        cls.close_connection()
        return result

    @classmethod
    def get_sender_id(cls, username):
        cls.connect()
        cursor = cls.__client.cursor()
        cursor.execute("SELECT user_id FROM dbo.users WHERE username = ?", (username,))
        result = cursor.fetchone()
        cls.close_connection()
        return result[0] if result else None

    @classmethod
    def log_notification(cls, subject, message, recipient_count, sender_id, attachments):
        cls.connect()
        cursor = cls.__client.cursor()
        attachment_names = ", ".join([os.path.basename(file) for file in attachments])
        cursor.execute("""
            INSERT INTO dbo.notifications (subject, message, date_sent, num_subscribers, sender_id, attachment_names)
            VALUES (?, ?, GETDATE(), ?, ?, ?)
        """, (subject, message, recipient_count, sender_id, attachment_names))
        cls.__client.commit()
        cls.close_connection()

    @classmethod
    def get_all_tags(cls):
        try:
            cls.connect()
            cursor = cls.__client.cursor()
            cursor.execute("SELECT tag_name FROM dbo.tags")
            tags = [f"{{{row[0]}}}" for row in cursor.fetchall()]  # Wrap each with {}
            cls.close_connection()
            return tags
        except Exception as e:
            print("Error fetching tags from database:", e)
            return []

    @classmethod
    def fetch_template_names(cls):
        try:
            cls.connect()
            cursor = cls.__client.cursor()
            cursor.execute("SELECT name FROM dbo.templates")
            template_names = [row[0] for row in cursor.fetchall()]
            return template_names
        except pyodbc.Error as e:
            print(f"Database Error (fetch_template_names): {e}")
            return []
        finally:
            cls.close_connection()

    # Fetch subject and message by template name
    @classmethod
    def fetch_template_by_name(cls, template_name):
        try:
            cls.connect()
            cursor = cls.__client.cursor()
            cursor.execute("SELECT subject, message FROM dbo.templates WHERE name = ?", (template_name,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
            else:
                print(f"Template '{template_name}' not found.")
                return "", ""
        except pyodbc.Error as e:
            print(f"Database Error (fetch_template_by_name): {e}")
            return "", ""
        finally:
            cls.close_connection()

    # Gets the notification logs from database
    @classmethod
    def get_notification_log(cls, start_date, end_date):
        """
        Fetches Notification log from database
        :param start_date: datetime, start date and time of notification sent
        :param end_date: datetime, end date and time of notification sent
        :return: Notification log
        """
        query = """
            SELECT n.date_sent, n.subject, n.message, n.sender_id, n.num_subscribers, u.first_name
            FROM dbo.Notifications n
            JOIN dbo.Users u ON n.sender_id = u.user_id
            WHERE n.date_sent BETWEEN ? AND ?
            ORDER BY n.date_sent;
        """

        # Holds list objects from Notification table
        notifications = []
        # Opens and closes database connection
        cls.connect()

        try:
            cursor = cls.__client.cursor()
            # Protects against SQL injection keeping query outside of cursor.execute
            cursor.execute(query, (start_date, end_date))

            # Gets column names
            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                # Converts tuples into dictionary
                row_dict = dict(zip(columns, row))
                notifications.append(Notification(**row_dict))
        finally:
            cls.close_connection()

        return notifications


if __name__ == "__main__":
    Database.read_user("tuser", "test@email.com")
    # Database.check_hash("rnixon")
