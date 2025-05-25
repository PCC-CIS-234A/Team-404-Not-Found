# =============================================================================
<<<<<<< HEAD
# Author:              Santhil Murugesan
# File:                    theme.py
# Created:            04/25/2025
# Project:              Food Pantry Notification System
# Module:           All modules in this project use this file as a common resource.
# Description:    Centralized theming for consistent GUI design.
# Functionality: Defines colors, fonts, and widget styles for uniform
#                              appearance.
# Output:             Consistent look and feel across all GUI windows and
#                              controls.
# References:     Python Documentation, Tkinter ttk Styling
=======
# Author:        Santhil Murugesan
# File:          theme.py
# Created:       04/25/2025
# Project:       Food Pantry Notification System
# Module:        All modules in this project use this file as a common resource.
# Description:   Centralized theming for consistent GUI design.
# Functionality: Defines colors, fonts, and widget styles for uniform
#                appearance.
# Output:        Consistent look and feel across all GUI windows and
#                controls.
# References:    Python Documentation, Tkinter ttk Styling
>>>>>>> santhil_template_creation
# =============================================================================

import tkinter.font as tkfont

# -----------------------------------------------------------------------------
# Brand Colors
# -----------------------------------------------------------------------------
LOGO_GROCERY_BAG = "#235578"
LOGO_TEXT = "#1690b4"

# -----------------------------------------------------------------------------
# PCC & UI Palette
# -----------------------------------------------------------------------------
PCC_HEADER = "#008099"
PCC_TEAL_SHADOW = "#00667a"
PCC_BLUE_SHADOW = "#263c53"
BG_LIGHT = "#f5f5f5"
APP_BACKGROUND = "#f7f9fb"  # Unified app background

# -----------------------------------------------------------------------------
# Button Colors
# -----------------------------------------------------------------------------
BUTTON_COLOR = "#007b8a"
BUTTON_HOVER = "#005f69"
BUTTON_TEXT = "#ffffff"

# -----------------------------------------------------------------------------
# Font Utilities
# -----------------------------------------------------------------------------


def get_fonts(root):
    """
    Returns a tuple of (default_font, bold_label_font, bold_button_font).

    Args:
        root (tk.Tk or tk.Toplevel): The root window used to derive font settings.

    Returns:
        tuple: (base_font, bold_label_font, bold_button_font)
    """
    base = tkfont.nametofont("TkDefaultFont")
    base.configure(size=11)

    label_bold = tkfont.Font(
        family=base.actual("family"),
        size=16,
        weight="bold"
    )

    button_bold = tkfont.Font(
        family=base.actual("family"),
        size=11,
        weight="bold"
    )

    return base, label_bold, button_bold

# -----------------------------------------------------------------------------
# Style Utilities
# -----------------------------------------------------------------------------


def apply_theme_styles(root=None):
    """
    Apply font, color, and widget style themes across the application.

    Args:
        root (tk.Tk or tk.Toplevel, optional): The main window to apply default font.
    """
    from tkinter import ttk

    style = ttk.Style()
    style.theme_use("default")

    if root:
        # Apply base font application-wide
        default_font, _, _ = get_fonts(root)
        root.option_add("*Font", default_font)

    # Configure frame backgrounds
    style.configure("Form.TFrame", background=APP_BACKGROUND)

    # Label styles
    style.configure(
        "TLabel",
        background=APP_BACKGROUND,
        foreground="#333333"
    )

    style.configure(
        "Header.TLabel",
        background=PCC_HEADER,
        foreground="white"
    )
    style.configure(
        "Preview.TLabel",
        background=PCC_TEAL_SHADOW,
        foreground="white"
    )

    # Button styles (for ttk.Button only)
    style.configure(
        "TButton",
        background=BUTTON_COLOR,
        foreground=BUTTON_TEXT,
        padding=6,
        relief="flat"
    )
    style.map(
        "TButton",
        background=[("active", BUTTON_HOVER)],
        foreground=[("active", BUTTON_TEXT)]
    )
<<<<<<< HEAD
    
=======
>>>>>>> santhil_template_creation
