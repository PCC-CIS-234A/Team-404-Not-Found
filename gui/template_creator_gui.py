import tkinter as tk
from tkinter import ttk, messagebox
from gui.theme import apply_theme_styles, get_fonts, APP_BACKGROUND, BUTTON_COLOR, BUTTON_HOVER, BUTTON_TEXT
from logic.template_logic import insert_or_update_template, fetch_template_names, fetch_template_by_name
from data.db_connection import get_connection

class TemplatePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        # [Place your GUI setup here from original file, replacing "root" with "self"]

        # Example snippet to begin adaptation:
        ttk.Label(self, text="Template Manager", font=label_font).pack(pady=10)

        # Continue transferring all widgets and methods here,
        # replacing the root widget references with self.

        # For example:
        self.template_var = tk.StringVar()
        self.template_dropdown = ttk.Combobox(self, textvariable=self.template_var)
        self.template_dropdown.pack()

        # Bind events and other GUI logic as methods inside this class
        self.refresh_template_dropdown()

    def refresh_template_dropdown(self):
        names = fetch_template_names()
        self.template_dropdown["values"] = names
        self.template_var.set("")

    # Add other methods similarly inside this class
