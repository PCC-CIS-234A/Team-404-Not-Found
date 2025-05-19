# logic/template_logic.py

import pyodbc
from data.database_access import connecttoourdb

# Fetch all available template names (created by Santhil)
def fetch_template_names():
    conn = None
    try:
        conn = connecttoourdb()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM dbo.templates")
        template_names = [row[0] for row in cursor.fetchall()]
        return template_names
    except pyodbc.Error as e:
        print(f"Database Error (fetch_template_names): {e}")
        return []
    finally:
        if conn:
            conn.close()

# Fetch subject and message by template name
def fetch_template_by_name(template_name):
    conn = None
    try:
        conn = connecttoourdb()
        cursor = conn.cursor()
        cursor.execute("SELECT subject, message FROM dbo.templates WHERE name = ?", (template_name,))
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
        if conn:
            conn.close()
