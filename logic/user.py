"""
Author: R-Nixon
Creation Date: 2025-4-16

Last Modified 06/06/2025 by Sayan

Description:
This module contains the User class and contains methods for setting
and getting User data, and also password hashing.
"""

import bcrypt


class User:
    """
    Class: User
    Author: R-Nixon
    Date Created: 2025-4-16

    Purpose: Defines the User class and contains methods for setting
    and getting User data.
    """

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

    def to_dict(self):
        """
        Function: read_user
        Author: R-Nixon
        Date Created: 2025-5-1

        Purpose: Create a dictionary containing user attributes

        :return: dictionary containing user attributes
        """
        return {
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "email": self.__email,
            "username": self.__username,
            "password_hash": self.__password_hash,
            "role": "Subscriber"
        }

    @classmethod
    def build(cls, dict):
        """
        Function: build
        Author: R-Nixon
        Date Created: 2025-5-1

        Purpose: Build a User class object from a dictionary.

        :param dict: string, user's username
        :return: User object
        """
        return User(dict["first_name"], dict["last_name"], dict["email"], dict["username"], dict["password_hash"],
                    dict["role"])

    # Read data from the database.
    @staticmethod
    def read_user(username, email):
        """
        Function: read_user
        Author: R-Nixon
        Date Created: 2025-5-1
        Date Modified: 2025-5-8

        Purpose: Check the database for a user that matches the username
        or email provided.

        :param username: string, user's username
        :param email: string, user's email
        :return: User object
        """
        from data.db_manager import Database
        users = Database.read_user(username, email)
        # if users is None
        #   return None
        # else:
        result = []
        for user in users or []:
            result.append({
                "first_name": user.get_first_name(),
                "last_name": user.get_last_name(),
                "email": user.get_email(),
                "username": user.get_username(),
                "password_hash": user.get_password_hash(),
                "role": user.get_role()
            })
        return result

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_username(self):
        return self.__username

    def get_password_hash(self):
        return self.__password_hash

    def get_role(self):
        return self.__role

    def verify_password(self, password):
        """
           Function: hash_password
           Author: R-Nixon
           Date Created: 2025-4-16

           Purpose: Check the password entry from the user against the
           stored password_hash.

           :param password: string, user's password
           :return: Boolean, True if password is valid, False otherwise
           """
        return bcrypt.checkpw(password.encode(), self.__password_hash.encode())

    @staticmethod
    def hash_password(password):
        """
          Function: hash_password
          Author: R-Nixon
          Date Created: 2025-4-16

          Purpose: Hashes the plaintext password provided by the user.

          :param password: string, user's password
          :return password_hash: string, hashed value of the password
          """
        salt = bcrypt.gensalt(13)
        password_hash = bcrypt.hashpw(password.encode('utf8'), salt)
        return password_hash.decode('utf8')

    @staticmethod
    # Add data to the database.
    def add_to_database(first_name, last_name, email, username, password_hash, role):
        """
        Function: add_to_database
        Author: R-Nixon
        Date Created: 2025-4-16

        Purpose: Adds a new user to the database.

        :param first_name: string, user first name
        :param last_name: string, user last name
        :param email: string, user email
        :param username: string, user username
        :param password_hash: string, hash value of the user's password
        :param role: string, user's role in the pantry system
        :return: None
        """

        from data.db_manager import Database
        Database.add_user(first_name, last_name, email, username, password_hash, role)
