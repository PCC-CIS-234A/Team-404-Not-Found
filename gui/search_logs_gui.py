# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-25
Last Modified: 2025-05-06

Description:
This file produces the GUI for the employee's to search for
notification logs by date range and displays
log results and details.
"""
# ***************************************************************
from logic.logic_layer import search_logs

# GUI builder - Tkinter library
import tkinter as tk
from tkinter import ttk, messagebox, font
# Tkinter library to build calendar
from tkcalendar import DateEntry


# Code wrapper to run app through main.py
def run_app():
    """
    Wraps code in the main function
    :return: None
    """
    # Creates Search button click
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
                tree.insert('', tk.END, values=(row["date_sent"], row["subject"], row["message"], row["first_name"], row["num_subscribers"]))


    # Creates main window
    root = tk.Tk()
    root.title("Notification Logs Search")
    root.geometry("1000x500")
    # Use Team chosen color
    root.configure(background='#f7f9fb')
    # Sets fonts
    default_font = font.Font(family='Helvetica', size=16, weight='bold')
    button_font = font.Font(family='Helvetica', size=16, weight='bold')

    # Adds style to GUI
    root.option_add("*Font", default_font)
    root.option_add("*Background", "#f7f9fb")
    root.option_add("*Foreground", "#1690b4")

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview.Heading",
                    background="#f7f9fb",
                    foreground="#1690b4",
                    font=default_font)

    style.configure("Treeview",
                    background="#ffffff",
                    fieldbackground="#ffffff",
                    foreground="#1690b4",
                    rowheight=30,
                    font=default_font)

    style.configure("Label",
                    background="#f7f9fb",
                    foreground="#1690b4",
                    font=default_font)

    style.configure("Button",
                    background="#007b8a",
                    foreground="#ffffff",
                    font=button_font,
                    padding=6)

    style.map("Button",
              background=[("active", "#005f6a"), ("pressed", "#005f6a")],
              foreground=[("active", "#ffffff"), ("pressed", "#ffffff")]
              )

    style.configure("Combobox",
                    fieldbackground="#ffffff",
                    background="#ffffff",
                    foreground="#1690b4",
                    font=default_font
                    )


    # Top frame
    top_frame = ttk.Frame(root)
    top_frame.pack(pady=20)

    # Creates box for "start" date
    ttk.Label(top_frame, text="Start: ").grid(row=0, column=0, padx=5)
    start_date_box = DateEntry(top_frame, width=12, background='#1690b4', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    start_date_box.grid(row=0, column=1, padx=5)

    # Creates box for "end" date
    ttk.Label(top_frame, text="End: ").grid(row=0, column=2, padx=5)
    end_date_box = DateEntry(top_frame, width=12, background='#1690b4', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
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

    details_frame = tk.Frame(root)
    details_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    details_text = tk.StringVar()
    ttk.Label(details_frame, text="Log Details: ").pack(anchor=tk.W, pady=5)
    ttk.Label(details_frame, textvariable=details_text, justify=tk.LEFT, anchor=tk.W).pack(fill=tk.BOTH, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_app()
    