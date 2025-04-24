# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-23

# Description:
# This module contains the User class and contains methods for setting and getting User data.
# *****************************************************

# Questions:
# Should there be separate class objects for the different roles: subscriber, employee, manager?

class User:
    __user_id = ""
    __f_name = ""
    __l_name = ""
    __email = ""
    __username = ""
    __password_hash = ""
    __role = ""

    def __init__(self, user_id, f_name, l_name, email, username, password_hash, role):
        self.__user_id = user_id
        self.__f_name = f_name
        self.__l_name = l_name
        self.__email = email
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role

    # Read data from the database.
    @staticmethod
    def read_data():
        from data.db_manager import Database
        return Database.read_data()

    # Add data to the database.
    def add_to_database(self):
        from data.db_manager import Database
        Database.add_user(self)
