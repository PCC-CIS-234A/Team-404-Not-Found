"""
Author: Sayan Tajul
Created: 05/20/2025
Last Modified: 05/28/2025
File: send_notification.py
Course: CIS 234A – PCC Sprint 2 Part 2
"""


import tkinter.font as tkfont

# === PCC THEME COLORS ===
PCC_WHITE = "#ffffff"
PCC_BLUE = "#008099"
PCC_LIGHT_BLUE = "#e6f2ff"
PCC_DARK_BLUE = "#235578"
PCC_TEXT = "#333333"

# === Function: Apply PCC white background to all widgets ===
def apply_theme_styles(widget):
    for child in widget.winfo_children():
        try:
            child.configure(bg=PCC_WHITE)
        except:
            pass
        apply_theme_styles(child)

# === Function: Get PCC standard fonts ===
def get_fonts(root):
    default_font = tkfont.Font(root=root, family="Helvetica", size=11)
    label_font = tkfont.Font(root=root, family="Helvetica", size=12, weight="bold")
    button_font = tkfont.Font(root=root, family="Helvetica", size=11)
    return default_font, label_font, button_font

# === Optional: Get PCC color palette as dictionary ===
def get_pcc_colors():
    return {
        "background": PCC_WHITE,
        "primary": PCC_BLUE,
        "secondary": PCC_LIGHT_BLUE,
        "accent": PCC_DARK_BLUE,
        "text": PCC_TEXT
    }
