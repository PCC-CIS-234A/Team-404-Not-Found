"""
Author: R-Nixon/ Modified by Sayan
Creation Date: 2025-5-23
Last Modified: 06/06/2025

Description:
This module is the welcome page after a manager signs into the system.
It contains links to manager features (send notification, create template, view notification logs)
and includes a logout button.

References:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""
import tkinter as tk
from tkinter import ttk
from theme import *

from home_page import HomePage
from send_notification import SendNotificationPage
from template_creator_gui import TemplatePage
from notification_logs import LogsPage


class ManagerWelcome(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-05-23
    Purpose: Welcome page for managers after successful login.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # Frame title with shadow effect
        shadow_offset = 2
        shadow_label = tk.Label(
            self, text="WELCOME!", font=label_font, bg=BUTTON_HOVER,
            fg="#333333", padx=11, pady=6
        )
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(
            self, text="WELCOME!", font=label_font,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10, pady=5
        )
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        # Welcome text frame
        welcome_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        welcome_frame.place(relx=0.5, rely=0.2, anchor="n")

        ttk.Label(welcome_frame, text="Welcome to the", font=label_font).grid(row=0, column=0)
        ttk.Label(welcome_frame, text="PCC Free Food Pantry!", font=label_font).grid(row=1, column=0)

        # Navigation buttons
        options_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        options_frame.place(relx=0.5, rely=0.4, anchor="n")

        send_notification_button = tk.Button(
            options_frame, text="Send Notification", font=(button_font, 12, "underline", "bold"),
            bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat",
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            command=lambda: controller.show_frame(SendNotificationPage)
        )
        send_notification_button.grid(row=0, column=0, padx=5)

        create_template_button = tk.Button(
            options_frame, text="Create Template", font=(button_font, 12, "underline", "bold"),
            bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat",
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            command=lambda: controller.show_frame(TemplatePage)
        )
        create_template_button.grid(row=0, column=1, padx=5)

        notification_logs_button = tk.Button(
            options_frame, text="Notification Logs", font=(button_font, 12, "underline", "bold"),
            bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat",
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            command=lambda: controller.show_frame(LogsPage)
        )
        notification_logs_button.grid(row=0, column=2, padx=5)

        # Logout button
        logout_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        logout_frame.place(relx=0.5, rely=0.6, anchor="n")

        logout_button = tk.Button(
            logout_frame, text="Logout", font=(button_font, 12, "underline", "bold"),
            bg=APP_BACKGROUND, fg=BUTTON_COLOR, relief="flat",
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            command=lambda: controller.show_frame(HomePage)
        )
        logout_button.grid(row=0, column=0)
