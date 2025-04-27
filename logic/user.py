# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-26

# Description:
# This module contains the User class and contains methods for setting and getting User data.
# *****************************************************

import bcrypt


class User:
    __user_id = ""
    __f_name = ""
    __l_name = ""
    __email = ""
    __username = ""
    __password_hash = ""
    __role = ""

    def __init__(self, first_name, last_name, email, username, password_hash, role):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role

    @classmethod
    def build(cls, dict):
        return User(dict["first_name"], dict["last_name"], dict["email"], dict["username"],
                    dict["password_hash"], dict["role"])

    # Read data from the database.
    @staticmethod
    def read_users():
        from data.db_manager import Database
        return Database.read_users()

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_username(self):
        return self.__username

    def get_password_hash(self, password):
        # code to hash a password using bcrypt
        return self.__password_hash

    # Check the password entry from the user against the stored password_hash
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.__password_hash())

    def to_dict(self):
        return {
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "email": self.__email,
            "username": self.__username,
            "password_hash": self.__password_hash,
            "role": "Subscriber"
        }

    # Add data to the database.
    def add_to_database(self):
        from data.db_manager import Database
        Database.add_user(self)
