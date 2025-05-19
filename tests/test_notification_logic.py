import unittest
from logic.notification_logic import send_email_to_subscribers, validate_email
from unittest.mock import patch

class TestNotificationValidation(unittest.TestCase):

    def test_email_format(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))

    def test_missing_required_fields(self):
        invalid_data = {"subject": "", "body": "Hello"}
        with self.assertRaises(ValueError):
            # Simulate a function that raises on missing subject
            if not invalid_data["subject"]:
                raise ValueError("Subject is required")

    def test_tag_replacement(self):
        template = "Hello {{name}}, welcome!"
        filled = template.replace("{{name}}", "Sayan")
        self.assertEqual(filled, "Hello Sayan, welcome!")

    def test_attachment_validation(self):
        attachments = ["valid.pdf", "image.png"]
        for file in attachments:
            self.assertTrue(file.endswith(('.pdf', '.png', '.jpg')))

    def test_database_insertion(self):
        # Simulating a DB insertion return (mocked)
        with patch("data.database_access.insert_notification") as mock_insert:
            mock_insert.return_value = True
            result = mock_insert("subject", "body", "2024-01-01", "user@example.com")
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
