# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-22
# Last Modified: 2025-4-26
# Description:
# This module is the interface for a current user to log in to the system.
# The user enters email or username, and password to log in.
# The user may also choose to sign up if they do not already have user credentials.

# Code Reference:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# *****************************************************
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from theme import *
from logic.user import User


class LoginPage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the login page of the notification system.
    The page accepts user inputs for email or username, and password.  It also has a button that takes the user to a
    page to sign up instead of logging in.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        from signup import SignupPage

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

        login_button = tk.Button(self, text="Login", font=button_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                 activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT, relief="flat", width=7,
                                 command=lambda: confirm_login)
        login_button.place(relx=0.5, rely=0.45, anchor="n")

        signup_frame = ttk.Frame(self, style="Form.TFrame")
        signup_frame.place(relx=0.5, rely=0.55, anchor="n")
        # To do: Add command to connect to a function to check user_entry and password_entry against the database.

        signup_label = ttk.Label(signup_frame, text="New User?")
        signup_label.grid(column=0, row=0)
        signup_button = tk.Button(signup_frame, text="Sign Up", font=(button_font, 11, "underline", "bold"),
                                  bg=APP_BACKGROUND, fg=BUTTON_COLOR, activebackground=BUTTON_HOVER,
                                  activeforeground=BUTTON_TEXT, relief="flat",
                                  command=lambda: controller.show_frame(SignupPage))
        signup_button.grid(column=1, row=0)

        def confirm_login():
            messagebox.showinfo("Welcome to the Notification System!")
            print("Welcome!")
            return
