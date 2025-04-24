# Initial interface for notification system
# Choose to log in, sign up, or switch to employee portal
import tkinter as tk
from tkinter import ttk
from gui.login import SubscriberLoginApp
from gui.signup import SubscriberSignupApp


class NotificationHomeApp:
    def __init__(self, parent):
        top_level = ttk.Frame(parent, padding="10")
        top_level.grid(column=0, row=0)

        header_label1 = ttk.Label(top_level, text="Welcome to the Panther Pantry", font=("Helvetica", 16, "bold"),
                                  foreground="#235578")
        header_label1.grid(column=0, row=0, padx=20, pady=5)
        header_label2 = ttk.Label(top_level, text="Notification Service!", font=("Helvetica", 16, "bold"),
                                  foreground="#235578")
        header_label2.grid(column=0, row=1)

        button_frame = ttk.Frame(top_level)
        button_frame.grid(column=0, row=2, pady=15)
        login_button = tk.Button(button_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                 width=7)
        signup_button = tk.Button(button_frame, text="Sign Up", font=("Helvetica", 12, "bold"), bg="#235578", fg="#fff",
                                  width=7)
        login_button.grid(column=0, row=0, padx=10, pady=10)
        signup_button.grid(column=1, row=0, padx=10, pady=10)

        footer_frame = ttk.Frame(top_level)
        footer_frame.grid(column=0, row=3, pady=15)
        # Button connects to home screen for Stories 2, 3, and 4.
        employee_button = tk.Button(footer_frame, text="Employee Login", font=("Helvetica", 10))
        employee_button.grid(column=0, row=2)

        self.mainwindow = top_level

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Panther Pantry Notifications")
    # root.geometry("350x200")
    app = NotificationHomeApp(root)
    app.run()
