# Sayan Tajul
# 06/06/2025
# Test Notification Logic

import unittest
from logic.notification_logic import validate_email, send_email_to_subscribers
from unittest.mock import patch, MagicMock

class TestNotificationLogic(unittest.TestCase):

    def test_valid_email(self):
        self.assertTrue(validate_email("test@example.com"))

    def test_invalid_email(self):
        self.assertFalse(validate_email("invalid-email"))

    @patch("logic.notification_logic.smtplib.SMTP_SSL")
    def test_send_email_to_valid_subscribers(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        subscribers = [
            {"first_name": "Alice", "email": "alice@example.com"},
            {"first_name": "Bob", "email": "bob@example.com"}
        ]
        subject = "Hello {{first_name}}"
        message = "This is a test message for {{first_name}} on {{date}}"

        try:
            send_email_to_subscribers(subject, message, subscribers)
        except Exception:
            self.fail("send_email_to_subscribers() raised Exception unexpectedly!")

        self.assertEqual(mock_server.send_message.call_count, 2)
        mock_server.quit.assert_called_once()

    @patch("logic.notification_logic.smtplib.SMTP_SSL")
    def test_invalid_email_skipped(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        subscribers = [
            {"first_name": "Charlie", "email": "invalid-email"}
        ]
        send_email_to_subscribers("Sub", "Msg", subscribers)
        mock_server.send_message.assert_not_called()
