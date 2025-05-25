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
<<<<<<< HEAD
from data.db_manager import Database
=======
from data.db_connection import get_connection
>>>>>>> santhil_template_creation

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
<<<<<<< HEAD
    conn = Database.connect()
=======
    conn = get_connection()
>>>>>>> santhil_template_creation
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
<<<<<<< HEAD
=======


def fetch_template_by_name(name):
    """
    Fetch a single template's details by its name.

    Args:
        name (str): The name of the template to fetch.

    Returns:
        tuple or None: Template data (name, category, subject, message) or None if not found.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, category, subject, message
                FROM dbo.templates
                WHERE name = ?
                """,
                (name,)
            )
            return cursor.fetchone()
        except Exception as e:
            print("Fetch error:", e)
        finally:
            conn.close()
    return None


def fetch_template_names():
    """
    Fetch a list of all distinct template names from the database.

    Returns:
        list: A list of template names.
    """
    conn = get_connection()
    names = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT name FROM dbo.templates"
            )
            rows = cursor.fetchall()
            names = [row[0] for row in rows if row[0]]
        except Exception as e:
            print("Error fetching template names:", e)
        finally:
            conn.close()
    return names
>>>>>>> santhil_template_creation
