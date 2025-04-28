import pyodbc

# Connect to your same database
def connect_to_db():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)

# Fetch all template names
def fetch_template_names():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM templates")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]

# Fetch subject and message for a given template name
def fetch_template_by_name(template_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT subject, message FROM templates WHERE name = ?", (template_name,))

    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0], result[1]
    else:
        return "", ""
