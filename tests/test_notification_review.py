# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-05-15
Last Modified: 2025-05-15

Description:
This file tests data layer Notification class.
"""
# ***************************************************************
import unittest
from logic.notification import Notification


# tests Notification class
class TestNotification(unittest.TestCase):
    def test_constructor(self):
        """
        Tests class constructor.
        :return: n/a
        """
        test_notification = Notification("2025-04-23", "Fresh Fruit", "Fresh fruit available.", 1011, 3, "Bob")

        self.assertEqual("2025-04-23", test_notification.date_sent())
        self.assertEqual("Fresh Fruit", test_notification.subject())
        self.assertEqual("Fresh fruit available.", test_notification.message())
        self.assertEqual(1011, test_notification.sender_id())
        self.assertEqual(3, test_notification.num_subscribers())
        self.assertEqual("Bob", test_notification.first_name())
