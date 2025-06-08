# Sayan Tajul
# 06/06/2025
# Test User

import unittest
from logic.user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("John", "Doe", "john@example.com", "johndoe", "hashedpwd", "Manager")

    def test_user_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["role"], "Subscriber")  # hardcoded in method

    def test_build_user(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "username": "janesmith",
            "password_hash": "abc123",
            "role": "Manager"
        }
        user = User.build(data)
        self.assertEqual(user.get_first_name(), "Jane")
        self.assertEqual(user.get_role(), "Manager")

    def test_verify_password_hashing_and_verification(self):
        plain_password = "securepassword"
        hashed = User.hash_password(plain_password)
        self.assertIsInstance(hashed, str)

        user = User("First", "Last", "test@test.com", "user123", hashed, "Manager")
        self.assertTrue(user.verify_password(plain_password))

    def test_invalid_password_verification(self):
        plain_password = "securepassword"
        wrong_password = "wrongpass"
        hashed = User.hash_password(plain_password)
        user = User("First", "Last", "test@test.com", "user123", hashed, "Manager")
        self.assertFalse(user.verify_password(wrong_password))
