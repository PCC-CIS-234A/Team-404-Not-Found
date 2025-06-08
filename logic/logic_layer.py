# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 06/06/2025 by Sayan

Description:
This file is the logic layer, which requests data from
the data layer and validates date and time input.
"""
# ***************************************************************
from datetime import datetime
from data.db_manager import Database


# Requests data from data layer and validates input
def search_logs(start_date_str, end_date_str):
    """
    Fetches notification log data from data layer, converts date strings to datetime objects,
    validates start date before end date,turns notification log objects into dictionaries, returns
    error if start date before end date or if trouble retrieving data
    :param start_date_str:start date formatted as YYYY-MM-DD
    :param end_date_str: end date formatted as YYYY-MM-DD
    :return:list of notification log dictionaries, with each dictionary representing a notification log
    """
    try:
        # Converts date strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid start date or end date")
    # Validates start date before end date
    if start_date > end_date:
        raise ValueError("Start date cannot come after end date.")

    # Calls Database class method to get log data objects
    try:
        notifications = Database.get_notification_log(start_date, end_date)
    # Returns error if trouble retrieving data
    except Exception as e:
        raise ValueError(f"Error getting notification logs: {str(e)}")

    # Turns notification log objects into dictionaries
    result = []
    for n in notifications or []:
        result.append({
            # Dictionary keys
            "date_sent": n.date_sent.strftime("%Y-%m-%d %H:%M:%S"),
            "subject": n.subject,
            "message": n.message,
            "first_name": n.first_name,
            "num_subscribers": n.num_subscribers
        })

    return result
