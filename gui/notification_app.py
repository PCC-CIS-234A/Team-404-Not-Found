# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-23

# Description:
# This module is the initial user interface for notification system.
# The user may choose to log in, sign up, or switch to the employee portal.
# Combines code from notification_home.py, signup.py, and login.py into a single tkinter app using Frames.

# Code Reference:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# *****************************************************

# Issues with the current code:

# Formatting is terrible.
# Color scheme does not match other team members' stories.
# Entries do not clear when switching back and forth between login and signup.
# The window title does not change to reflect the current frame.
# All the frame classes are in the same file as the app class.
# Buttons do not connect to code in the logic layer.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class NotificationApp(tk.Tk):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is the tkinter app that contains the frames and widgets for the user login page,
    user sign up page, and employee login page (forthcoming).
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        # container.grid(column=0, row=0)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("Panther Pantry Notification System")

        # Initialize frames to an empty array.
        self.frames = {}

        # Iterate through a tuple containing the different page layouts.
        # Initialize a frame for each object in the loop.
        for F in (HomePage, LoginPage, SignupPage):  # add EmployeePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    # Display the current frame passed as a parameter.
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the initial screen of the notification system.  The page gives
    options to log in, sign up, or log in as an employee in the form of buttons that change the frame.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header_label1 = ttk.Label(self, text="Welcome to the Panther Pantry", font=("Helvetica", 16, "bold"),
                                  foreground="#235578")
        header_label1.grid(column=0, row=0, padx=20, pady=5)
        header_label2 = ttk.Label(self, text="Notification Service!", font=("Helvetica", 16, "bold"),
                                  foreground="#235578")
        header_label2.grid(column=0, row=1)

        button_frame = ttk.Frame(self)
        button_frame.grid(column=0, row=2, pady=15)
        login_button = tk.Button(button_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                 width=7, command=lambda: controller.show_frame(LoginPage))
        signup_button = tk.Button(button_frame, text="Sign Up", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                  width=7, command=lambda: controller.show_frame(SignupPage))
        login_button.grid(column=0, row=0, padx=10, pady=10)
        signup_button.grid(column=1, row=0, padx=10, pady=10)

        footer_frame = ttk.Frame(self)
        footer_frame.grid(column=0, row=3, pady=15)
        # Button connects to employee login screen for Stories 2, 3, and 4.
        # Add later: command=lambda: controller.show_frame(EmployeePage)
        employee_button = tk.Button(footer_frame, text="Employee Login", font=("Helvetica", 10))
        employee_button.grid(column=0, row=2)


class LoginPage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the subscriber login page of the notification system.
    The page accepts user inputs for email or username and password.  It also has a button that takes the user to a page
    to sign up instead of logging in.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header_label = ttk.Label(self, text="Subscriber Login", font=("Helvetica", 16, "bold"), foreground="#235578")
        header_label.grid(column=0, row=0)

        input_frame = ttk.Frame(self, padding=10)
        input_frame.grid(column=0, row=1)

        user_label = ttk.Label(input_frame, text="Email or Username")
        user_label.grid(column=0, row=0, pady=3, sticky="e")
        password_label = ttk.Label(input_frame, text="Password")
        password_label.grid(column=0, row=1, pady=3, sticky="e")

        user_entry = ttk.Entry(input_frame)
        user_entry.grid(column=1, row=0, padx=5, pady=3)
        password_entry = ttk.Entry(input_frame, show="*")
        password_entry.grid(column=1, row=1, padx=5, pady=3)

        button_frame = ttk.Frame(self)
        button_frame.grid(column=0, row=2)
        # To do: Add command to connect to a function to check user_entry and password_entry against the database.
        login_button = tk.Button(button_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                 width=7)
        login_button.grid(column=0, row=0, padx=10, pady=15)

        footer_frame = ttk.Frame(self)
        footer_frame.grid(column=0, row=3, pady=10)
        signup_label = ttk.Label(footer_frame, text="New Subscriber?")
        signup_label.grid(column=0, row=1)
        signup_button = tk.Button(footer_frame, text="Sign Up", bg="#235578", fg="#fff", width=7,
                                  command=lambda: controller.show_frame(SignupPage))
        signup_button.grid(column=0, row=2, padx=10)
        # Button connects to employee login screen for Stories 2, 3, and 4.
        # Add later: command=lambda: controller.show_frame(EmployeePage)
        employee_button = tk.Button(footer_frame, text="Employee Login", font=("Helvetica", 10))
        employee_button.grid(column=1, row=2)


class SignupPage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the subscriber sign up page of the notification system.
    The page accepts user inputs for account creation.  It also has a button that takes the user to a page to log in
    instead of signing up.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header_label = ttk.Label(self, text="Subscriber Sign Up",
                                 font=("Helvetica", 16, "bold"), foreground="#235578")
        header_label.grid(column=0, row=0)

        input_frame = ttk.Frame(self, padding=10)
        input_frame.grid(column=0, row=1)

        f_name_label = ttk.Label(input_frame, text="First Name")
        f_name_label.grid(column=0, row=0, pady=3, sticky="e")
        l_name_label = ttk.Label(input_frame, text="Last Name")
        l_name_label.grid(column=0, row=1, pady=3, sticky="e")
        email_label = ttk.Label(input_frame, text="Email")
        email_label.grid(column=0, row=2, pady=3, sticky="e")
        username_label = ttk.Label(input_frame, text="Create a Username")
        username_label.grid(column=0, row=3, pady=3, sticky="e")
        password_label = ttk.Label(input_frame, text="Password")
        password_label.grid(column=0, row=4, pady=3, sticky="e")
        re_password_label = ttk.Label(input_frame, text="Re-enter Password")
        re_password_label.grid(column=0, row=5, pady=3, sticky="e")

        f_name_entry = ttk.Entry(input_frame)
        f_name_entry.grid(column=1, row=0, padx=5, pady=3)
        l_name_entry = ttk.Entry(input_frame)
        l_name_entry.grid(column=1, row=1, padx=5, pady=3)
        email_entry = ttk.Entry(input_frame)
        email_entry.grid(column=1, row=2, padx=5, pady=3)
        username_entry = ttk.Entry(input_frame)
        username_entry.grid(column=1, row=3, padx=5, pady=3)
        password_entry = ttk.Entry(input_frame, show="*")
        password_entry.grid(column=1, row=4, padx=5, pady=3)
        re_password_entry = ttk.Entry(input_frame, show="*")
        re_password_entry.grid(column=1, row=5, padx=5, pady=3)

        button_frame = ttk.Frame(self)
        button_frame.grid(column=0, row=2)
        # To do: Add a command to connect to a function to check the signup entries against the database and create a
        # new user with the entries.
        signup_button = tk.Button(button_frame, text="Sign Up", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                  width=7)
        login_button = tk.Button(button_frame, text="Login", bg="#235578", fg="#fff", width=6,
                                 command=lambda: controller.show_frame(LoginPage))
        signup_button.grid(column=0, row=0, padx=10, pady=15)
        login_button.grid(column=0, row=2, padx=10)

        login_label = ttk.Label(button_frame, text="Already a Subscriber?")
        login_label.grid(column=0, row=1)
        # Button connects to employee login screen for Stories 2, 3, and 4.
        # Add later: command=lambda: controller.show_frame(EmployeePage)
        employee_button = tk.Button(button_frame, text="Employee Login", font=("Helvetica", 10))
        employee_button.grid(column=1, row=2)


app = NotificationApp()
app.mainloop()
