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

from tkinter import messagebox
from data.db_manager import Database

# -----------------------------------------------------------------------------
# Database Operations
# -----------------------------------------------------------------------------


def insert_or_update_template(
    name, category, subject, message, creator_id=1, original_name=None
):
    """
    Insert a new template or update an existing template in the database.

    Args:
        name (str): Template name.
        category (str): Template category.
        subject (str): Template subject.
        message (str): Template message body.
        creator_id (int, optional): ID of the creator. Defaults to 1.
        original_name (str, optional): Original name for lookup during update.

    Returns:
        None
    """
    conn = Database.connect()
    if conn:
        try:
            cursor = conn.cursor()

            # Determine whether this is an insert or update
            lookup_name = original_name if original_name else name

            cursor.execute(
                "SELECT template_id FROM dbo.templates WHERE name = ?",
                (lookup_name,)
            )
            existing = cursor.fetchone()

            if existing and not original_name:
                # Adding new but name already exists
                messagebox.showwarning(
                    "Duplicate Name",
                    f"A template named '{name}' already exists. "
                    "Please choose a different name."
                )
                return

            if existing:
                # Updating an existing template
                cursor.execute(
                    """
                    UPDATE dbo.templates
                    SET name       = ?,
                        category   = ?,
                        subject    = ?,
                        message    = ?,
                        creator_id = ?
                    WHERE template_id = ?
                    """,
                    (name, category, subject, message, creator_id, existing[0])
                )
                conn.commit()
                # Info message disabled to avoid duplicate popups
            else:
                # Adding a new template
                cursor.execute(
                    """
                    INSERT INTO dbo.templates
                        (creator_id, name, category, subject, message)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (creator_id, name, category, subject, message)
                )
                conn.commit()
                # Info message disabled to avoid duplicate popups

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
    else:
        messagebox.showerror("Connection Error", "Unable to connect to the database.")
