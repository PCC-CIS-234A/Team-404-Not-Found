# =============================================================================
# Author:        Santhil Murugesan
# Last Modified 06/06/2025 by Sayan
# File:          template_logic.py
# Created:       04/25/2025
# Project:       Food Pantry Notification System
# Module:        Template Manager (db_connection.py, template_logic.py,
#                template_creator_gui.py, and theme.py)
# Description:   Contains business logic for template operations (CRUD).
# Functionality: Handles inserting, updating, deleting, and fetching
#                template data from the database.
# Output:        Database transactions and application data updates.
# References:    Python Documentation, SQL Server (pyodbc)
# =============================================================================

# from tkinter import messagebox
from data.db_manager import Database


def insert_or_update_template(name, category, subject, message, creator_id=1, original_name=None):
    """
    Insert a new template or update an existing template in the database.
    Delegates to the db_manager.Database class.
    """
    Database.insert_or_update_template(name, category, subject, message, creator_id, original_name)


def fetch_template_names():
    """
    Fetch all template names from the database (for dropdown/list display).
    Delegates to the db_manager.Database class.
    """
    return Database.fetch_template_names()


def fetch_template_by_name(name):
    """
    Fetch a single template's details by name (case-insensitive, trimmed).
    Delegates to the db_manager.Database class.
    """
    return Database.fetch_template_by_name(name.strip())
