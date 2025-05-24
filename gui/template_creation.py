# =============================================================================
# Author:        Santhil Murugesan
# File:          template_creator_gui
# Created:       04/25/2025
# Project:       Food Pantry Notification System
# Module:        Template Manager  (db_connection.py, template_logic.py,
#                template_creator_gui.py and theme.py)
# Description:   GUI interface for creating, editing, and managing templates.
# Functionality: Supports adding new templates, updating existing ones,
#                and deleting templates through a user-friendly interface.
# Output:        User-driven template actions reflected in the database.
# References:    Python Documentation, Tkinter, SQL Server (pyodbc)
# =============================================================================

# Modified version of original template_creator_gui file
# Modified 5-23-2025 by RNixon

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from theme import *
from data.db_manager import Database

# -----------------------------------------------------------------------------
# Global variables
# -----------------------------------------------------------------------------
original_data = {}
current_mode = "Creating New Template"


class TemplatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        shadow_offset = 2
        shadow_label = tk.Label(
            self,
            text="TEMPLATE MANAGER",
            font=label_font,
            bg=BUTTON_HOVER,
            fg="#333333",
            padx=11,
            pady=6
        )
        shadow_label.place(
            relx=0.5, rely=0.03, anchor="n",
            x=shadow_offset, y=shadow_offset
        )

        title_label = tk.Label(
            self,
            text="TEMPLATE MANAGER",
            font=label_font,
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT,
            padx=10,
            pady=5
        )
        title_label.place(relx=0.5, rely=0.03, anchor="n")

        # Top Frame (Template selection and New button)
        frame_top = ttk.Frame(self, padding=10, style="Form.TFrame")
        frame_top.pack(fill=tk.X, pady=(80, 15))

        ttk.Label(
            frame_top, text="Select Template:", font=label_font
        ).pack(side=tk.LEFT)

        template_var = tk.StringVar()
        template_dropdown = ttk.Combobox(
            frame_top, textvariable=template_var,
            state="readonly", width=40
        )
        template_dropdown.pack(side=tk.LEFT, padx=10)

        new_button = tk.Button(
            frame_top, text="+ New", command=lambda: clear_form(),
            font=button_font,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            relief="flat", borderwidth=0, padx=10, pady=5
        )
        new_button.pack(side=tk.LEFT)

        # Form Frame (Template fields)
        form_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(2, weight=1)

        ttk.Label(
            form_frame, text="Template Name:", font=label_font
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(
            form_frame, text="Subject:", font=label_font
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        subject_entry = ttk.Entry(form_frame)
        subject_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(
            form_frame, text="Message Body:", font=label_font
        ).grid(row=2, column=0, sticky=tk.NW, pady=5)
        body_text = tk.Text(form_frame, height=10, wrap=tk.WORD)
        body_text.grid(row=2, column=1, sticky="nsew", pady=5)

        # Button Frame (Save/Delete/Cancel)
        button_frame = ttk.Frame(self, padding=10, style="Form.TFrame")
        button_frame.pack(pady=(0, 15))

        save_button = tk.Button(
            button_frame, text="Save", command=lambda: save_template(),
            font=button_font,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            relief="flat", borderwidth=0, padx=14, pady=6
        )
        save_button.pack(side=tk.LEFT, padx=10)

        delete_button = tk.Button(
            button_frame, text="Delete", command=lambda: delete_template(),
            font=button_font,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            relief="flat", borderwidth=0, padx=14, pady=6
        )
        delete_button.pack(side=tk.LEFT, padx=10)
        delete_button.config(state="disabled")

        cancel_button = tk.Button(
            button_frame, text="Cancel", command=lambda: clear_form(),
            font=button_font,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER, activeforeground=BUTTON_TEXT,
            relief="flat", borderwidth=0, padx=14, pady=6
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

        # Event bindings
        name_entry.bind("<KeyRelease>", lambda e: check_for_changes())
        subject_entry.bind("<KeyRelease>", lambda e: check_for_changes())
        body_text.bind("<KeyRelease>", lambda e: check_for_changes())

        template_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda e: load_template(template_var.get())
        )

        def refresh_template_dropdown():
            """Refresh the template dropdown with available template names."""
            names = Database.fetch_template_names()
            template_dropdown["values"] = names
            template_var.set("")

        def clear_form():
            """Clear form fields and reset to 'Creating New Template' mode."""
            name_entry.config(state="normal")
            name_entry.delete(0, tk.END)
            subject_entry.delete(0, tk.END)
            body_text.delete("1.0", tk.END)
            template_var.set("Creating New Template")
            delete_button.config(state="disabled")

            global original_data
            original_data = {"name": "", "subject": "", "body": ""}
            save_button.config(state="disabled")

        def load_template(template_name):
            """Load an existing template's data into the form."""
            if not template_name or template_name == "Creating New Template":
                return

            template = Database.fetch_template_by_name(template_name)
            if template:
                # Populate form fields
                template_var.set(template[0])  # Keep dropdown and entry synced
                name_entry.config(state="normal")
                name_entry.delete(0, tk.END)
                subject_entry.delete(0, tk.END)
                body_text.delete("1.0", tk.END)

                name_entry.insert(0, template[0])
                name_entry.config(state="readonly")
                subject_entry.insert(0, template[2])
                body_text.insert("1.0", template[3])

                delete_button.config(state="normal")

                global original_data
                original_data = {
                    "name": template[0].strip(),
                    "subject": template[2].strip(),
                    "body": template[3].strip()
                }
                save_button.config(state="disabled")

        def check_for_changes(event=None):
            """Check if current form content differs from original loaded data."""
            current = {
                "name": name_entry.get().strip(),
                "subject": subject_entry.get().strip(),
                "body": body_text.get("1.0", tk.END).strip()
            }
            if template_var.get() == "Creating New Template":
                # Enable Save if anything is filled
                if current["name"] or current["subject"] or current["body"]:
                    save_button.config(state="normal")
                else:
                    save_button.config(state="disabled")
            else:
                # Enable Save only if subject or body changed
                if (current["subject"] != original_data.get("subject") or
                        current["body"] != original_data.get("body")):
                    save_button.config(state="normal")
                else:
                    save_button.config(state="disabled")

        def save_template():
            """Save a new template or update an existing template."""
            if template_var.get() == "Creating New Template":
                name = name_entry.get().strip()
            else:
                name = template_var.get().strip()

            subject = subject_entry.get().strip()
            body = body_text.get("1.0", tk.END).strip()
            current_mode = template_var.get()
            original_name = (
                None if current_mode == "Creating New Template" else current_mode
            )

            if current_mode == "Creating New Template":
                # Validate fields
                if not name or not subject or not body:
                    messagebox.showwarning(
                        "Missing Info", "Please fill out all required fields."
                    )
                    return
                existing_templates = Database.fetch_template_names()
                if name in existing_templates:
                    messagebox.showerror(
                        "Duplicate Name",
                        f"A template named '{name}' already exists. "
                        "Please choose a unique name."
                    )
                    return

            try:
                Database.insert_or_update_template(
                    name, None, subject, body, creator_id=1,
                    original_name=original_name
                )
                messagebox.showinfo("Saved", f"Template '{name}' saved successfully.")
                refresh_template_dropdown()
                template_var.set(name)

                global original_data
                original_data = {
                    "name": name,
                    "subject": subject,
                    "body": body
                }
                save_button.config(state="disabled")
                delete_button.config(state="normal")
                name_entry.config(state="readonly")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        def delete_template():
            """Delete the selected template from the database."""
            template_name = template_var.get()
            if not template_name or template_name == "Creating New Template":
                messagebox.showwarning(
                    "Select Template", "No template selected to delete."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete", f"Delete template '{template_name}'?"
            )
            if not confirm:
                return

            try:
                conn = Database.connect()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM dbo.templates WHERE name = ?", (template_name,)
                )
                conn.commit()
                conn.close()

                messagebox.showinfo("Deleted", f"Template '{template_name}' deleted.")
                refresh_template_dropdown()
                clear_form()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Initial load
        refresh_template_dropdown()
