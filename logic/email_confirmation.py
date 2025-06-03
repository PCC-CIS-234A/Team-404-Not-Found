"""
Author: R-Nixon
Creation Date: 2025-5-23
Last Modified: 2025-5-27
Description:
This module is currently a stub to test the functionality of
one-time-password generation using pytop and email confirmation.
Code will eventually be integrated into signup.py
and possibly notification_logic.py for email sending.

Borrowed code and logic from Sayan's  files
notification_logic.py and send_notification.py

Code Reference:
https://www.codespeedy.com/popup-window-with-input-entry-in-tkinter/
https://github.com/walid11111/Multi-Factor-Auth-System
"""


import tkinter as tk
import pyotp
import configparser
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logic.notification_logic import process_tags
from data.db_manager import Database


config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../gui/config.ini')
config.read(config_path)

SENDER_EMAIL = config.get('EMAIL', 'sender_email')
APP_PASSWORD = config.get('EMAIL', 'app_password')


# Duplicated in signup.py without the hardcoded values
def send_confirmation_email(tag_values={}):
    sender_email = SENDER_EMAIL
    app_password = APP_PASSWORD

    subject, message = Database.fetch_template_subject_message("Email Confirmation")

    sender_username = "Sarah Sam"  # Manager username from your DB

    # Recipient hardcoded for testing
    recipient = "Rebecca"
    sender_id = Database.get_sender_id(sender_username)
    attachments = "NULL"
    Database.log_notification(subject, message, 1, sender_id, attachments)

    try:
        # Connect to Gmail SMTP securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)

        # Hardcoded to test logic
        first_name = recipient
        recipient_email = "rebecca.nixon1@pcc.edu"
        otp_code = generate_code()

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

        print("Sending to:", recipient_email)
        print("Message preview:\n", personalized_message)

        server.send_message(email_msg)

        server.quit()

    except Exception as e:
        raise Exception(f"Email Sending Error: {e}")


def generate_key():
    secret_key = pyotp.random_base32()
    print("secret key:", secret_key)
    return secret_key


def generate_totp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp


def generate_code(totp):
    otp_code = totp.now()
    print("otp code:", otp_code)
    print("totp: ", totp)
    return otp_code


def verify_code(totp, code_entry):
    print(totp.verify(code_entry))
#
#
# def show_entry_in_main():
#     # Updating the label in the main window with the entry from the popup
#     confirmation_label = tk.Label(text="opt_code")
#     confirmation_label.pack()
#     entry_text.set(entry.get())
#     popup.destroy()  # This will close the popup window

#
# def open_popup():
#     global popup, entry
#     popup = tk.Toplevel(root)  # Creating a popup window which will be on top of the main window
#     popup.title("Email Confirmation")
#     popup.geometry("300x150")
#     entry_label = tk.Label(popup, text="Enter your confirmation code:")
#     entry_label.pack(pady=(10, 10))
#     # Input widget in the popup window
#     entry = tk.Entry(popup)
#     entry.pack(pady=(20, 10))
#     # Submit button that will call the show entry function which will set the text to the variable
#     btn_ok = tk.Button(popup, text="Submit", command=[verify_code(), popup.destroy()])
#     btn_ok.pack()
#
#
# # Creating the main window
# root = tk.Tk()
# root.title("Main Window")
# root.geometry("400x300")
# otp_code = generate_code()
# # Button in the main window to open the popup window
# btn_open_popup = tk.Button(root, text="Sign Up", command=open_popup)
# btn_open_popup.pack(pady=20)
# # Variable to store the input text
# entry_text = tk.StringVar()
# # Label to display the entry from the popup window
# label = tk.Label(root, textvariable=entry_text)
# label.pack(pady=(50, 10))
# root.mainloop()
