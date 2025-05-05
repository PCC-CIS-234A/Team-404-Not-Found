# My import
import pyodbc

# Database connection (Reusable across functions) (Team 404 Not Found)
def connect_to_db():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)

# Fetching all available template names from our database made by Santhil
def fetch_template_names():
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM templates")
        templates = [row[0] for row in cursor.fetchall()]
        return templates
    except pyodbc.Error as e:
        print(f"Database Error (fetch_template_names): {e}")
        return []
    finally:
        conn.close()

# Fetching subject and message content for the selected template name from Santhil
def fetch_template_by_name(template_name):
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT subject, message FROM templates WHERE name = ?", (template_name,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            print(f"Template '{template_name}' not found.")
            return "", ""
    except pyodbc.Error as e:
        print(f"Database Error (fetch_template_by_name): {e}")
        return "", ""
    finally:
        conn.close()
