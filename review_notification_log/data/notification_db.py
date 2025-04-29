# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-23
Last Modified: 2025-04-28

Description:
This file defines Notification class and Database class
and contains connection settings to access the Database.
"""
# ***************************************************************
import pyodbc
from datetime import datetime

# Defines Notification (model/entity) class.  Notification table in database.
class Notification:

    def __init__(self, notification_id, user_id, subject, message, date_time, num_subscribers):
        self.notification_id = notification_id
        self.user_id = user_id
        self.subject = subject
        self.message = message
        self.date_time = date_time
        self.num_subscribers = num_subscribers


# Defines Database class
class Database:

    server = "",
    database = "",
    user = "",
    password = "",
    trust_server_certificate = "Yes",
    driver = "{ODBC Driver 17 for SQL Server}"

    @classmethod
    def configure(cls, server, database, user, password, trust_server_certificate, driver):
        cls.server = server
        cls.database = database
        cls.user = user
        cls.password = password
        cls.trust_server_certificate = trust_server_certificate
        cls.driver = driver

    # Connects to the database
    @classmethod
    def connect(cls):
        connection_string = (
            "Server={cls.};"
            "Database={cls.};"
            "User={cls.};"
            "Password={cls.};"
            "Trust Server={cls.Yes};"
            "Driver={{{ODBC Driver 17 for SQL Server}}};"
        )
        return pyodbc.connect(connection_string)

 # Gets the notification logs from database
    @classmethod
    def get_notification_log(cls, start_date, end_date):
        query = """
            SELECT notification_id, user_id, subject, message, date_time, num_subscribers
            FROM Notification
            WHERE date_time BETWEEN ? AND ?
            ORDER BY date_time;
        """

       # Holds list objects from Notification table
        notifications = []
        # Opens and closes database connection
        connection = cls.connect()

        try:
            cursor = connection.cursor()
            try:
                cursor.execute(query, (start_date, end_date))
                rows = cursor.fetchall()
                for row in rows:
                    notifications.append(Notification(*row))
            finally:
                cursor.close()
        finally:
                connection.close()

        return notifications
