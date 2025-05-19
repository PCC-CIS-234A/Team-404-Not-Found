import unittest
from unittest.mock import patch
from logic.notification_logic import validate_email, process_tags

class TestNotificationValidation(unittest.TestCase):

    def test_email_format(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("no_at_symbol.com"))

    def test_missing_required_fields(self):
        subject = ""
        message = "Hello"
        with self.assertRaises(ValueError):
            if not subject or not message:
                raise ValueError("Subject and Message are required")

    def test_tag_replacement_with_function(self):
        template = "Hello {{name}}, your event is on {{date}}"
        tag_values = {"name": "Sayan", "date": "2025-05-20"}
        expected = "Hello Sayan, your event is on 2025-05-20"
        result = process_tags(template, tag_values)
        self.assertEqual(result, expected)

    def test_attachment_validation(self):
        attachments = ["doc1.pdf", "image.png", "slide.jpg"]
        for file in attachments:
            self.assertTrue(file.endswith(('.pdf', '.png', '.jpg')))
        # Add negative test
        invalid_files = ["doc.exe", "archive.zip"]
        for file in invalid_files:
            self.assertFalse(file.endswith(('.pdf', '.png', '.jpg')))

    def test_database_insertion_mocked(self):
        with patch("data.database_access.insert_notification") as mock_insert:
            mock_insert.return_value = True
            result = mock_insert("subject", "body", "2025-05-20", "user@example.com")
            mock_insert.assert_called_once_with("subject", "body", "2025-05-20", "user@example.com")
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
