# ***************************************************************
"""
Author(s): jasag
Creation Date: 2025-04-16
Last Modified: 2025-04-22

Description:
This file produces the GUI for the employee login form.
"""
# ***************************************************************
# GUI builder
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Test password to test GUI
valid_username = "test"
valid_password = "password"

# Function to log user into Notification Logs Search
def login():
    username = enter_username.get()
    password = enter_password.get()
    if username == valid_username and password == valid_password:
        messagebox.showinfo("Login Successful", "Welcome " + username + "!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password!")

# Creates main window
root = tk.Tk()
root.title("Notification Logs Employee Portal")
root.geometry("400x300")

# Use Team chosen color
root.configure(background='#008099')
text_color = "1690b4"

# Center frame
center_frame = ttk.Frame(root)
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Creates username entry box
ttk.Label(center_frame, text="Email/Username: ").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
enter_username = ttk.Entry(center_frame, width=30)
enter_username.grid(row=0, column=1, padx=10, pady=10)

# Creates password entry box
ttk.Label(center_frame, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
enter_password = ttk.Entry(center_frame, width=30, show="*")
enter_password.grid(row=1, column=1, padx=10, pady=10)

# Creates login button
ttk.Button(center_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
