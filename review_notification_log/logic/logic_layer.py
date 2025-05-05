# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 2025-05-05

Description:
This file is the logic layer, which requests data from
the data layer and validates date and time input.
"""
# ***************************************************************
from datetime import datetime
from data.notification_db import Database


# Requests data from data layer and validates input
def search_logs(start_date_str, end_date_str):
    try:
        # Converts date strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid start date or end date")

    if start_date > end_date:
        raise ValueError("Start date cannot come after end date.")

# Calls Database class method to get log data objects
    try:
        notifications = Database.get_notification_log(start_date, end_date)
    except Exception as e:
           raise ValueError(f"Error getting notification logs: {str(e)}")

# Turns notification log objects into dictionaries
    result = []
    for n in notifications or []:
        result.append({
            "date_sent" : n.date_sent.strftime("%Y-%m-%d %H:%M:%S"),
            "subject" : n.subject,
            "message" : n.message,
            "sender_id" : n.sender_id,
            "num_subscribers" : n.num_subscribers
        })

    return result


    # Uses test data instead fo database data
    #except Exception as e:
        #print("{e}")
        #return[
            #("2025-04-18 10:00", "New Items",
            #"Fresh vegetables available for pickup.", "Bob Smith", "20")
        #]
