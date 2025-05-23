# =============================================================================
# Author:        Santhil Murugesan
# File:          db_connection.py
# Created:       04/25/2025
# Project:       Food Pantry Notification System
# Module:        All modules in this project use this file as a common resource.
# Description:   Provides database connectivity for template management.
# Functionality: Establishes and manages SQL Server connections.
# Output:        Database connection objects for CRUD operations.
# References:    Python Documentation, pyodbc Library
# =============================================================================

import pyodbc

# -----------------------------------------------------------------------------
# Database Connection
# -----------------------------------------------------------------------------


def get_connection():
    """
    Establish a connection to the SQL Server database.

    Returns:
        pyodbc.Connection or None: Active connection object if successful, otherwise None.
    """
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=cisdbss.pcc.edu;'
            'DATABASE=CIS234A_404 Team Not Found;'
            'UID=CIS234A_404 Team Not Found;'
            'PWD=NoErrors&2;'
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

# -----------------------------------------------------------------------------
# Example Fetch Function
# -----------------------------------------------------------------------------


def fetch_users():
    """
    Example function to fetch and print all users from the database.

    Returns:
        None
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, email, role, created_date FROM dbo.users"
            )
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print("Error fetching users:", e)
        finally:
            conn.close()

# -----------------------------------------------------------------------------
# Test Runner
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    fetch_users()
