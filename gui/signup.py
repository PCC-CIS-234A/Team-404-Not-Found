"""
Author: R-Nixon
Creation Date: 2025-4-22
Last Modified: 2025-5-27
Description:
This module is the interface for a new user to sign up in the system.
The user enters first name, last name, email, username, and password to sign up.
The user may also choose to log in if they already have user credentials.

Code Reference:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from theme import *
from logic.user import User
from logic.input_validation import validate_email, validate_password
from data.db_manager import Database


# Problems with the code:
# The GUI layer should not connect directly with the database?


class SignupPage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the user sign up page of the pantry system.
    The page accepts user inputs for account creation.
    It also has a button that takes the user to a page to log in instead of signing up.
    Successful signup will take the user to a welcome page.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        from login import LoginPage
        from subscriber_welcome import SubscriberWelcome
        from logic.email_confirmation import send_confirmation

        # GUI theme.
        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # Styling for the frame title.
        shadow_offset = 2
        shadow_label = tk.Label(self, text="USER SIGN UP", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(self, text="USER SIGN UP", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        # Frame for input labels and entries.
        input_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        input_frame.place(relx=0.5, rely=0.15, anchor="n")

        # Labels for the user inputs.
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

        # Entries for the user inputs.
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

        # Primary function button.
        signup_button = tk.Button(self, text="Sign Up", font=button_font, width=7, bg=BUTTON_COLOR,
                                  fg=BUTTON_TEXT, activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                  relief="flat", command=lambda: signup_user())
        signup_button.place(relx=0.5, rely=0.7, anchor="n")

        # Frame to hold the login option.
        login_frame = ttk.Frame(self, style="Form.TFrame")
        login_frame.place(relx=0.5, rely=0.8, anchor="n")
        login_label = ttk.Label(login_frame, text="Already a User?")
        login_label.grid(column=0, row=0)
        login_button = tk.Button(login_frame, text="Login", font=(button_font, 11, "underline", "bold"),
                                 bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat", activebackground=BUTTON_HOVER,
                                 activeforeground=BUTTON_TEXT, command=lambda: [clear_form(),
                                                                                controller.show_frame(LoginPage)])

        login_button.grid(column=1, row=0)

        # Initialize the entries.
        self.first_name_entry = first_name_entry
        self.last_name_entry = last_name_entry
        self.email_entry = email_entry
        self.username_entry = username_entry
        self.password_entry = password_entry
        self.re_password_entry = re_password_entry

        def signup_user():
            """
            Function: signup_user
            Author: R-Nixon
            Date Created: 2025-4-26

            Purpose: Validate user's GUI inputs.
            Username and email are checked against existing entries in the database.
            Password entries are verified against minimum criteria
            and checked for re-entry matching.
            Calls the create_user function.

            :return: None
            """
            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            email = self.email_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            re_password = self.re_password_entry.get().strip()

            if (first_name == "" or last_name == "" or email == "" or username == "" or password == "" or
                    re_password == ""):
                messagebox.showerror("Error", "All fields are required")
            elif validate_password(password) is False:
                messagebox.showerror("Error", "Password must be at least 6 characters long and contain a "
                                              "lowercase letter, an uppercase letter, a number, and a special "
                                              "character.")
            elif password != re_password:
                messagebox.showerror("Error", "Passwords must match")
            elif validate_email(email) is False:
                messagebox.showerror("Error", "Invalid Email")
            elif Database.check_username(username) is not None:
                messagebox.showerror("Account Creation Failed", "The account creation failed.  Please check "
                                                                "your account information and try again")
            # Original logic before email confirmation requirement
            # elif Database.check_email(email) is not None:
            #     messagebox.showerror("Account Creation Failed", "The account creation failed.  Please check "
            #                                                     "your account information and try again")
            # else:
            #     create_user()
            else:
                send_confirmation()

        def confirm_email():
            email = self.email_entry.get().strip()
            Database.check_email(email)

        def create_user():
            """
            Function: create_user
            Author: R-Nixon
            Date Created: 2025-4-26

            Purpose: Create a new user from the GUI inputs.
            Adds a new user to the database.
            Clears the form and switches to the WelcomePage upon successful signup.

            :return: None
            """
            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            email = self.email_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            password_hash = User.hash_password(password)
            role = "Subscriber"

            User.add_to_database(first_name, last_name, email, username, password_hash, role)
            clear_form()
            controller.show_frame(SubscriberWelcome)

        def clear_form():
            """
            Function: clear_form
            Author: R-Nixon
            Date Created: 2025-5-2

            Purpose: Clear all entry fields

            :return: None
            """
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            re_password_entry.delete(0, tk.END)
