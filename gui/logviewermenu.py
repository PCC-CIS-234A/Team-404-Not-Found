# Sayan's logviewermenu.py
# Sayan Tajul - Team 404
# View Notifications with Search & Date Filter + Export to CSV

from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime
import csv
from tkinter import filedialog

# Using PCC Style Colors for everything
PCCblue = "#008099"
softcolorback = "#235578"
bgcolor = "#f5f5f5"

# Making a SQL Server Connection
def connect_database():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)

# Loading Messages (with keyword and date range if needed)
def load_messages(keyword="", start_date=None, end_date=None):
    conn = connect_database()
    cursor = conn.cursor()

    query = """
        SELECT subject, message, date_sent FROM notifications
        WHERE (subject LIKE ? OR message LIKE ?)
    """
    params = [f'%{keyword}%', f'%{keyword}%']

    if start_date and end_date:
        query += " AND date_sent BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    query += " ORDER BY date_sent DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# GUI Setup for Log Viewer
window = tk.Tk()
window.title("Notification Log Viewer - Team 404")
window.geometry("1000x600")
window.configure(bg=bgcolor)

# Header PCC style
tk.Label(window, text="Message History", font=("Helvetica", 18, "bold"), bg=bgcolor, fg=softcolorback).pack(pady=12)

# Search + Filter Bar PCC or professional looking
filter_frame = tk.Frame(window, bg=bgcolor)
filter_frame.pack(pady=5)

# Buttons
tk.Label(filter_frame, text="Search:", font=("Helvetica", 11), bg=bgcolor, fg=softcolorback).pack(side="left", padx=(10, 5))
search_box = tk.Entry(filter_frame, width=30)
search_box.pack(side="left")

# Date From
tk.Label(filter_frame, text="From:", font=("Helvetica", 11), bg=bgcolor, fg=softcolorback).pack(side="left", padx=(15, 5))
start_date = DateEntry(filter_frame, width=12, background=PCCblue, foreground="white", borderwidth=2)
start_date.pack(side="left")

# Date To
tk.Label(filter_frame, text="To:", font=("Helvetica", 11), bg=bgcolor, fg=softcolorback).pack(side="left", padx=(15, 5))
end_date = DateEntry(filter_frame, width=12, background=PCCblue, foreground="white", borderwidth=2)
end_date.pack(side="left")

# Filter and Other Button
def update_table():
    keyword = search_box.get().strip()
    start = start_date.get_date().strftime("%Y-%m-%d")
    end = end_date.get_date().strftime("%Y-%m-%d")
    for row in tree.get_children():
        tree.delete(row)
    for row in load_messages(keyword, start, end):
        tree.insert("", "end", values=(row[0], row[1], row[2].strftime("%Y-%m-%d %H:%M:%S")))

tk.Button(filter_frame, text="Search Messages", font=("Helvetica", 10, "bold"), bg=PCCblue, fg="white", command=update_table).pack(side="left", padx=(20, 10))

# Export to CSV if needed
def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Subject", "Message", "Date Sent"])
            for row_id in tree.get_children():
                row = tree.item(row_id)['values']
                writer.writerow(row)
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

# Table Like PCC style
columns = ("Subject", "Message", "Date Sent")
tree_frame = tk.Frame(window)
tree_frame.pack(padx=20, pady=15, fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=300 if col != "Date Sent" else 180)

tree.pack(side="left", fill="both", expand=True)
yscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=yscroll.set)
yscroll.pack(side="right", fill="y")

# Loading the initial data
for row in load_messages():
    tree.insert("", "end", values=(row[0], row[1], row[2].strftime("%Y-%m-%d %H:%M:%S")))

# Bottom Buttons Arranges
toolbar = tk.Frame(window, bg=bgcolor)
toolbar.pack(pady=10)

def go_back():
    messagebox.showinfo("Navigation", "This could return to send_notification.py")

tk.Button(toolbar, text="Send a New Message", font=("Helvetica", 10, "bold"), bg=softcolorback, fg="white", padx=10, command=go_back).pack(side="left", padx=10)
tk.Button(toolbar, text="Download as CSV", font=("Helvetica", 10, "bold"), bg=PCCblue, fg="white", padx=10, command=export_to_csv).pack(side="left", padx=10)

window.mainloop()