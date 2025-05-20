# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-05-15
Last Modified: 2025-05-15

Description:
This file tests logic layer search_logs.
"""
# ***************************************************************
import unittest
from unittest import result
from logic.logic_layer import search_logs


# tests logic layer search_logs
class TestSearchLogs(unittest.TestCase):

    def test_invalid_date_format_error(self):
        """
        Tests invalid date format error.
        :return: n/a
        """
        with self.assertRaises(ValueError):
            search_logs("04-23", "04-30")
        self.assertIn("Invalid date format", str(result))

    def test_start_date_after_end_error(self):
        """
        Tests start date after end date error.
        :return: n/a
        """
        with self.assertRaises(ValueError):
            search_logs("2025-05-23", "2025-04-23")
        self.assertIn("Invalid start date", str(result))
        self.assertIn("Invalid end date", str(result))

    def test_database_error(self):
        """
        Tests database error.
        :return: n/a
        """
        with self.assertRaises(ValueError):
            search_logs("2025-05-23", "2025-04-23")
        self.assertIn("Database error", str(result))

    def test_no_notifications(self):
        """
        Tests no notifications error.
        :return: n/a
        """
        with self.assertRaises(ValueError):
            search_logs("2025-05-23", "2025-04-23")
        self.assertIn("No notifications found", str(result))
