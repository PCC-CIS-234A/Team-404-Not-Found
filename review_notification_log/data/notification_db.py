# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-23
Last Modified: 2025-05-02

Description:
This file defines Notification class and Database class
and contains connection settings to access the Database.
"""
# ***************************************************************
import pyodbc
from datetime import datetime


# Defines Notification (model/entity) class.  Notification table in database.
class Notification:

    def __init__(self, date_sent, subject, message, sender_id, num_subscribers):
        self.date_sent = date_sent
        self.subject = subject
        self.message = message
        self.sender_id = sender_id
        self.num_subscribers = num_subscribers


# Defines Database class
class Database:
    server = ""
    database = ""
    user = ""
    password = ""
    trust_server_certificate = "Yes"
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
            f"DRIVER={cls.driver};"
            f"SERVER={cls.server};"
            f"DATABASE={cls.database};"
            f"UID={cls.user};"
            f"PWD={cls.password};"
            f"TrustServerCertificate={cls.trust_server_certificate};"
        )
        return pyodbc.connect(connection_string)

 # Gets the notification logs from database
    @classmethod
    def get_notification_log(cls, start_date, end_date):
        query = """
            SELECT date_sent, subject, message, sender_id, num_subscribers
            FROM dbo.Notifications
            WHERE date_sent BETWEEN ? AND ?
            ORDER BY date_sent;
        """

       # Holds list objects from Notification table
        notifications = []
        # Opens and closes database connection
        connection = cls.connect()

        try:
            cursor = connection.cursor()
            # Protects against SQL injection keeping query outside of cursor.execute
            cursor.execute(query, (start_date, end_date))

            # Gets column names
            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                notifications.append(Notification(**row_dict))
        finally:
            connection.close()

        return notifications
