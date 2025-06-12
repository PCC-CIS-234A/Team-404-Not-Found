# Sayan Tajul
# 06/06/2025
# Test Logic Review

import unittest
from unittest.mock import patch
# from unittest.mock import MagicMock
from logic.logs_logic_layer import search_logs
from datetime import datetime


class TestSearchLogs(unittest.TestCase):

    def test_invalid_date_format_error(self):
        """Invalid format should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            search_logs("04-23", "04-30")
        self.assertIn("Invalid start date", str(context.exception))

    def test_start_date_after_end_error(self):
        """Start date after end date should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            search_logs("2025-05-23", "2025-04-23")
        self.assertIn("Start date cannot come after end date", str(context.exception))

    @patch("logic.logic_layer.Database.get_notification_log")
    def test_database_error(self, mock_db_call):
        """Simulate database failure"""
        mock_db_call.side_effect = Exception("DB is down")
        with self.assertRaises(ValueError) as context:
            search_logs("2025-05-01", "2025-05-10")
        self.assertIn("Error getting notification logs", str(context.exception))

    @patch("logic.logic_layer.Database.get_notification_log")
    def test_no_notifications_returns_empty_list(self, mock_db_call):
        """Simulate no data in DB (empty list returned)"""
        mock_db_call.return_value = []
        result = search_logs("2025-05-01", "2025-05-10")
        self.assertEqual(result, [])

    @patch("logic.logic_layer.Database.get_notification_log")
    def test_valid_logs_returned(self, mock_db_call):
        """Simulate valid log entries from DB"""
        mock_notification = type("MockLog", (), {
            "date_sent": datetime(2025, 5, 10, 15, 30),
            "subject": "Reminder",
            "message": "Don't forget!",
            "first_name": "Alice",
            "num_subscribers": 5
        })()
        mock_db_call.return_value = [mock_notification]

        result = search_logs("2025-05-01", "2025-05-15")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["first_name"], "Alice")
        self.assertIn("subject", result[0])
