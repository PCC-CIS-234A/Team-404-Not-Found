# *****************************************************
# Author: R-Nixon
# Creation Date: 2025-5-1
# Last Modified: 2025-5-2
# Description:
# This module is the welcome page after a user signs into the system.
# This page greets both new users and returning users.

# Code Reference:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# *****************************************************
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

        # GUI theme
        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # Styling for the frame title
        shadow_offset = 2
        shadow_label = tk.Label(self, text="WELCOME", font=label_font, bg=BUTTON_HOVER, fg="#333333", padx=11,
                                pady=6)
        shadow_label.place(relx=0.5, rely=0.03, anchor="n", x=shadow_offset, y=shadow_offset)

        title_label = tk.Label(self, text="WELCOME", font=label_font, bg=BUTTON_COLOR, fg=BUTTON_TEXT, padx=10,
                               pady=5)
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        # Welcome text
        welcome_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        welcome_frame.place(relx=0.5, rely=0.2, anchor="n")

        welcome_label1 = ttk.Label(welcome_frame, text="Welcome the the Panther Pantry", font=label_font)
        welcome_label1.grid(row=0, column=0)
        welcome_label2 = ttk.Label(welcome_frame, text="Notification System!", font=label_font)
        welcome_label2.grid(row=1, column=0)

