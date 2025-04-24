# For a new user to sign up to the system

import tkinter as tk
from tkinter import ttk


class SubscriberSignupApp:
    def __init__(self, parent):
        top_level = ttk.Frame(parent, padding=10)
        top_level.grid(column=0, row=0, sticky="nsew")

        header_label = ttk.Label(top_level, text="Subscriber Sign Up",
                                 font=("Helvetica", 16, "bold"), foreground="#235578")
        header_label.grid(column=0, row=0)

        input_frame = ttk.Frame(top_level, padding=10)
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
        password_entry = ttk.Entry(input_frame)
        password_entry.grid(column=1, row=4, padx=5, pady=3)
        re_password_entry = ttk.Entry(input_frame)
        re_password_entry.grid(column=1, row=5, padx=5, pady=3)

        button_frame = ttk.Frame(top_level)
        button_frame.grid(column=0, row=2)
        signup_button = tk.Button(button_frame, text="Sign Up", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                  width=7)
        login_button = tk.Button(button_frame, text="Login", bg="#235578", fg="#fff", width=6)
        signup_button.grid(column=0, row=0, padx=10, pady=15)
        login_button.grid(column=0, row=2, padx=10)

        login_label = ttk.Label(button_frame, text="Already a Subscriber?")
        login_label.grid(column=0, row=1)

        self.mainwindow = top_level

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Panther Pantry Notification - Sign Up")
    app = SubscriberSignupApp(root)
    app.run()
