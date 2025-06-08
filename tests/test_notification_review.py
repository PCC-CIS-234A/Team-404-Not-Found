# Sayan Tajul
# 06/06/2025
# Test Notification Review

import unittest
from unittest.mock import patch, MagicMock
from logic import template_logic

class TestNotificationReview(unittest.TestCase):

    @patch("logic.template_logic.Database.connect")
    def test_fetch_template_by_name_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("Template1", "CategoryA", "SubjectA", "MessageA")
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = template_logic.fetch_template_by_name("Template1")
        self.assertEqual(result[0], "Template1")

    @patch("logic.template_logic.Database.connect")
    def test_fetch_template_by_name_not_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = template_logic.fetch_template_by_name("MissingTemplate")
        self.assertIsNone(result)

    @patch("logic.template_logic.Database.connect")
    def test_fetch_template_names(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("Welcome",), ("Update",)]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        names = template_logic.fetch_template_names()
        self.assertIn("Welcome", names)
        self.assertEqual(len(names), 2)
