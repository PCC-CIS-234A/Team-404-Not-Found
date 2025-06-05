"""
Author: R-Nixon
Creation Date: 2025-4-22
Last Modified: 2025-6-04
Description:
This module is the tkinter application that manages multiple interface pages.
It dynamically changes the window title based on the currently active frame.

References:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""

import tkinter as tk
from gui.theme import apply_theme_styles

# Import all GUI page classes
from home_page import HomePage
from signup import SignupPage
from login import LoginPage
from subscriber_welcome import SubscriberWelcome
from staff_welcome import StaffWelcome
from manager_welcome import ManagerWelcome
from notification_logs import LogsPage
from send_notification import SendNotificationPage
from template_creator_gui import TemplatePage


class PantryApp(tk.Tk):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: Tkinter application managing frames for different GUI pages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1920x1080")
        self.minsize(width=720, height=500)

        apply_theme_styles(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store frame instances
        self.frames = {}

        # Define all pages here for easy maintenance
        pages = (
            HomePage, LoginPage, SignupPage,
            SubscriberWelcome, StaffWelcome, ManagerWelcome,
            SendNotificationPage, TemplatePage, LogsPage
        )

        # Initialize each frame and store it
        for Page in pages:
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the default starting page
        self.show_frame(HomePage)

    def show_frame(self, page_class):
        """
        Raise the specified frame to the top and dynamically update the window title.

        :param page_class: class of the frame to be displayed
        """
        frame = self.frames[page_class]
        frame.tkraise()

        # Dictionary mapping frames to their window titles
        page_titles = {
            HomePage: "Home - PCC Free Food Pantry",
            LoginPage: "Login - PCC Free Food Pantry",
            SignupPage: "Signup - PCC Free Food Pantry",
            SubscriberWelcome: "Subscriber Welcome - PCC Free Food Pantry",
            StaffWelcome: "Staff Welcome - PCC Free Food Pantry",
            ManagerWelcome: "Manager Welcome - PCC Free Food Pantry",
            SendNotificationPage: "Send Notification - PCC Free Food Pantry",
            TemplatePage: "Template Manager - PCC Free Food Pantry",
            LogsPage: "Notification Logs - PCC Free Food Pantry"
        }

        # Set window title based on current frame
        self.title(page_titles.get(page_class, "PCC Free Food Pantry"))


if __name__ == "__main__":
    app = PantryApp()
    app.mainloop()
