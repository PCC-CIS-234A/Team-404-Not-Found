# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 2025-04-28

Description:
This file is the logic layer, which requests data from
the data layer and validates date and time input.
"""
# ***************************************************************
from datetime import datetime
from data.notification_db import Database


# Requests data from data layer and validates input
def search_logs(start_date: datetime, end_date: datetime):
    if start_date > end_date:
        return[]
    return Database.get_notification_log(start_date, end_date)
