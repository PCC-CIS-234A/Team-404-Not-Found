# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-16
Last Modified: 2025-04-18

Description:
This file produces the GUI for the employee's to search for
notification logs by date range.
"""
# ***************************************************************

# GUI builder
import tkinter as tk
from tkinter import ttk, messagebox
# Datetime class from built-in module
from datetime import datetime, timedelta

# Function to generate list of dates
def generate_dates(days=30):
    base = datetime.today()
    return [(base + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

# Test function to test GUI search - will need to go into logic layer
def search_logs(from_date, to_date):
    return []

# Search button click
def search_click():
    from_date = from_date_box.get()
    to_date = to_date_box.get()

    results = search_logs(from_date, to_date)
    if not results:
        messagebox.showerror("Error. Invalid date range.", "Please enter a new date range.")
    else:
        print(results)

# Creates main window
root = tk.Tk()
root.title("Notification Logs Search")
root.geometry("400x200")
# Use Team chosen color
root.configure(background='#008099')
text_color = "1690b4"

# Gets list of dates
date_option = generate_dates()

# Centering frame
center_frame = ttk.Frame(root)
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Creates box for "from" date
ttk.Label(center_frame, text="From: ").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
from_date_box = ttk.Combobox(center_frame, values=date_option, state="readonly")
from_date_box.grid(row=0, column=1, padx=10, pady=10)

# Creates box for "to" date
ttk.Label(center_frame, text="To: ").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
to_date_box = ttk.Combobox(center_frame, values=date_option, state="readonly")
to_date_box.grid(row=1, column=1, padx=10, pady=10)

# Creates search button
ttk.Button(center_frame, text="Search").grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
