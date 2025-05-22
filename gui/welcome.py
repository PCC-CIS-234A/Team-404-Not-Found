"""
Author: R-Nixon
Creation Date: 2025-5-1
Last Modified: 2025-5-11
Description:
This module is the welcome page after a user signs into the system.
This page greets both new users and returning users, and contains a button for the user
to exit to the login/signup home page.

Code Reference:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""
import tkinter as tk
from tkinter import ttk
from theme import *


class WelcomePage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-05-01
    Purpose: This class is a tkinter frame that contains the welcome page for users.
    Users will see this page after a successful login or signup.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        from home_page import HomePage
        # from send_notification import NotificationPage
        # from template_creator import TemplatePage
        # from notification_logs import LogsPage

        # GUI theme.
        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # Styling for the frame title.
        shadow_offset = 2
        shadow_label = tk.Label(self, text="WELCOME!", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(self, text="WELCOME!", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        # Welcome text.
        welcome_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        welcome_frame.place(relx=0.5, rely=0.2, anchor="n")

        welcome_label1 = ttk.Label(welcome_frame, text="Welcome to the", font=label_font)
        welcome_label1.grid(row=0, column=0)
        welcome_label2 = ttk.Label(welcome_frame, text="404 Food Pantry!", font=label_font)
        welcome_label2.grid(row=1, column=0)

        # Navigation options.
        options_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        options_frame.place(relx=0.5, rely=0.3, anchor="n")
        send_notification_button = tk.Button(options_frame, text="Send Notification", font=(button_font, 12, "underline", "bold"),
                                bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat", activebackground=BUTTON_HOVER,
                                activeforeground=BUTTON_TEXT)
        send_notification_button.grid(row=0, column=0)
        create_template_button = tk.Button(options_frame, text="Create Template", font=(button_font, 12, "underline", "bold"),
                                bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat", activebackground=BUTTON_HOVER,
                                activeforeground=BUTTON_TEXT)
        create_template_button.grid(row=0, column=1)
        notification_logs_button = tk.Button(options_frame, text="Notification Logs",
                                           font=(button_font, 12, "underline", "bold"),
                                           bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat",
                                           activebackground=BUTTON_HOVER,
                                           activeforeground=BUTTON_TEXT)
        notification_logs_button.grid(row=0, column=2)

        # Logout button.
        logout_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        logout_frame.place(relx=0.5, rely=0.5, anchor="n")

        logout_button = tk.Button(logout_frame, text="Logout", font=(button_font, 12, "underline", "bold"),
                                bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat", activebackground=BUTTON_HOVER,
                                activeforeground=BUTTON_TEXT, command=lambda: controller.show_frame(HomePage))
        logout_button.grid(row=0, column=0)
