"""
Author: R-Nixon
Creation Date: 2025-4-22
Last Modified: 2025-5-11
Description:
This module is the initial user interface for pantry system.
The user may choose to log in or sign up.

Code Reference:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""
import tkinter as tk
from tkinter import ttk
from theme import *


class HomePage(tk.Frame):
    """
    Author: R-Nixon
    Creation Date: 2025-04-22
    Purpose: This class is a tkinter frame that contains the initial screen of the pantry system.  The page gives
    options to log in or sign up in the form of buttons that switch between frames.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        from signup import SignupPage
        from login import LoginPage

        # GUI theme.
        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # Styling for the frame title.
        shadow_offset = 2
        shadow_label = tk.Label(self, text="PCC FREE FOOD PANTRY", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.1, anchor="n", x=shadow_offset, y=shadow_offset)
        title_label = tk.Label(self, text="PCC FREE FOOD PANTRY", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.1, anchor="n")

        # Frame to hold the login and signup buttons.
        button_frame = ttk.Frame(self, style="Form.TFrame")
        button_frame.place(relx=0.5, rely=0.5, anchor="n")
        login_button = tk.Button(button_frame, text="Login", font=button_font, width=7, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                                 activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                 relief="flat", command=lambda: controller.show_frame(LoginPage))
        signup_button = tk.Button(button_frame, text="Sign Up", font=button_font, width=7, bg=BUTTON_COLOR,
                                  fg=BUTTON_TEXT, activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
                                  relief="flat", command=lambda: controller.show_frame(SignupPage))
        login_button.grid(column=0, row=0, padx=10, pady=10)
        signup_button.grid(column=1, row=0, padx=10, pady=10)
