"""
Author: R-Nixon
Creation Date: 2025-5-20
Last Modified: 2025-5-21

Description:
This module contains the User class and contains methods for setting
and getting User data, and also password hashing.
"""
# Two tests fail, as expected.
# These were User functions I could not get to work properly in Sprint 1.

import unittest
from logic.user import User


class TestUser(unittest.TestCase):
    def test_constructor(self):
        test_user = User("Test", "User", "test@email.com", "tuser", "pass_hash", "Subscriber")

        self.assertEqual("Test", test_user.get_first_name())
        self.assertEqual("User", test_user.get_last_name())
        self.assertEqual("test@email.com", test_user.get_email())
        self.assertEqual("tuser", test_user.get_username())
        self.assertEqual("pass_hash", test_user.get_password_hash())
        self.assertEqual("Subscriber", test_user.get_role())

    def test_to_dict(self):
        test_user = User("Test", "User", "test@email.com", "tuser",
                         "$2b$13$IAJ2qLxIz6PVXqv1PAEDlewLjyTJWpuAfA/2UlIUPVfpq/4UQxenS", "Subscriber")

        self.assertEqual({
            "first_name": "Test",
            "last_name": "User",
            "email": "test@email.com",
            "username": "tuser",
            "password_hash": "$2b$13$IAJ2qLxIz6PVXqv1PAEDlewLjyTJWpuAfA/2UlIUPVfpq/4UQxenS",
            "role": "Subscriber"
        }, test_user.to_dict())

    # Fails <user.User object at 0x00000202AA900A10> != <user.User object at 0x00000202AA8C7D10>
    def test_build(self):
        test_user = User("Test", "User", "test@email", "tuser",
                         "$2b$13$IAJ2qLxIz6PVXqv1PAEDlewLjyTJWpuAfA/2UlIUPVfpq/4UQxenS", "Subscriber")

        self.assertEqual(test_user.build(dict), User(dict["first_name"], dict["last_name"], dict["email"],
                                                     dict["username"], dict["password_hash"], dict["role"]))

    def test_read_user(self):
        test_user = User("Test", "User", "test@email", "tuser",
                         "$2b$13$IAJ2qLxIz6PVXqv1PAEDlewLjyTJWpuAfA/2UlIUPVfpq/4UQxenS", "Subscriber")

        self.assertEqual(test_user.read_user("tuser", "test@email.com"),
                         [{
                           'first_name': 'Test',
                           'last_name': 'User',
                           'email': 'test@email.com',
                           'username': 'tuser',
                           'password_hash': '$2b$13$IAJ2qLxIz6PVXqv1PAEDlewLjyTJWpuAfA/2UlIUPVfpq/4UQxenS',
                           'role': 'Subscriber'}])

    # Fails TypeError: 'str' object is not callable
    def test_verify_password(self):
        test_user = User("Test", "User", "test@email", "tuser",
                         "$2b$13$IAJ2qLxIz6PVXqv1PAEDlewLjyTJWpuAfA/2UlIUPVfpq/4UQxenS", "Subscriber")

        self.assertEqual(test_user.verify_password("P@ssw0rd"), True)
