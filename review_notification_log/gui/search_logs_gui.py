# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 2025-04-25

Description:
This file produces the GUI for the employee's to search for
notification logs by date range and displays
log results and details.
"""
# ***************************************************************
from logic.logic_layer import search_logs

# GUI builder
import tkinter as tk
from tkinter import ttk, messagebox
# Datetime class from built-in module
from datetime import datetime, timedelta

# Function to generate list of dates
def generate_dates(days=30):
    base = datetime.today()
    return [(base + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

# Function to display details of a log once clicked
def display_log_details(event):
    selected_item = tree.selection()[0]
    row_data = tree.item(selected_item, "values")

    details_text.set(f"Date & Time: {row_data[0]}\n"
                     f"Subject: {row_data[1]}\n"
                     f"Message: {row_data[2]}\n"
                     f"Sender: {row_data[3]}\n"
                     f"# of Subscribers: {row_data[4]}")

# Test function to test GUI search - will need to go into logic layer
#def search_logs(start_date, end_date):
    #return []

# Search button click
def search_click():
    start_date = start_date_box.get()
    end_date = end_date_box.get()

    results = search_logs(start_date, end_date)
    # Gets current search's logs and deletes older search logs
    for row in tree.get_children():
        tree.delete(row)
    if not results:
        messagebox.showerror("Error. Invalid date range.", "Please enter a new date range.")
    else:
        for row in results:
    # Adds log to GUI view
            tree.insert('', tk.END, values=row)

# Creates main window
root = tk.Tk()
root.title("Notification Logs Search")
root.geometry("900x400")
# Use Team chosen color
root.configure(background='#008099')
text_color = "1690b4"

# Gets list of dates
date_option = generate_dates()

# Top frame
top_frame = ttk.Frame(root)
top_frame.pack(pady=10)

# Creates box for "start" date
ttk.Label(top_frame, text="Start: ").grid(row=0, column=0, padx=5)
start_date_box = ttk.Combobox(top_frame, values=date_option, state="readonly")
start_date_box.grid(row=0, column=1, padx=5)

# Creates box for "end" date
ttk.Label(top_frame, text="To: ").grid(row=0, column=2, padx=5)
end_date_box = ttk.Combobox(top_frame, values=date_option, state="readonly")
end_date_box.grid(row=0, column=3, padx=5)

# Creates search button
ttk.Button(top_frame, text="Search", command=search_click).grid(row=0, column=4, padx=10)

# Adds a treeview with column headers
tree_frame = ttk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Scroll through log data
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

columns = ("Date & Time", "Subject",
           "Message", "Sender", "# of Subscribers")
tree = ttk.Treeview(tree_frame, columns=columns, show ="headings", yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

# Settings for columns display
for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=100)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Connects log in treeview with display below
tree.bind("<ButtonRelease-1>", display_log_details)

# Displays details of the log clicked
details_frame = tk.Frame(root)
details_frame.pack(fill=tk.BOTH, padx=10, pady=10)

details_text = tk.StringVar()
details_label = ttk.Label(details_frame, text="Log Details: ")
details_label.pack(anchor=tk.W, pady=5)
details_display = ttk.Label(details_frame, textvariable=details_text, justify=tk.LEFT, anchor=tk.W)
details_display.pack(fill=tk.BOTH, padx=10, pady=10)


# Test data to test GUI - will need to move to data access layer
test_data = [
    ("2025-04-18 10:00", "New Items",
     "Fresh vegetables available for pick up.", "Bob Smith", "20"),
]

# Test log data to test GUI
for row in test_data:
    tree.insert('', tk.END, values=row)

root.mainloop()
