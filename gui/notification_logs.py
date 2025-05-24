"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 2025-05-06

Description:
This file produces the GUI for the employee's to search for
notification logs by date range and displays
log results and details.
"""
# Modified version of search_logs_gui file by jasag
# Modified 5-22-2025 by RNixon
# Needs styling applied


from logic.logic_layer import search_logs

# GUI builder - Tkinter library
import tkinter as tk
from tkinter import ttk, messagebox, font
# Tkinter library to build calendar
from tkcalendar import DateEntry

from theme import *


class LogsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        top_frame = ttk.Frame(self)
        top_frame.pack(pady=20)

        ttk.Label(top_frame, text="Start: ").grid(row=0, column=0, padx=5)
        start_date_box = DateEntry(top_frame, width=12, background='#1690b4', foreground='white', borderwidth=2,
                                   date_pattern='yyyy-mm-dd')
        start_date_box.grid(row=0, column=1, padx=5)

        # Creates box for "end" date
        ttk.Label(top_frame, text="End: ").grid(row=0, column=2, padx=5)
        end_date_box = DateEntry(top_frame, width=12, background='#1690b4', foreground='white', borderwidth=2,
                                 date_pattern='yyyy-mm-dd')
        end_date_box.grid(row=0, column=3, padx=5)

        # Creates search button
        ttk.Button(top_frame, text="Search", command=lambda: search_click()).grid(row=0, column=4, padx=10)

        # Adds a treeview with column headers
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scroll through log data
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("Date & Time", "Subject",
                   "Message", "Sender", "# of Subscribers")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        # Settings for columns display
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=150, anchor=tk.W)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Connects log in treeview with display below
        tree.bind("<ButtonRelease-1>", lambda event: on_tree_click(event))

        # Displays details of the log clicked
        def on_tree_click(event):
            """
            Displays details of log selected in Log Details box below
            :param event: event object info about which column and row was clicked
            :return: None
            """
            item_id = tree.identify_row(event.y)
            clicked_column = tree.identify_column(event.x)

            if not item_id or not clicked_column:
                return

            col_index = int(clicked_column.replace("#", "")) - 1
            values = tree.item(item_id, "values")

            if 0 <= col_index < len(values):
                selected_value = values[col_index]
                details_text.set(f"{columns[col_index]}: {selected_value}")

        details_frame = tk.Frame(self)
        details_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        details_text = tk.StringVar()
        ttk.Label(details_frame, text="Log Details: ").pack(anchor=tk.W, pady=5)
        (ttk.Label(details_frame, textvariable=details_text, justify=tk.LEFT, anchor=tk.W)
            .pack(fill=tk.BOTH, padx=10, pady=10))

        def search_click():
            """
            Creates search button functionality
            :return: None
            """
            start_date = start_date_box.get()
            end_date = end_date_box.get()

            # Error handling -- Don't need this with calendar feature?
            if not start_date or not end_date:
                messagebox.showerror("Error", "Start date and end date cannot be empty")
                return

            if start_date > end_date:
                messagebox.showerror("Error", "Start date cannot be greater than end date")
                return

            try:
                results = search_logs(start_date, end_date)
            except ValueError:
                messagebox.showerror("Error", "No records for that date range.  Please try again.")
                return

            # Clears results
            tree.delete(*tree.get_children())

            # Displays results of search from database
            if not results:
                messagebox.showerror("Error", "No notification logs for that date range.  Please try again.")
            else:
                for row in results:
                    tree.insert('', tk.END, values=(row["date_sent"], row["subject"], row["message"],
                                                    row["first_name"], row["num_subscribers"]))
