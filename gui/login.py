# For an existing user to log in to the system

import tkinter as tk
from tkinter import ttk


class SubscriberLoginApp:
    def __init__(self, parent):
        # self.title("Subscriber Login")

        top_level = ttk.Frame(parent, padding=10)
        top_level.grid(column=0, row=0, sticky="nsew")

        header_label = ttk.Label(top_level, text="Subscriber Login",
                                 font=("Helvetica", 16, "bold"), foreground="#235578")
        header_label.grid(column=0, row=0)

        input_frame = ttk.Frame(top_level, padding=10)
        input_frame.grid(column=0, row=1)

        user_label = ttk.Label(input_frame, text="Email or Username")
        user_label.grid(column=0, row=0, pady=3, sticky="e")
        password_label = ttk.Label(input_frame, text="Password")
        password_label.grid(column=0, row=1, pady=3, sticky="e")

        user_entry = ttk.Entry(input_frame)
        user_entry.grid(column=1, row=0, padx=5, pady=3)
        password_entry = ttk.Entry(input_frame, show="*")
        password_entry.grid(column=1, row=1, padx=5, pady=3)

        button_frame = ttk.Frame(top_level)
        button_frame.grid(column=0, row=2)
        login_button = tk.Button(button_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff", width=7)
        login_button.grid(column=0, row=0, padx=10, pady=15)

        footer_frame = ttk.Frame(top_level)
        footer_frame.grid(column=0, row=3, pady=10)
        signup_label = ttk.Label(footer_frame, text="New Subscriber?")
        signup_label.grid(column=0, row=1)
        signup_button = tk.Button(footer_frame, text="Sign Up", bg="#235578", fg="#fff", width=7)
        signup_button.grid(column=0, row=2, padx=10)


        self.mainwindow = top_level

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Panther Pantry Notification - Login")
    app = SubscriberLoginApp(root)
    app.run()
