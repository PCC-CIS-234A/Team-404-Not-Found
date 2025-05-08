"""
Author: R-Nixon
Creation Date: 2025-5-2
Last Modified: 2025-5-2

Description:
This module destroys and recreates the tables in the SQL database.
"""
from db_manager import Database

if __name__ == '__main__':
    Database.rebuild_data()
