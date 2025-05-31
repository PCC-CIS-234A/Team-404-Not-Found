# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 2025-05-31

Description:
This file is the logic layer, which requests data from
the data layer and validates date and time input.
"""
# ***************************************************************
from datetime import datetime, timedelta
from data.notification_db import Database


# UPDATED Sprint#2 A9 Requests data from data layer and validates input
def search_logs(start_date_str, end_date_str, sort_by=None, sort_order="ASC"):
    """
    Fetches notification log data from data layer, converts date strings to datetime objects,
    validates start date before end date,turns notification log objects into dictionaries, returns
    error if start date before end date or if trouble retrieving data.  Optional sorting by column.
    :param start_date_str:start date formatted as YYYY-MM-DD
    :param end_date_str: end date formatted as YYYY-MM-DD
    :param sort_by: optional column sort by
    :param sort_order: "asc" or "desc"
    :return:list of notification log dictionaries, with each dictionary representing a notification log
    """
    print("LOGIC LAYER -start:", start_date_str, "-end:", end_date_str)
    try:
        # Converts date strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        # Fix not getting records from end of date
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
    except ValueError:
        raise ValueError("Invalid start date or end date")
    print("LOGIC LAYER -converted:", start_date, end_date)
    # Validates start date before end date
    if start_date > end_date:
        raise ValueError("Start date cannot come after end date.")

    # Calls Database class method to get log data objects
    try:
        #Updated Sprint#2 A9
        notifications = Database.get_notification_log(start_date, end_date, sort_by, sort_order)
        print("LOGIC LAYER -db returned:", len(notifications), "notifications")
    # Returns error if trouble retrieving data
    except Exception as e:
        print("LOGIC LAYER -db error:", e)
        raise ValueError(f"Error getting notification logs: {str(e)}")

    # Turns notification log objects into dictionaries
    result = []
    for n in notifications or []:
        result.append({
            # Dictionary keys
            "date_sent" : n.date_sent.strftime("%Y-%m-%d %H:%M:%S"),
            "subject" : n.subject,
            "message" : n.message,
            "first_name" : n.first_name,
            "num_subscribers" : n.num_subscribers
        })

    print("Logic LAYER -returning:", len(result), "results")
    return result

# NEW Sprint#2 A8 search_logs_keyword logic
def search_logs_keyword(keyword):
    """
    Fetches notification log data by keyword from data layer,
    validates keyword and returns notification log objects,
    converts results to dictionaries
    :param keyword: text to search
    :return: list of log dictionaries
    """
    if not keyword:
        raise ValueError("Keyword cannot be empty")

    try:
        notifications = Database.search_logs_keyword(keyword)
    except Exception as e:
        raise ValueError(f"Error getting notification logs: {str(e)}")
    result = []
    for n in notifications or []:
        result.append({
            "date_sent" : n.date_sent.strftime("%Y-%m-%d %H:%M:%S"),
            "subject" : n.subject,
            "message" : n.message,
            "first_name" : n.first_name,
            "num_subscribers" : n.num_subscribers
        })

    return result
