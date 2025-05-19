import pyodbc
import tkinter as tk
import re

def prompt_for_tags(template_str):
    tags = list(set(re.findall(r"\{\{(.*?)\}\}", template_str)))
    if not tags:
        return {}

    # Only one popup window
    top = tk.Toplevel()
    top.title("Fill in Template Tags")
    top.configure(bg="#f5f5f5")

    # Set desired popup size and center position
    popup_width = 500
    popup_height = 400
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_pos = int((screen_width / 2) - (popup_width / 2))
    y_pos = int((screen_height / 2) - (popup_height / 2))
    top.geometry(f"{popup_width}x{popup_height}+{x_pos}+{y_pos}")

    tag_descriptions = {
        "campus_location": "Which campus is this offer available at?",
        "start_date": "When does the availability start?",
        "end_date": "When does the availability end?",
        "item_name": "What is the item name?",
        "discount": "How much is the discount?",
        "reason": "Why is the pantry closed?",
        "closure_date": "What is the closure date?",
        "reopening_date": "What is the reopening date?",
        "availability_start": "When will the food item become available?",
        "availability_end": "Until when will the food item be available?",
        "food_item": "What is the name of the food item?",
        "event_name": "What is the name of the event?",
        "date": "What date will the event happen?",
        "time": "What time will the event start?",
        "location": "Where is the event taking place?",
        "low_stock_item": "Which item is currently low in stock?"
    }

    user_filled_tags = {}

    tk.Label(top, text="Please fill in the missing details below:", font=("Helvetica", 12, "bold"),
             bg="#f5f5f5").pack(pady=(10, 10))

    entries = {}

    for tag in tags:
        friendly_prompt = tag_descriptions.get(tag, f"Enter value for: {tag}")
        tk.Label(top, text=friendly_prompt, bg="#f5f5f5").pack()
        entry = tk.Entry(top, width=50)
        entry.pack(pady=(0, 5))
        entries[tag] = entry

    def submit_tags():
        for tag, entry in entries.items():
            user_filled_tags[tag] = entry.get().strip()
        top.destroy()

    submit_btn = tk.Button(top, text="Submit", bg="#008099", fg="white", command=submit_tags)
    submit_btn.pack(pady=(10, 10))

    top.grab_set()
    top.wait_window()

    return user_filled_tags

def connecttoourdb():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)

def fetch_available_tags():
    try:
        conn = connecttoourdb()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tag_name FROM dbo.tags")
        tags = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tags
    except Exception as e:
        print("Error fetching tags:", e)
        return []

