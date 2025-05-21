class Notification:

    def __init__(self, date_sent, subject, message, sender_id, num_subscribers, first_name):
        """
        Defines Notification class
        :param date_sent: datetime, date and time of notification sent
        :param subject: string, subject of the notification
        :param message: string, message of the notification
        :param sender_id: int, id of the sender of the notification
        :param num_subscribers: int, number of subscribers notified
        :param first_name: str, name of the person who sent the notification
        """
        self.date_sent = date_sent
        self.subject = subject
        self.message = message
        self.sender_id = sender_id
        self.num_subscribers = num_subscribers
        self.first_name = first_name
