# =============================================================================
# Author:        Santhil Murugesan
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

from data.db_manager import Database

def insert_or_update_template(name, category, subject, message, creator_id=1, original_name=None):
    """Insert or update a template using Database class."""
    return Database.insert_or_update_template(
        name=name,
        category=category,
        subject=subject,
        message=message,
        creator_id=creator_id,
        original_name=original_name
    )


def fetch_template_by_name(name):
    """Fetch template details by name."""
    return Database.fetch_template_by_name(name)


def fetch_template_names():
    """Return all available template names."""
    return Database.fetch_template_names()









