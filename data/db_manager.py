# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-23

# Description:
# This module contains the Database class and connects the logic layer to the SQL database.
# *****************************************************

import pymssql
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
            cls.__client = pymssql.connect(
                server='cisdbss.pcc.edu',
                database='CIS234A_404 Team Not Found',
                user='CIS234A_404 Team Not Found',
                password='NoErrors&2'
            )

    # Close the database connection.
    @classmethod
    def close_connection(cls):
        cls.__client.close()

    # Read data from the database.
    @classmethod
    def read_data(cls):
        cls.build_dummy_data()

    # Build dummy data before the database connection is live.
    # Not needed once the database connection code is complete.
    @staticmethod
    def build_dummy_data():
        # Parameters from the User class:
        # __user_id = ""
        # __f_name = ""
        # __l_name = ""
        # __email = ""
        # __username = ""
        # __password_hash = ""
        # __role = ""

        # This format might be better?
        # rn = User("000001", "Rebecca", "Nixon", "rnixon@pcc.edu", "rnixon","password hash", "Subscriber")

        rn = {
            "user_id": "000001",
            "f_name": "Rebecca",
            "l_name": "Nixon",
            "email": "rnixon@pcc.edu",
            "username": "rnixon",
            "password_hash": "password hash",
            "role": "Subscriber"
        }

        cs = {
            "user_id": "000002",
            "f_name": "Chad",
            "l_name": "Summerhays",
            "email": "chads@pcc.edu",
            "username": "chads",
            "password_hash": "password hash",
            "role": "Subscriber"
        }

        tc = {
            "user_id": "000003",
            "f_name": "Travis",
            "l_name": "Corbin",
            "email": "tcorbin@pcc.edu",
            "username": "tcorbin",
            "password_hash": "password hash",
            "role": "Subscriber"
        }

        st = {
            "user_id": "000005",
            "f_name": "Stephanie",
            "l_name": "Tran",
            "email": "stran@pcc.edu",
            "username": "stran",
            "password_hash": "password hash",
            "role": "Subscriber"
        }

        jp = {
            "user_id": "000006",
            "f_name": "Jeff",
            "l_name": "Popham",
            "email": "jpopham@pcc.edu",
            "username": "jpopham",
            "password_hash": "password hash",
            "role": "Subscriber"
        }

        all_users = [rn, cs, tc, st, jp]
        return all_users

    # Rebuild data in the database from a known good dataset.
    @classmethod
    def rebuild_data(cls):
        pass

    # Add a user to the database.
    @classmethod
    def add_user(cls, user):
        pass
