"""
Author: R-Nixon
Creation Date: 2025-4-22
Last Modified: 2025-6-3
Description:
This module is the interface for a new user to sign up in the system.
The user enters first name, last name, email, username, and password to sign up.
The user must enter a confirmation code in a popup window before signup is complete.
The user may also choose to switch to the login page if they already have user credentials.

Code Reference:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from theme import *
from logic.user import User
from logic.input_validation import validate_email, validate_password
from data.db_manager import Database

import configparser
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logic.notification_logic import process_tags
from logic.otp import generate_otp_code, verify_otp_code


config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../gui/config.ini')
config.read(config_path)

SENDER_EMAIL = config.get('EMAIL', 'sender_email')
APP_PASSWORD = config.get('EMAIL', 'app_password')


# Problems with the code:

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
            Username is checked against existing entries in the database.
            Password entries are verified against minimum criteria
            and checked for re-entry matching.
            Calls functions to create a totp code, send a confirmation email, and
            for confirming user email.

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
                messagebox.showerror("Account Creation Failed", "The username already exists.  Please choose"
                                                                "another username and try again.")
            else:
                # Function returns a tuple
                otp = generate_otp_code()
                # Retrieve specific values from the tuple
                totp = otp[0]
                otp_code = otp[1]
                send_confirmation_email(otp_code)
                confirm_email(totp)

        def send_confirmation_email(otp_code, tag_values={}):
            """
             Function: signup_user
             Author: R-Nixon
             Date Created: 2025-5-27

             Purpose: Send a confirmation email to a new user attempting to sign up.
             Email is personalized to include the first name entry from the signup form.

             Code and logic from Sayan's files notification_logic.py and send_notification.py

             :param otp_code: string,
             :param tag_values: dictionary, values of template tags
             :return: None
             """
            sender_email = SENDER_EMAIL
            app_password = APP_PASSWORD

            subject, message = Database.fetch_template_subject_message("Email Confirmation")

            try:
                # Connect to Gmail SMTP securely
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(sender_email, app_password)

                first_name = self.first_name_entry.get().strip()
                recipient_email = self.email_entry.get().strip()

                # Personalize subject and message using tags
                personalized_subject = process_tags(subject, tag_values)
                personalized_subject = personalized_subject.replace(
                    "{{first_name}}", first_name).replace("{{date}}", datetime.datetime.now().strftime('%Y-%m-%d'))

                personalized_message = process_tags(message, tag_values)
                personalized_message = (personalized_message
                                        .replace("{{first_name}}", first_name)
                                        .replace("{{date}}", datetime.datetime.now().strftime('%Y-%m-%d'))
                                        .replace("{{time}}", datetime.datetime.now().strftime('%H:%M:%S'))
                                        .replace("{{otp_code}}", otp_code))

                # Setup email content
                email_msg = MIMEMultipart()
                email_msg['From'] = sender_email
                email_msg['To'] = recipient_email
                email_msg['Subject'] = personalized_subject
                email_msg.attach(MIMEText(personalized_message, 'html'))

                # Print statements for debugging
                print("Sending to:", recipient_email)
                print("Message preview:\n", personalized_message)

                server.send_message(email_msg)

                server.quit()

            except Exception as e:
                raise Exception(f"Email Sending Error: {e}")

        def confirm_email(totp):
            """
             Function: confirm_email
             Author: R-Nixon
             Date Created: 2025-6-1

             Purpose: Confirm a new user's email address.
             User is prompted to enter the totp code from their email.
             User is given 3 tries to provide the correct code.
             Checks if email exists in the database.
             If all validations are passed, calls function to create a new user.

             :param totp: TOTP object
             :return: None
             """
            counter = 3
            email = self.email_entry.get().strip()
            for i in range(counter):
                user_code = simpledialog.askstring(
                    "Enter Code", "Please enter the confirmation code\nfrom your email:")
                if verify_otp_code(totp, user_code):
                    # Check if email is already in the database
                    if Database.check_email(email) is not None:
                        messagebox.showerror("Account Creation Failed", "An account already exists for this email.  "
                                                                        "Please login to your existing account or check"
                                                                        " your information and try again.")
                        clear_form()
                        counter += counter
                        break
                    else:
                        create_user()
                        break
                else:
                    messagebox.showerror("Confirmation Error", "Incorrect confirmation code.  Please try again.")
                    i += 1
                    if i == counter:
                        messagebox.showerror("Confirmation Error", "Incorrect code limit exceeded.")
                        clear_form()

        def create_user():
            """
            Function: create_user
            Author: R-Nixon
            Date Created: 2025-4-26

            Purpose: Create a new user from the GUI inputs.
            Adds a new user to the database.
            Clears the form and switches to the SubscriberWelcome upon successful signup.

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
