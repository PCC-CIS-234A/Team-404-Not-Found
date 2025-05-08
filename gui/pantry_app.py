"""
Author: R-Nixon
Creation Date: 2025-4-22
Last Modified: 2025-5-3
Description:
This module is the tkinter app that holds Frames for different interface pages.
Uses code from home_page.py, signup.py, login.py, and welcome.py as the current frames.

Code Reference:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""

# Problems with the code:
# The window title does not change to reflect the current frame.

import tkinter as tk
from gui.theme import *
from home_page import HomePage
from signup import SignupPage
from login import LoginPage
from welcome import WelcomePage


class PantryApp(tk.Tk):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter app that contains the frames for the user home page, login page, and sign up page.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("Panther Pantry")
        self.geometry("500x500")
        self.minsize(width=400, height=465)

        apply_theme_styles(self)

        # Initialize frames to an empty array.
        self.frames = {}

        # Possible to iterate through the frames to change the window title?
        # for t in (HomePage, LoginPage, SignupPage, WelcomePage):
        # change the title for each object in the loop?

        # Iterate through a tuple containing the different page layouts.
        # Initialize a frame for each object in the loop.
        # In a future sprint, add landing pages to the tuple: SubscriberPage, StaffPage, ManagerPage
        for F in (HomePage, LoginPage, SignupPage, WelcomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        """
        Function: show_frame
        Author: R-Nixon
        Date Created: 2025-4-22

        Purpose: Display the current tkinter frame passed as a parameter.

        :param cont: container that holds the tkinter frame
        :return: None
        """
        frame = self.frames[cont]
        frame.tkraise()


app = PantryApp()
app.mainloop()
