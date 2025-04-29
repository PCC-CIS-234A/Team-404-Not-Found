# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-22
# Last Modified: 2025-4-28
# Description:
# This module is the interface for a new user to sign up in the system.
# The user enters first name, last name, email, username, and password to sign up.
# The user may also choose to log in if they already have user credentials.

# Code Reference:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# *****************************************************
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from theme import *
from logic.user import User


class SignupPage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the user sign up page of the notification system.
    The page accepts user inputs for account creation.  It also has a button that takes the user to a page to log in
    instead of signing up.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        from login import LoginPage

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

        # To do: Add a command to connect to a function to check the signup entries against the database and create a
        # new user with the entries.
        # Add error handling.

        signup_button = tk.Button(self, text="Sign Up", font=button_font, width=7, bg=BUTTON_COLOR,
                                  fg=BUTTON_TEXT, activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                  relief="flat", command=lambda: self.create_user())
        signup_button.place(relx=0.5, rely=0.7, anchor="n")

        login_frame = ttk.Frame(self, style="Form.TFrame")
        login_frame.place(relx=0.5, rely=0.8, anchor="n")
        login_label = ttk.Label(login_frame, text="Already a User?")
        login_label.grid(column=0, row=0)
        login_button = tk.Button(login_frame, text="Login", font=(button_font, 11, "underline", "bold"),
                                 bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat", activebackground=BUTTON_HOVER,
                                 activeforeground=BUTTON_TEXT, command=lambda: controller.show_frame(LoginPage))
        login_button.grid(column=1, row=0)

        self.first_name_entry = first_name_entry
        self.last_name_entry = last_name_entry
        self.email_entry = email_entry
        self.username_entry = username_entry
        self.password_entry = password_entry

        # Create a new user from the GUI inputs.
        # Needs input validation added.
        # Needs password hashing added.

    def create_user(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password_hash = self.password_entry.get().strip()
        role = 'Subscriber'

        User.add_to_database(first_name, last_name, email, username, password_hash, role)
        # self.clear_entries()
        messagebox.showinfo(title="Success", message="Sign Up Successful!")

    # @staticmethod
    # def clear_entries():
    #     for ttk.Entry in SignupPage
    #         entry.delete(0, 'end')

