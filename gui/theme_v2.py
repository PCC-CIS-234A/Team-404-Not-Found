# =============================================================================
# File:          theme_v2.py
# Project:       Food Pantry Notification System
# Description:   Centralized theming for GUI based on PCC Brand Color Palette.
# =============================================================================

import tkinter.font as tkfont
from tkinter import ttk

# ---------------------------------------------------------------------
# PCC Brand Colors (Primary)
# ---------------------------------------------------------------------
PCC_TURQUOISE = "#008EAA"
PCC_NAVY = "#000000"

# ---------------------------------------------------------------------
# PCC Secondary & Tertiary Colors (Selected for UI elements)
# ---------------------------------------------------------------------
PCC_SEAFOAM_GREEN = "#ADC8B8"
PCC_LIGHT_TAN = "#C3BEB5"
PCC_TAN = "#8A837A"
PCC_SALMON_PINK = "#FF8571"
PCC_GOLDEN_YELLOW = "#EBA904"

# ---------------------------------------------------------------------
# UI Palette derived from PCC Colors
# ---------------------------------------------------------------------
# Backgrounds
APP_BACKGROUND = "#FDFEFF"
SECTION_BG_ALT = "#FFFFFF"  # Light grey for alternate sections F0F4F5
DISABLED_BG = "#EAEAEA"
LOGO_AREA_BACKGROUND = "#FFFFFF"
HEADER_BACKGROUND = LOGO_AREA_BACKGROUND

# Text Colors
TEXT_COLOR = PCC_NAVY
SUBTLE_TEXT_COLOR = PCC_TAN
DISABLED_TEXT_COLOR = "#909090"
BUTTON_TEXT = "#FFFFFF"

# Borders & Focus
BORDER_COLOR = PCC_LIGHT_TAN
FOCUS_BORDER_COLOR = PCC_TURQUOISE
HEADER_BORDER_COLOR = "#202020"
SECTION_BORDER_COLOR = "#D0D3D4"  # Border for raised sections

# Buttons
PRIMARY_BUTTON_COLOR = PCC_TURQUOISE
PRIMARY_BUTTON_HOVER = "#007C99"
PRIMARY_BUTTON_TEXT = BUTTON_TEXT

SECONDARY_BUTTON_COLOR = "#A0A0A0"
SECONDARY_BUTTON_HOVER = "#8A8A8A"
SECONDARY_BUTTON_TEXT = BUTTON_TEXT

TITLE_BAR_BACKGROUND = PCC_TURQUOISE
TITLE_BAR_TEXT_COLOR = BUTTON_TEXT

# ---------------------------------------------------------------------
# Standard Padding & Spacing
# ---------------------------------------------------------------------
PAD_XLARGE = 20
PAD_LARGE = 15
PAD_MEDIUM = 10
PAD_SMALL = 5
PAD_XSMALL = 3


# ---------------------------------------------------------------------
# Font Utilities
# ---------------------------------------------------------------------
def get_fonts(root=None):
    """
    Returns a tuple of (default_font, label_font (bold), button_font).
    """
    try:
        base_family = "Segoe UI"
        tkfont.nametofont("TkDefaultFont").actual("family")
    except tkfont.TclError:
        base_family = "Arial"
    except Exception:
        base_family = "Helvetica"

    font_size_default = 12
    font_size_button = 12
    font_size_label = 13

    default_font = tkfont.Font(family=base_family, size=font_size_default)
    label_font = tkfont.Font(family=base_family, size=font_size_label,
                             weight="bold")
    button_font = tkfont.Font(family=base_family, size=font_size_button,
                              weight="bold")

    return default_font, label_font, button_font


# ---------------------------------------------------------------------
# Style Utilities
# ---------------------------------------------------------------------
def apply_theme_styles(root=None):
    """
    Apply PCC color palette and styles to ttk widgets.
    """
    style = ttk.Style()
    style.theme_use("default")

    default_font, bold_label_font, button_font = get_fonts(root)

    if root:
        root.option_add("*Font", default_font)
        root.configure(bg=APP_BACKGROUND)

    style.configure(".",
                    background=APP_BACKGROUND,
                    foreground=TEXT_COLOR,
                    font=default_font,
                    relief="flat")

    style.configure("TFrame", background=APP_BACKGROUND)
    style.configure("RaisedSectionInner.TFrame", background=SECTION_BG_ALT)


    # Style for the "grey inner box" - RaisedSection.TFrame
    style.configure("RaisedSection.TFrame",
                    background=SECTION_BG_ALT,
                    relief="raised",
                    borderwidth=1,
                    bordercolor=SECTION_BORDER_COLOR)

    # Label styles
    style.configure("TLabel", font=default_font, background=APP_BACKGROUND,
                    foreground=TEXT_COLOR, padding=(0, PAD_SMALL))
    style.configure("RaisedSection.TLabel", font=default_font,
                    background=SECTION_BG_ALT, foreground=TEXT_COLOR,
                    padding=(0, PAD_SMALL))
    style.configure("Bold.TLabel", font=bold_label_font,
                    background=APP_BACKGROUND, foreground=TEXT_COLOR)
    style.configure("RaisedSection.Bold.TLabel", font=bold_label_font,
                    background=SECTION_BG_ALT, foreground=TEXT_COLOR)

    header_title_font = tkfont.Font(family=bold_label_font.cget("family"),
                                    size=bold_label_font.cget("size") + 3,
                                    weight="bold")

    style.configure("LogoArea.TFrame",
                    background=LOGO_AREA_BACKGROUND,
                    relief="flat",
                    borderwidth=0,
                    padding=(PAD_XSMALL, PAD_XSMALL))

    style.configure("Logo.TLabel",
                    background=LOGO_AREA_BACKGROUND,
                    padding=(0, 0))

    style.configure("TitleBar.TFrame",
                    background=TITLE_BAR_BACKGROUND,
                    relief="flat",
                    borderwidth=0,
                    padding=(PAD_XSMALL, PAD_XSMALL))

    style.configure("TitleHeader.TLabel",
                    font=header_title_font,
                    background=TITLE_BAR_BACKGROUND,
                    foreground=TITLE_BAR_TEXT_COLOR,
                    anchor="center",
                    padding=(PAD_MEDIUM, PAD_XSMALL))

    style.configure(
        "Hint.TLabel", # For hints on APP_BACKGROUND
        font=(default_font.cget("family"), default_font.cget("size") - 1, "italic"),
        background=APP_BACKGROUND,
        foreground=SUBTLE_TEXT_COLOR
    )
    style.configure("RaisedSection.Hint.TLabel", # For hints on SECTION_BG_ALT
                    font=(default_font.cget("family"), default_font.cget("size") - 1, "italic"),
                    background=SECTION_BG_ALT,
                    foreground=TEXT_COLOR # Default to darker text color as per image
                    )

    style.configure(
        "TButton",
        font=button_font,
        background=PRIMARY_BUTTON_COLOR,
        foreground=PRIMARY_BUTTON_TEXT,
        padding=(PAD_MEDIUM, PAD_SMALL),
        relief="raised",
        borderwidth=1
    )
    style.map(
        "TButton",
        background=[("active", PRIMARY_BUTTON_HOVER),
                    ("!active", PRIMARY_BUTTON_COLOR),
                    ("disabled", DISABLED_BG)],
        foreground=[("disabled", DISABLED_TEXT_COLOR),
                    ("!disabled", PRIMARY_BUTTON_TEXT)],
        relief=[("pressed", "sunken"), ("!disabled !pressed", "raised")]
    )

    style.configure(
        "Secondary.TButton",
        font=default_font, # Consider button_font if boldness is desired
        background=SECONDARY_BUTTON_COLOR,
        foreground=SECONDARY_BUTTON_TEXT,
        padding=(PAD_MEDIUM, PAD_SMALL),
        relief="raised",
        borderwidth=1
    )
    style.map(
        "Secondary.TButton",
        background=[("active", SECONDARY_BUTTON_HOVER),
                    ("!active", SECONDARY_BUTTON_COLOR),
                    ("disabled", DISABLED_BG)],
        foreground=[("disabled", DISABLED_TEXT_COLOR),
                    ("!disabled", SECONDARY_BUTTON_TEXT)],
        relief=[("pressed", "sunken"), ("!disabled !pressed", "raised")]
    )

    style.configure("TSeparator", background=BORDER_COLOR)

    style.configure("TCombobox",
                    font=default_font,
                    padding=PAD_SMALL,
                    relief="sunken",
                    borderwidth=1,
                    bordercolor=BORDER_COLOR
                    )
    style.map("TCombobox",
              fieldbackground=[("readonly", "white"),
                               ("disabled", DISABLED_BG), ("focus", "white")],
              foreground=[("disabled", DISABLED_TEXT_COLOR)],
              bordercolor=[("focus", FOCUS_BORDER_COLOR),
                           ("!focus", BORDER_COLOR)],
              selectbackground=[("focus", PRIMARY_BUTTON_COLOR)],
              selectforeground=[("focus", PRIMARY_BUTTON_TEXT)]
              )

    if root:
        root.option_add("*TCombobox*Listbox.font", default_font)
        root.option_add("*TCombobox*Listbox.background", "white")
        root.option_add("*TCombobox*Listbox.selectBackground",
                        PRIMARY_BUTTON_COLOR)
        root.option_add("*TCombobox*Listbox.selectForeground",
                        PRIMARY_BUTTON_TEXT)
        root.option_add("*TCombobox*Listbox.relief", "flat")
        root.option_add("*TCombobox*Listbox.borderwidth", 1)
        root.option_add("*TCombobox*Listbox.bordercolor", BORDER_COLOR)

    style.configure("TEntry",
                    font=default_font,
                    padding=(PAD_SMALL + 2), # Consistent padding for tk.Entry might need manual adjustment
                    relief="sunken", # ttk.Entry uses this, tk.Entry uses FLAT then highlight
                    borderwidth=1,
                    bordercolor=BORDER_COLOR # Default border color
                    )
    style.map("TEntry", # Affects ttk.Entry
              bordercolor=[("focus", FOCUS_BORDER_COLOR), ("!focus", BORDER_COLOR)],
              foreground=[("disabled", DISABLED_TEXT_COLOR), ("readonly", SUBTLE_TEXT_COLOR)],
              fieldbackground=[("disabled", DISABLED_BG), ("readonly", DISABLED_BG), ("focus", "white")]
              )

    style.configure("Vertical.TScrollbar",
                    relief="flat",
                    background=SECONDARY_BUTTON_COLOR, # Scrollbar handle color
                    troughcolor=APP_BACKGROUND,       # Scrollbar trough color
                    borderwidth=0,
                    arrowcolor=TEXT_COLOR) # Color of the arrows on the scrollbar
    style.map("Vertical.TScrollbar",
              background=[('active', SECONDARY_BUTTON_HOVER)], # Handle color on hover
              )