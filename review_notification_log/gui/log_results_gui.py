# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-16
Last Modified: 2025-04-18

Description:
This file produces the GUI with the results of the
notification logs search.
"""
# ***************************************************************

# GUI builder
import tkinter as tk
from tkinter import ttk

# Test data to test GUI - will need to move to data access layer
test_data = [
    ("2025-04-18 10:00", "New Items",
     "Fresh vegetables available for pick up.", "Bob Smith", "20"),
]

# Creates main window
root = tk.Tk()
root.title("Notification Log Search Results")
root.geometry("800x300")
# Use Team chosen color
root.configure(background='#008099')
text_color = "1690b4"

# Centering Frame
center_frame = tk.Frame(root)
center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Adds a treeview with column headers
columns = ("Date & Time", "Subject",
           "Message", "Sender", "# of Subscribers" )
tree = ttk.Treeview(center_frame, columns=columns, show ="headings")

tree.heading("Date & Time", text="Date & Time")
tree.heading("Subject", text="Subject")
tree.heading("Message", text="Message")
tree.heading("Sender", text="Sender")
tree.heading("# of Subscribers", text="# of Subscribers")

tree.column("Date & Time", width=140)
tree.column("Subject", width=140)
tree.column("Message", width=300)
tree.column("Sender", width=100)
tree.column("# of Subscribers", width=50)

# Scroll through log data
scrollbar = ttk.Scrollbar(center_frame, orient="vertical",
                          command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Test log data to test GUI
for row in test_data:
    tree.insert('', tk.END, values=row)

root.mainloop()
