# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-4-16
# Last Modified: 2025-4-26
# Description:
# This module is the tkinter app that holds Frames for different interface pages.
# Uses code from home_page.py, signup.py, and login.py as the current frames.

# Code Reference:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# *****************************************************

# Issues with the current code:

# Entries do not clear when switching back and forth between login and signup.
# The window title does not change to reflect the current frame.
# Buttons do not connect to code in the logic layer.

import tkinter as tk
from gui.theme import *
from home_page import HomePage
from signup import SignupPage
from login import LoginPage


class NotificationApp(tk.Tk):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is the tkinter app that contains the frames and widgets for the user login page,
    user sign up page, and employee login page (forthcoming).
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("Panther Pantry Notification System")
        self.geometry("500x500")
        self.minsize(width=400, height=465)

        apply_theme_styles(self)

        # Initialize frames to an empty array.
        self.frames = {}

        # Iterate through a tuple containing the different page layouts.
        # Initialize a frame for each object in the loop.
        # In a future sprint, add landing pages to the tuple: SubscriberPage, StaffPage, ManagerPage
        for F in (HomePage, LoginPage, SignupPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    # Display the current frame passed as a parameter.
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = NotificationApp()
app.mainloop()
