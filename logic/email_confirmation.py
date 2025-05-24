"""
uthor: R-Nixon
Creation Date: 2025-5-23
Last Modified: 2025-5-23
Description:
This module is a stub to test the functionality of
one-time-password generation using pytop and email confirmation.
Code will eventually be integrated into signup.py
and possibly notification_logic.py for email sending.

Code Reference:
https://www.codespeedy.com/popup-window-with-input-entry-in-tkinter/
"""


import tkinter as tk
import pyotp


def generate_code():
    secret_key = pyotp.random_base32()
    hotp = pyotp.HOTP(secret_key)
    otp_code = hotp.at(0)
    print(otp_code)
    return otp_code


def show_entry_in_main():
    # Updating the label in the main window with the entry from the popup
    confirmation_label = tk.Label(text="opt_code")
    confirmation_label.pack()
    entry_text.set(entry.get())
    popup.destroy()  # This will close the popup window


def open_popup():
    global popup, entry
    popup = tk.Toplevel(root)  # Creating a popup window which will be on top of the main window
    popup.title("Email Confirmation")
    popup.geometry("300x150")
    entry_label = tk.Label(popup, text="Enter your confirmation code:")
    entry_label.pack(pady=(10, 10))
    # Input widget in the popup window
    entry = tk.Entry(popup)
    entry.pack(pady=(20, 10))
    # Submit button that will call the show entry function which will set the text to the variable
    btn_ok = tk.Button(popup, text="Submit", command=show_entry_in_main)
    btn_ok.pack()


# Creating the main window
root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")
otp_code = generate_code()
# Button in the main window to open the popup window
btn_open_popup = tk.Button(root, text="Sign Up", command=open_popup)
btn_open_popup.pack(pady=20)
# Variable to store the input text
entry_text = tk.StringVar()
# Label to display the entry from the popup window
label = tk.Label(root, textvariable=entry_text)
label.pack(pady=(50, 10))
root.mainloop()


def send_confirmation_email():
    pass
