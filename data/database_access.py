import pyodbc

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

# Stub function for unit testing (I can later add real DB insert here)
def insert_notification(subject, message, date_sent, recipient_email):
    print(f"Inserting: {subject}, {message}, {date_sent}, {recipient_email}")
    return True  # Simulating a successful insert
