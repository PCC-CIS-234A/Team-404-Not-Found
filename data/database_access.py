# data/database_access.py
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
