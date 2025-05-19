import pyodbc
import os

# Connecting to our Database in SQL Server (CIS 234A Team 404 not found)
def connecttoourdb():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)

# Stub function for unit testing
def insert_notification(subject, message, date_sent, recipient_email):
    print(f"Inserting: {subject}, {message}, {date_sent}, {recipient_email}")
    return True

def get_subscribers():
    conn = connecttoourdb()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, email FROM dbo.users WHERE role = 'subscriber'")
    result = [{"first_name": row[0], "email": row[1]} for row in cursor.fetchall()]
    conn.close()
    return result

def get_sender_id(username):
    conn = connecttoourdb()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM dbo.users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def log_notification(subject, message, recipient_count, sender_id, attachments):
    conn = connecttoourdb()
    cursor = conn.cursor()
    attachment_names = ", ".join([os.path.basename(file) for file in attachments])
    cursor.execute("""
        INSERT INTO dbo.notifications (subject, message, date_sent, num_subscribers, sender_id, attachment_names)
        VALUES (?, ?, GETDATE(), ?, ?, ?)
    """, (subject, message, recipient_count, sender_id, attachment_names))
    conn.commit()
    conn.close()

def get_all_tags():
    conn = connecttoourdb()
    cursor = conn.cursor()
    cursor.execute("SELECT tag_name FROM dbo.tags")
    tags = [f"{{{row[0]}}}" for row in cursor.fetchall()]  # Wrap each with {}
    conn.close()
    return tags
