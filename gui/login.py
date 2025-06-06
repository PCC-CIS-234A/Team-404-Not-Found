"""
Author: R-Nixon
Creation Date: 2025-4-22
Last Modified: 2025-5-13
Description:
This module is the interface for a current user to log in to the system.
The user enters email or username, and password to log in.
The user may also choose to sign up if they do not already have user credentials.

Code References:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
https://stackoverflow.com/questions/9559549/how-to-compare-plain-text-password-to-hashed-password-using-bcrypt
"""
import bcrypt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from theme import *
from data.db_manager import Database
# from logic.user import User

# Problems with the code:
# The GUI layer should not connect directly with the database?


class LoginPage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the login page of the pantry system.
    The page accepts user inputs for email or username, and password.
    It also has a button that takes the user to a page to sign up instead of logging in.
    Successful login will take the user to a welcome page.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        from signup import SignupPage
        from welcome import WelcomePage

        # GUI theme.
        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # Styling for the frame title.
        shadow_offset = 2
        shadow_label = tk.Label(self, text="USER LOGIN", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(self, text="USER LOGIN", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        # Frame for input labels and entries.
        input_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        input_frame.place(relx=0.5, rely=0.2, anchor="n")

        # Labels for user inputs.
        user_label = ttk.Label(input_frame, text="Email or Username", font=label_font)
        user_label.grid(column=0, row=0, pady=3, sticky="e")
        password_label = ttk.Label(input_frame, text="Password", font=label_font)
        password_label.grid(column=0, row=1, pady=3, sticky="e")

        # Entries for user inputs.
        login_user_entry = ttk.Entry(input_frame)
        login_user_entry.grid(column=1, row=0, padx=5, pady=3)
        login_password_entry = ttk.Entry(input_frame, show="*")
        login_password_entry.grid(column=1, row=1, padx=5, pady=3)

        # Primary function button.
        login_button = tk.Button(self, text="Login", font=button_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                 activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT, relief="flat", width=7,
                                 command=lambda: confirm_login())
        login_button.place(relx=0.5, rely=0.45, anchor="n")

        # Frame to hold the signup option.
        signup_frame = ttk.Frame(self, style="Form.TFrame")
        signup_frame.place(relx=0.5, rely=0.55, anchor="n")
        signup_label = ttk.Label(signup_frame, text="New User?")
        signup_label.grid(column=0, row=0)
        signup_button = tk.Button(signup_frame, text="Sign Up", font=(button_font, 11, "underline", "bold"),
                                  bg=APP_BACKGROUND, fg=BUTTON_COLOR, activebackground=BUTTON_HOVER,
                                  activeforeground=BUTTON_TEXT, relief="flat",
                                  command=lambda: [clear_form(), controller.show_frame(SignupPage)])
        signup_button.grid(column=1, row=0)

        # Initialize the entries.
        self.login_user_entry = login_user_entry
        self.login_password_entry = login_password_entry

        def confirm_login():
            """
            Function: confirm_login
            Author: R-Nixon
            Date Created: 2025-4-26

            Purpose: Primary attempt at a function to confirm login credentials.
            Confirm the user credentials from the GUI inputs.
            Username or email are checked against existing entries in the database.
            Clears the form and switches to the WelcomePage upon successful login.

            :return: None
            """
            login_user = self.login_user_entry.get().strip()
            login_password = self.login_password_entry.get().strip()
            user = Database.read_user(login_user, login_user)

            if login_user == "" or login_password == "":
                messagebox.showerror("Error", "All fields are required")
            elif user is None:
                messagebox.showerror("Login Failed", "The login attempt failed.  Please check your account "
                                                     "information and try again")
            elif user is not None:
                stored_hash = Database.check_hash(login_user)
                result = bcrypt.checkpw(login_password.encode(), stored_hash.encode())
                if result is False:
                    messagebox.showerror("Login Failed", "The login attempt failed.  Please check your "
                                                         "account information and try again")
                else:
                    clear_form()
                    controller.show_frame(WelcomePage)

        def clear_form():
            """
            Function: clear_form
            Author: R-Nixon
            Date Created: 2025-5-2

            Purpose: Clear all entry fields

            :return: None
            """
            login_user_entry.delete(0, tk.END)
            login_password_entry.delete(0, tk.END)
