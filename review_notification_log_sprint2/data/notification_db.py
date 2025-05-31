# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-23
Last Modified: 2025-05-31

Description:
This file defines Notification class and Database class
and contains connection settings to access the Database.
"""
# ***************************************************************
import pyodbc

# Defines Notification (model/entity) class.  Notification table in database.
class Notification:

    def __init__(self, date_sent, subject, message, sender_id, num_subscribers, first_name):
        """
        Defines Notification class
        :param date_sent: datetime, date and time of notification sent
        :param subject: string, subject of the notification
        :param message: string, message of the notification
        :param sender_id: int, id of the sender of the notification
        :param num_subscribers: int, number of subscribers notified
        :param first_name: str, name of the person who sent the notification
        """
        self.date_sent = date_sent
        self.subject = subject
        self.message = message
        self.sender_id = sender_id
        self.num_subscribers = num_subscribers
        self.first_name = first_name


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
        """
        Configuration settings to connect to database.
        :param server: server connection string
        :param database: database connection string
        :param user: user connection string
        :param password: password connection string
        :param trust_server_certificate: trust_server_certificate connection string
        :param driver: driver connection string
        :return: None
        """
        cls.server = server
        cls.database = database
        cls.user = user
        cls.password = password
        cls.trust_server_certificate = trust_server_certificate
        cls.driver = driver

    # Connects to the database
    @classmethod
    def connect(cls):
        """
        Connects to database
        :return: connection object
        """
        connection_string = (
            f"DRIVER={cls.driver};"
            f"SERVER={cls.server};"
            f"DATABASE={cls.database};"
            f"UID={cls.user};"
            f"PWD={cls.password};"
            f"TrustServerCertificate={cls.trust_server_certificate};"
        )
        return pyodbc.connect(connection_string)

    # UPDATED Sprint#2 A9 Gets the notification logs from database
    @classmethod
    def get_notification_log(cls, start_date, end_date, sort_by, sort_order):
        """
        Fetches Notification log from database
        :param start_date: datetime, start date and time of notification sent
        :param end_date: datetime, end date and time of notification sent
        :param sort_by: optional column sort by
        :param sort_order: "asc" or "desc"
        :return: list of Notification logs
        """

        # NEW Sprint#2 A9 validate allowed columns for sorting
        valid_sort_columns = {
            "Date & Time": "n.date_sent",
            "Subject": "n.subject",
            "Message": "n.message",
            "Sender": "u.first_name",
            "# of Subscribers": "n.num_subscribers"
        }
        # Default sort
        order_clause = "ORDER BY n.date_sent"
        if sort_by in valid_sort_columns:
            db_column = valid_sort_columns[sort_by]
            order = "ASC" if sort_order.upper() == "ASC" else "DESC"
            order_clause = f"ORDER BY {db_column} {order}"

        query = f"""
            SELECT n.date_sent, n.subject, n.message, n.sender_id, n.num_subscribers, u.first_name
            FROM dbo.Notifications n
            JOIN dbo.Users u ON n.sender_id = u.user_id
            WHERE n.date_sent BETWEEN ? AND ?
            {order_clause};
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
                # Converts tuples into dictionary
                row_dict = dict(zip(columns, row))
                notifications.append(Notification(**row_dict))
        finally:
            connection.close()

        return notifications


    # NEW Sprint#2 A8 Searches logs for keyword
    @classmethod
    def search_logs_keyword(cls, keyword):
        """
        Searches Notification log by keyword
        :param keyword, search text
        :return: List of Notification logs matching keyword
        """
        query = """
               SELECT n.date_sent, n.subject, n.message, n.sender_id, n.num_subscribers, u.first_name
               FROM dbo.Notifications n
               JOIN dbo.Users u ON n.sender_id = u.user_id
               WHERE n.subject LIKE ? OR n.message LIKE ? OR u.first_name LIKE ?
               ORDER BY n.date_sent;
           """

        # % match user input with any sequence of characters
        keyword_pattern = f"%{keyword}%"
        params = (keyword_pattern, keyword_pattern, keyword_pattern)

        # Holds list objects from Notification table
        notifications = []
        # Opens and closes database connection
        connection = cls.connect()

        try:
            cursor = connection.cursor()
            # Protects against SQL injection keeping query outside of cursor.execute
            cursor.execute(query, params)

            # Gets column names
            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                # Converts tuples into dictionary
                row_dict = dict(zip(columns, row))
                notifications.append(Notification(**row_dict))
        finally:
            connection.close()

        return notifications
