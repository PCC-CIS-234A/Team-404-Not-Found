# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-26
# Description:
# This module is the initial user interface for notification system.
# The user may choose to log in or sign up.
# Combines code from notification_home.py, signup.py, and login.py into a single tkinter app using Frames.

# Code Reference:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# *****************************************************

# Issues with the current code:

# Entries do not clear when switching back and forth between login and signup.
# The window title does not change to reflect the current frame.
# All the frame classes are in the same file as the app class.
# Buttons do not connect to code in the logic layer.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.theme import *


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
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("Panther Pantry Notification System")
        self.geometry("500x500")
        self.minsize(width=400, height=465)

        apply_theme_styles(self)

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
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        shadow_offset = 2
        shadow_label = tk.Label(self, text="PANTHER PANTRY", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.1, anchor="n", x=shadow_offset, y=shadow_offset)
        title_label = tk.Label(self, text="PANTHER PANTRY", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        shadow_offset = 2
        shadow_label2 = tk.Label(self, text="NOTIFICATION SYSTEM", font=label_font, bg=BUTTON_HOVER, fg="#333333",
                                 padx=11, pady=6)
        shadow_label2.place(relx=0.5, rely=0.2, anchor="n", x=shadow_offset, y=shadow_offset)
        title_label2 = tk.Label(self, text="NOTIFICATION SYSTEM", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                padx=10, pady=5)
        title_label2.place(relx=0.5, rely=0.2, anchor="n")

        button_frame = ttk.Frame(self, style="Form.TFrame")
        button_frame.place(relx=0.5, rely=0.5, anchor="n")
        login_button = tk.Button(button_frame, text="Login", font=button_font, width=7, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                 activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                 relief="flat", command=lambda: controller.show_frame(LoginPage))
        signup_button = tk.Button(button_frame, text="Sign Up", font=button_font, width=7, bg=BUTTON_COLOR,
                                  fg=BUTTON_TEXT, activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                  relief="flat", command=lambda: controller.show_frame(SignupPage))
        login_button.grid(column=0, row=0, padx=10, pady=10)
        signup_button.grid(column=1, row=0, padx=10, pady=10)


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
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        shadow_offset = 2
        shadow_label = tk.Label(self, text="USER LOGIN", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(self, text="USER LOGIN", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        input_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        input_frame.place(relx=0.5, rely=0.2, anchor="n")

        user_label = ttk.Label(input_frame, text="Email or Username", font=label_font)
        user_label.grid(column=0, row=0, pady=3, sticky="e")
        password_label = ttk.Label(input_frame, text="Password", font=label_font)
        password_label.grid(column=0, row=1, pady=3, sticky="e")

        user_entry = ttk.Entry(input_frame)
        user_entry.grid(column=1, row=0, padx=5, pady=3)
        password_entry = ttk.Entry(input_frame, show="*")
        password_entry.grid(column=1, row=1, padx=5, pady=3)

        button_frame = ttk.Frame(self, style="Form.TFrame")
        button_frame.place(relx=0.5, rely=0.45, anchor="n")
        # To do: Add command to connect to a function to check user_entry and password_entry against the database.
        login_button = tk.Button(button_frame, text="Login", font=button_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                 activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT, relief="flat", width=7)
        login_button.grid(column=0, row=0, padx=10, pady=15)
        signup_label = ttk.Label(button_frame, text="New User?")
        signup_label.grid(column=0, row=1)
        signup_button = tk.Button(button_frame, text="Sign Up", font=button_font, bg=BUTTON_COLOR,
                                  fg=BUTTON_TEXT, activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                  relief="flat", width=7, command=lambda: controller.show_frame(SignupPage))
        signup_button.grid(column=0, row=2, padx=10)


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
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        shadow_offset = 2
        shadow_label = tk.Label(self, text="USER SIGN UP", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(self, text="USER SIGN UP", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        input_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        input_frame.place(relx=0.5, rely=0.15, anchor="n")

        first_name_label = ttk.Label(input_frame, text="First Name", font=label_font)
        first_name_label.grid(column=0, row=0, pady=3, sticky="e")
        last_name_label = ttk.Label(input_frame, text="Last Name", font=label_font)
        last_name_label.grid(column=0, row=1, pady=3, sticky="e")
        email_label = ttk.Label(input_frame, text="Email", font=label_font)
        email_label.grid(column=0, row=2, pady=3, sticky="e")
        username_label = ttk.Label(input_frame, text="Username", font=label_font)
        username_label.grid(column=0, row=3, pady=3, sticky="e")
        password_label = ttk.Label(input_frame, text="Password", font=label_font)
        password_label.grid(column=0, row=4, pady=3, sticky="e")
        re_password_label = ttk.Label(input_frame, text="Re-enter Password", font=label_font)
        re_password_label.grid(column=0, row=5, pady=3, sticky="e")

        first_name_entry = ttk.Entry(input_frame)
        first_name_entry.grid(column=1, row=0, padx=5, pady=3)
        last_name_entry = ttk.Entry(input_frame)
        last_name_entry.grid(column=1, row=1, padx=5, pady=3)
        email_entry = ttk.Entry(input_frame)
        email_entry.grid(column=1, row=2, padx=5, pady=3)
        username_entry = ttk.Entry(input_frame)
        username_entry.grid(column=1, row=3, padx=5, pady=3)
        password_entry = ttk.Entry(input_frame, show="*")
        password_entry.grid(column=1, row=4, padx=5, pady=3)
        re_password_entry = ttk.Entry(input_frame, show="*")
        re_password_entry.grid(column=1, row=5, padx=5, pady=3)

        button_frame = ttk.Frame(self, style="Form.TFrame")
        button_frame.place(relx=0.5, rely=0.65, anchor="n")
        # To do: Add a command to connect to a function to check the signup entries against the database and create a
        # new user with the entries.
        signup_button = tk.Button(button_frame, text="Sign Up", font=button_font, width=7, bg=BUTTON_COLOR,
                                  fg=BUTTON_TEXT, activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                  relief="flat")
        login_button = tk.Button(button_frame, text="Login", font=button_font, width=6, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                 activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT, relief="flat",
                                 command=lambda: controller.show_frame(LoginPage))
        signup_button.grid(column=0, row=0, padx=10, pady=15)
        login_button.grid(column=0, row=2, padx=10)

        login_label = ttk.Label(button_frame, text="Already a User?")
        login_label.grid(column=0, row=1)


app = NotificationApp()
app.mainloop()
