# database_access.py
# Data Layer - Handles all SQL Server interactions for the Notification System

import pyodbc
import os  # For extracting filenames from attachment paths

# Database connection function (used by all data layer functions)
def connecttoourdb():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)

# Insert notification during unit testing (this is a stub, not used in production)
def insert_notification(subject, message, date_sent, recipient_email):
    print(f"Inserting: {subject}, {message}, {date_sent}, {recipient_email}")
    return True

# et all subscribers' names and emails
def get_subscribers():
    conn = connecttoourdb()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, email FROM dbo.users WHERE role = 'subscriber'")
    result = [{"first_name": row[0], "email": row[1]} for row in cursor.fetchall()]
    conn.close()
    return result

# Get sender's user_id by username
def get_sender_id(username):
    conn = connecttoourdb()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM dbo.users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Log a notification after sending
def log_notification(subject, message, recipient_count, sender_id, attachments):
    conn = connecttoourdb()
    cursor = conn.cursor()
    attachment_names = ", ".join([os.path.basename(file) for file in attachments])  # Only file names
    cursor.execute("""
        INSERT INTO dbo.notifications (subject, message, date_sent, num_subscribers, sender_id, attachment_names)
        VALUES (?, ?, GETDATE(), ?, ?, ?)
    """, (subject, message, recipient_count, sender_id, attachment_names))
    conn.commit()
    conn.close()

# Fetch all tag names from the 'tags' table and format with curly brackets
def get_all_tags():
    try:
        conn = connecttoourdb()
        cursor = conn.cursor()
        cursor.execute("SELECT tag_name FROM dbo.tags")
        tags = [f"{{{row[0]}}}" for row in cursor.fetchall()]  # Wrap each tag with {}
        conn.close()
        return tags
    except Exception as e:
        print("Error fetching tags from database:", e)
        return []
