import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

root = tk.Tk()
root.title("Date Picker Example")


def get_selected_date():
    selected_date = cal.get_date()
    print("Selected Date:", selected_date)


cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack(padx=10, pady=10)

select_button = ttk.Button(root, text="Select Date", command=get_selected_date)
select_button.pack(pady=5)

root.mainloop()
