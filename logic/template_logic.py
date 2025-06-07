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

from tkinter import messagebox
from data.db_manager import Database

# ---------------------------------------------------------------------------
# Database Operations
# ---------------------------------------------------------------------------

def insert_or_update_template(name, category, subject, message, creator_id=1, original_name=None):
    """
    Insert a new template or update an existing template in the database.
    """
    conn = Database.connect()
    if conn:
        try:
            cursor = conn.cursor()
            lookup_name = original_name if original_name else name

            cursor.execute(
                "SELECT template_id FROM dbo.templates WHERE name = ?",
                (lookup_name,)
            )
            existing = cursor.fetchone()

            if existing and not original_name:
                messagebox.showwarning(
                    "Duplicate Name",
                    f"A template named '{name}' already exists. "
                    "Please choose a different name."
                )
                return

            if existing:
                cursor.execute(
                    """
                    UPDATE dbo.templates
                    SET name = ?, category = ?, subject = ?, message = ?, creator_id = ?
                    WHERE template_id = ?
                    """,
                    (name, category, subject, message, creator_id, existing[0])
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO dbo.templates (creator_id, name, category, subject, message)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (creator_id, name, category, subject, message)
                )
            conn.commit()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
    else:
        messagebox.showerror("Connection Error", "Unable to connect to the database.")


def fetch_template_by_name(name):
    """
    Fetch a single template's details by its name.
    """
    conn = Database.connect()
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
    """
    conn = Database.connect()
    names = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT name FROM dbo.templates")
            rows = cursor.fetchall()
            names = [row[0] for row in rows if row[0]]
        except Exception as e:
            print("Error fetching template names:", e)
        finally:
            conn.close()
    return names
