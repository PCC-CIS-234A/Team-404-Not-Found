# =============================================================================
# Author:        Santhil Murugesan (UI Refinements by AI)
# File:          template_creator_gui.py
# Created:       04/25/2025
# Project:       Food Pantry Notification System
# Module:        Template Manager
# Description:   GUI interface for creating, editing, and managing templates.
#                Uses an image for the main title.
# =============================================================================
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

# Assuming these paths are correct for your project structure
from data.db_manager import Database
from gui.theme_v2 import (
    apply_theme_styles,
    get_fonts,
    APP_BACKGROUND,
    DISABLED_BG,
    TEXT_COLOR,
    DISABLED_TEXT_COLOR,
    SUBTLE_TEXT_COLOR,
    BORDER_COLOR,
    FOCUS_BORDER_COLOR,
    PAD_LARGE,
    PAD_MEDIUM,
    PAD_SMALL,
    PAD_XSMALL,
    HEADER_BACKGROUND,
    TITLE_BAR_BACKGROUND,
    SECTION_BG_ALT
)
from logic.template_logic import insert_or_update_template, \
    fetch_template_names, fetch_template_by_name


class TemplateCreatorGUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, bold_label_font, button_font_obj = get_fonts(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        current_main_row = 0

        self.back_arrow_icon_tk = None
        back_arrow_file_name = "arrowback.jpg"
        script_dir = os.path.dirname(__file__)
        paths_to_try_arrow = [
            os.path.join(script_dir, "assets", back_arrow_file_name),
            os.path.join(script_dir, back_arrow_file_name),
            back_arrow_file_name
        ]
        arrow_path_to_use = next(
            (path for path in paths_to_try_arrow if os.path.exists(path)),
            None)
        if arrow_path_to_use:
            try:
                arrow_image_pil = Image.open(arrow_path_to_use)
                arrow_height = int(button_font_obj.cget("size") * 1.5)
                if arrow_height < 16: arrow_height = 16
                aspect_ratio_arrow = arrow_image_pil.width / arrow_image_pil.height
                arrow_width = int(arrow_height * aspect_ratio_arrow)
                arrow_image_resized = arrow_image_pil.resize(
                    (arrow_width, arrow_height), Image.Resampling.LANCZOS)
                self.back_arrow_icon_tk = ImageTk.PhotoImage(
                    arrow_image_resized)
            except Exception as e:
                print(
                    f"Error loading back arrow icon '{back_arrow_file_name}': {e}")

        top_bar_frame = ttk.Frame(self, style="AppHeader.TFrame")
        top_bar_frame.grid(row=current_main_row, column=0, sticky="ew",
                           pady=(0, PAD_XSMALL))
        top_bar_frame.grid_columnconfigure(0, weight=0)
        top_bar_frame.grid_columnconfigure(1, weight=1)
        top_bar_frame.grid_columnconfigure(2, weight=0)

        back_button = ttk.Button(
            top_bar_frame, text="Back", image=self.back_arrow_icon_tk,
            compound=tk.LEFT, style="TButton",
            command=lambda: self._go_back(controller)
        )
        if self.back_arrow_icon_tk:
            back_button.image = self.back_arrow_icon_tk
        back_button.grid(row=0, column=0, sticky="w",
                         padx=(PAD_LARGE, PAD_MEDIUM), pady=PAD_SMALL)

        title_bar_frame = ttk.Frame(top_bar_frame, style="TitleBar.TFrame")
        title_bar_frame.grid(row=0, column=1, sticky="nsew")
        title_bar_frame.grid_columnconfigure(0, weight=1)

        self.title_image_tk = None
        title_image_file_name = "templatecreator.png"
        paths_to_try_title_img = [
            os.path.join(script_dir, "assets", title_image_file_name),
            os.path.join(script_dir, title_image_file_name),
            title_image_file_name
        ]
        title_img_path_to_use = next(
            (path for path in paths_to_try_title_img if os.path.exists(path)),
            None)
        app_heading_label = None
        if title_img_path_to_use:
            try:
                title_image_pil = Image.open(title_img_path_to_use)
                title_image_height = 30
                aspect_ratio_title = title_image_pil.width / title_image_pil.height
                title_image_width = int(
                    title_image_height * aspect_ratio_title)
                title_image_resized = title_image_pil.resize(
                    (title_image_width, title_image_height),
                    Image.Resampling.LANCZOS)
                self.title_image_tk = ImageTk.PhotoImage(title_image_resized)
                app_heading_label = ttk.Label(title_bar_frame,
                                              image=self.title_image_tk,
                                              style="TitleHeader.TLabel")
                app_heading_label.image = self.title_image_tk
            except Exception as e:
                print(
                    f"Error loading title image '{title_image_file_name}': {e}")
        if not app_heading_label:  # Fallback if image loading failed or path not found
            app_heading_label = ttk.Label(title_bar_frame,
                                          text="T E M P L A T E  C R E A T O R",
                                          style="TitleHeader.TLabel")
        if app_heading_label:
            app_heading_label.grid(row=0, column=0, sticky="nsew")

        logo_display_frame = ttk.Frame(top_bar_frame, style="LogoArea.TFrame")
        logo_display_frame.grid(row=0, column=2, sticky="e",
                                padx=(PAD_MEDIUM, PAD_LARGE), pady=PAD_XSMALL)
        pcc_logo_file_name = "PCC-Primary-Logo-R_Turquoise.png"
        paths_to_try_pcc_logo = [
            os.path.join(script_dir, "assets", pcc_logo_file_name),
            os.path.join(script_dir, pcc_logo_file_name), pcc_logo_file_name
        ]
        pcc_logo_path_to_use = next(
            (path for path in paths_to_try_pcc_logo if os.path.exists(path)),
            None)
        pcc_logo_label_widget = None
        if pcc_logo_path_to_use:
            try:
                pcc_logo_image_pil = Image.open(pcc_logo_path_to_use)
                title_font_approx_height_for_pcc = bold_label_font.cget(
                    "size") + 1
                pcc_logo_height = int(title_font_approx_height_for_pcc * 2.5)
                aspect_ratio_pcc = pcc_logo_image_pil.width / pcc_logo_image_pil.height
                pcc_logo_width = int(pcc_logo_height * aspect_ratio_pcc)
                pcc_logo_image_resized = pcc_logo_image_pil.resize(
                    (pcc_logo_width, pcc_logo_height),
                    Image.Resampling.LANCZOS)
                self.pcc_logo_photo_tk = ImageTk.PhotoImage(
                    pcc_logo_image_resized)
                pcc_logo_label_widget = ttk.Label(logo_display_frame,
                                                  image=self.pcc_logo_photo_tk,
                                                  style="Logo.TLabel")
                pcc_logo_label_widget.image = self.pcc_logo_photo_tk
            except Exception as e:
                print(f"Error processing PCC logo image: {e}")
        if not pcc_logo_label_widget:  # Fallback if image loading failed or path not found
            pcc_logo_label_widget = ttk.Label(logo_display_frame, text="PCC",
                                              style="Logo.TLabel")
        pcc_logo_label_widget.pack(padx=PAD_SMALL, pady=PAD_XSMALL)

        current_main_row += 1

        content_body_frame = ttk.Frame(self, style="RaisedSection.TFrame",
                                       padding=PAD_MEDIUM)
        content_body_frame.grid(row=current_main_row, column=0, sticky="nsew",
                                padx=PAD_LARGE, pady=(PAD_SMALL, PAD_LARGE))
        content_body_frame.grid_columnconfigure(1,
                                                weight=1)  # For name_entry, tag_dropdown, subject_entry, message_body
        content_body_frame.grid_columnconfigure(3,
                                                weight=1)  # For template_dropdown
        content_body_frame.grid_rowconfigure(3,
                                             weight=1)  # Row for message_outer_frame (Message Body)

        current_content_row = 0

        ttk.Label(content_body_frame, text="Template Name:",
                  style="RaisedSection.Bold.TLabel").grid(
            row=current_content_row, column=0, sticky="e", padx=(0, PAD_SMALL),
            pady=PAD_MEDIUM)
        self.name_entry = ttk.Entry(content_body_frame)
        self.name_entry.grid(row=current_content_row, column=1, sticky="ew",
                             padx=(0, PAD_MEDIUM), pady=PAD_MEDIUM)
        ttk.Label(content_body_frame, text="Existing Templates:",
                  style="RaisedSection.Bold.TLabel").grid(
            row=current_content_row, column=2, sticky="e",
            padx=(PAD_MEDIUM, PAD_SMALL), pady=PAD_MEDIUM)
        self.template_var = tk.StringVar()
        self.template_dropdown = ttk.Combobox(content_body_frame,
                                              textvariable=self.template_var,
                                              state="readonly")
        self.template_dropdown.grid(row=current_content_row, column=3,
                                    sticky="ew", pady=PAD_MEDIUM)
        current_content_row += 1

        ttk.Label(content_body_frame, text="Insert Tag:",
                  style="RaisedSection.Bold.TLabel").grid(
            row=current_content_row, column=0, sticky="e", padx=(0, PAD_SMALL),
            pady=(PAD_MEDIUM, 0))
        self.tag_var = tk.StringVar()
        self.tag_dropdown = ttk.Combobox(content_body_frame,
                                         textvariable=self.tag_var,
                                         state="disabled")
        self.tag_dropdown.configure(
            postcommand=lambda: self.tag_dropdown.configure(
                values=self.load_tags()))
        self.tag_dropdown.grid(row=current_content_row, column=1, sticky="ew",
                               padx=(0, PAD_MEDIUM), pady=(PAD_MEDIUM, 0))
        self.hint_label = ttk.Label(content_body_frame, text="",
                                    style="RaisedSection.Hint.TLabel")  # Default empty
        self.hint_label.grid(row=current_content_row, column=2, columnspan=2,
                             sticky="w", padx=(PAD_SMALL, 0),
                             pady=(PAD_MEDIUM, 0))
        current_content_row += 1

        ttk.Label(content_body_frame, text="Subject:",
                  style="RaisedSection.Bold.TLabel").grid(
            row=current_content_row, column=0, sticky="e", padx=(0, PAD_SMALL),
            pady=(PAD_MEDIUM, PAD_SMALL))
        self.subject_entry = tk.Entry(content_body_frame, font=default_font,
                                      relief=tk.FLAT,
                                      borderwidth=1, highlightthickness=1,
                                      fg=TEXT_COLOR, bg="white",
                                      insertbackground=TEXT_COLOR,
                                      disabledbackground=DISABLED_BG,
                                      highlightbackground=BORDER_COLOR,
                                      highlightcolor=FOCUS_BORDER_COLOR,
                                      disabledforeground=DISABLED_TEXT_COLOR,
                                      readonlybackground=DISABLED_BG)
        self.subject_entry.grid(row=current_content_row, column=1,
                                columnspan=3, sticky="ew",
                                pady=(PAD_MEDIUM, PAD_SMALL))
        current_content_row += 1

        ttk.Label(content_body_frame, text="Message:",
                  style="RaisedSection.Bold.TLabel").grid(
            row=current_content_row, column=0, sticky="ne",
            padx=(0, PAD_SMALL), pady=(PAD_MEDIUM, 0))
        message_outer_frame = ttk.Frame(content_body_frame, style="TFrame")
        message_outer_frame.grid(row=current_content_row, column=1,
                                 columnspan=3, sticky="nsew",
                                 pady=(PAD_MEDIUM, 0))
        message_outer_frame.grid_rowconfigure(0, weight=1)
        message_outer_frame.grid_columnconfigure(0, weight=1)
        message_outer_frame.configure(relief="sunken", borderwidth=1)
        scrollbar = ttk.Scrollbar(message_outer_frame, orient="vertical",
                                  style="Vertical.TScrollbar")
        scrollbar.grid(row=0, column=1, sticky="ns", pady=PAD_XSMALL,
                       padx=PAD_XSMALL)
        self.body_text = tk.Text(message_outer_frame, wrap=tk.WORD,
                                 yscrollcommand=scrollbar.set,
                                 font=default_font, relief=tk.FLAT,
                                 borderwidth=0, highlightthickness=0,
                                 fg=TEXT_COLOR, background="white",
                                 insertbackground=TEXT_COLOR,
                                 state=tk.DISABLED,
                                 height=15)  # MODIFIED: Added height option
        self.body_text.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.body_text.tag_config("tag", font=(default_font.cget("family"),
                                               default_font.cget("size"),
                                               "bold"))
        scrollbar.config(command=self.body_text.yview)
        current_content_row += 1

        action_buttons_outer_frame = ttk.Frame(content_body_frame,
                                               style="RaisedSectionInner.TFrame")
        action_buttons_outer_frame.grid(row=current_content_row, column=1,
                                        columnspan=3, sticky="ew",
                                        pady=(PAD_MEDIUM, PAD_MEDIUM))

        buttons_inner_frame = ttk.Frame(action_buttons_outer_frame,
                                        style="RaisedSectionInner.TFrame")
        buttons_inner_frame.grid(row=0, column=0,
                                 sticky="w")  # Align buttons to the left

        button_definitions = [
            ("+ New", self.clear_form, "new_button", "TButton", None),
            ("Edit", self.enable_edit_mode, "edit_button", "TButton", None),
            ("Save As...", self.save_as_template, "save_as_button", "TButton",
             None),
            ("Save", self.save_template, "save_button", "TButton", None),
            ("Delete", self.delete_template, "delete_button",
             "Secondary.TButton", None),
            ("Cancel", self.clear_form, "cancel_button", "Secondary.TButton",
             None)
        ]
        for i, (label, cmd, attr_name, btn_style, icon_img) in enumerate(
                button_definitions):
            btn_width = 10 if "Save As" in label else 8
            btn = ttk.Button(buttons_inner_frame, text=label, command=cmd,
                             style=btn_style, width=btn_width)
            if i == 0:  # First button
                btn.grid(row=0, column=i, padx=(0, PAD_XSMALL), pady=0)
            else:  # Subsequent buttons
                btn.grid(row=0, column=i, padx=(PAD_XSMALL, PAD_XSMALL),
                         pady=0)
            setattr(self, attr_name, btn)

        self.refresh_template_dropdown()
        self.template_dropdown.bind("<<ComboboxSelected>>",
                                    lambda e: self.on_template_selected())
        self.tag_dropdown.bind("<<ComboboxSelected>>",
                               self.insert_selected_tag)
        self.tag_dropdown.bind("<Button-1>", self._on_tag_dropdown_click)

        self.subject_entry.bind("<FocusIn>", self.on_focus)
        self.subject_entry.bind("<KeyRelease>",
                                self._update_save_as_button_state)
        self.body_text.bind("<FocusIn>", self.on_focus)
        self.body_text.bind("<KeyRelease>", self._update_save_as_button_state)
        self.last_focused = None

        self.clear_form()
        self._update_tk_entry_border(self.subject_entry, BORDER_COLOR)

    def _update_tk_entry_border(self, widget, color):
        if widget == self.subject_entry:
            widget.configure(highlightbackground=color, highlightcolor=color)

    def _go_back(self, controller):
        try:
            # Ensure ManagerWelcome is correctly imported relative to your project structure
            from manager_welcome import ManagerWelcome
            controller.show_frame(ManagerWelcome)
        except ImportError:
            messagebox.showerror("Navigation Error",
                                 "Could not load the Manager Welcome screen.")
            print(
                "Error: Could not import ManagerWelcome. Check path and class name.")

    def load_tags(self):
        try:
            cursor = Database.get_cursor()
            cursor.execute("SELECT tag_name, description FROM dbo.tags")
            return [f"{desc} – {tag}" for tag, desc in cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("DB Error", f"Failed to load tags: {e}")
            return []

    def _on_tag_dropdown_click(self, event=None):
        if self.tag_dropdown.cget('state') == tk.DISABLED:
            self.hint_label.configure(
                text="Click on the Message body to enable tag selection.",
                foreground=SUBTLE_TEXT_COLOR,
                style="RaisedSection.Hint.TLabel"
            )

    def on_focus(self, event):
        self.last_focused = event.widget
        self._update_tk_entry_border(self.subject_entry, BORDER_COLOR)
        current_hint_text = self.hint_label.cget("text")
        msg_to_clear_when_body_focused = "Click on the Message body to enable tag selection."

        if self.last_focused == self.body_text:
            self.tag_dropdown.config(state="readonly")
            if current_hint_text == msg_to_clear_when_body_focused:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
        elif self.last_focused == self.subject_entry:
            self.tag_dropdown.config(state="disabled")
            if current_hint_text == msg_to_clear_when_body_focused:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
            self._update_tk_entry_border(self.subject_entry,
                                         FOCUS_BORDER_COLOR)
        else:
            self.tag_dropdown.config(state="disabled")
            if current_hint_text == msg_to_clear_when_body_focused:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")

    def insert_selected_tag(self, event=None):
        selected = self.tag_var.get()
        if "–" in selected:
            label = selected.split("–")[-1].strip()
            safe_tag = "{{" + label.lower().replace(' ', '_') + "}}"
            if self.last_focused != self.body_text:
                messagebox.showwarning("Invalid Target",
                                       "Tags can only be inserted into the Message body.")
                self.tag_var.set("")
                return
            if self.body_text.cget("state") == tk.DISABLED:
                messagebox.showinfo("Read Only",
                                    "Enable editing to insert tags into the message body.")
                self.tag_var.set("")
                return
            try:
                start_index = self.body_text.index(tk.INSERT)
                self.body_text.insert(start_index, safe_tag)
                end_index = f"{start_index}+{len(safe_tag)}c"
                self.body_text.tag_add("tag", start_index, end_index)
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
            except Exception as e:
                messagebox.showerror("Insertion Error",
                                     f"Could not insert tag: {e}")
                self.hint_label.configure(text="Failed to insert tag.",
                                          foreground="red",
                                          style="RaisedSection.Hint.TLabel")
        self.tag_var.set("")

    def refresh_template_dropdown(self):
        names = fetch_template_names()
        self.template_dropdown["values"] = names
        current = self.template_var.get()
        if current not in names:
            self.template_var.set("")
            self.template_dropdown.set("")

    def _set_text_widget_state(self, widget, state):
        tk_state = state
        if widget == self.subject_entry:
            widget.config(state=tk_state)
            widget.config(bg="white" if tk_state == tk.NORMAL else DISABLED_BG,
                          fg=TEXT_COLOR if tk_state == tk.NORMAL else DISABLED_TEXT_COLOR)
        elif widget == self.body_text:
            widget.config(state=tk_state)
            widget.config(
                background="white" if tk_state == tk.NORMAL else DISABLED_BG,
                fg=TEXT_COLOR if tk_state == tk.NORMAL else DISABLED_TEXT_COLOR)

    def _update_save_as_button_state(self, event=None):
        subject_empty = not self.subject_entry.get().strip()
        body_content = self.body_text.get("1.0", tk.END).strip()
        body_empty = not body_content

        if hasattr(self, 'save_as_button'):
            if subject_empty and body_empty:
                self.save_as_button.config(state="disabled")
            else:
                self.save_as_button.config(state="normal")

    def clear_form(self):
        self.name_entry.config(state="normal")
        self._set_text_widget_state(self.subject_entry, tk.NORMAL)
        self._set_text_widget_state(self.body_text, tk.NORMAL)
        self.name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)
        self.body_text.tag_remove("tag", "1.0", tk.END)
        self.template_var.set("")
        self.name_entry.focus()
        self.delete_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.tag_dropdown.config(state="disabled")
        self.hint_label.configure(text="", style="RaisedSection.Hint.TLabel")
        self._update_tk_entry_border(self.subject_entry, BORDER_COLOR)
        self._update_save_as_button_state()

    def load_template(self, template_name, from_save_operation=False):
        if not template_name:
            self.clear_form()
            return
        template = fetch_template_by_name(template_name)
        if template:
            self.name_entry.config(state="normal")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, template[0])
            self.name_entry.config(state="readonly")
            self._set_text_widget_state(self.subject_entry, tk.NORMAL)
            self.subject_entry.delete(0, tk.END)
            self.subject_entry.insert(0, template[2])
            self._set_text_widget_state(self.subject_entry, tk.DISABLED)
            self._set_text_widget_state(self.body_text, tk.NORMAL)
            self.body_text.delete("1.0", tk.END)
            self.body_text.insert("1.0", template[3])
            self._set_text_widget_state(self.body_text, tk.DISABLED)
            self.template_var.set(template[0])
            self.delete_button.config(state="normal")
            self.save_button.config(state="disabled")
            self.edit_button.config(state="normal")
            self.tag_dropdown.config(state="disabled")
            if not from_save_operation:
                self.hint_label.configure(
                    text="Template loaded. Click 'Edit' to modify.",
                    foreground=SUBTLE_TEXT_COLOR,
                    style="RaisedSection.Hint.TLabel")
            else:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
        else:
            messagebox.showerror("Load Error",
                                 f"Could not find template: {template_name}")
            self.clear_form()
        self._update_tk_entry_border(self.subject_entry, BORDER_COLOR)
        self._update_save_as_button_state()

    def save_as_template(self):
        subject = self.subject_entry.get().strip()
        body_content = self.body_text.get("1.0", tk.END).strip()

        if not subject and not body_content:
            messagebox.showwarning("Missing Info",
                                   "Subject or Message must have content to Save As.")
            return

        new_name = simpledialog.askstring("Save As Template",
                                          "Enter new template name:",
                                          parent=self.winfo_toplevel())
        if not new_name:
            return
        new_name = new_name.strip()
        if not new_name:
            messagebox.showwarning("Invalid Name",
                                   "Template name cannot be empty.")
            return

        existing_names = fetch_template_names()
        if new_name in existing_names:
            messagebox.showerror("Duplicate Name",
                                 f"A template named '{new_name}' already exists. Please choose a different name.")
            return
        try:
            insert_or_update_template(new_name, "General", subject,
                                      body_content, creator_id=1,
                                      original_name=new_name)
            messagebox.showinfo("Saved As",
                                f"Template '{new_name}' saved successfully.")
            self.refresh_template_dropdown()
            self.template_var.set(new_name)
            self.load_template(new_name, from_save_operation=True)
        except Exception as e:
            messagebox.showerror("Save Error",
                                 f"Failed to save template '{new_name}': {str(e)}")
            self.hint_label.configure(
                text=f"Error saving template '{new_name}'.", foreground="red",
                style="RaisedSection.Hint.TLabel")

    def save_template(self):
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        if not name or not subject or not body:
            messagebox.showwarning("Missing Info",
                                   "Template Name, Subject, and Message are required.")
            return

        original_loaded_name = self.template_var.get()
        is_name_field_readonly = (self.name_entry.cget('state') == 'readonly')

        db_original_name_for_update = name
        if is_name_field_readonly:
            db_original_name_for_update = original_loaded_name
        elif original_loaded_name and name != original_loaded_name:
            db_original_name_for_update = original_loaded_name

        is_new_template_or_name_changed = not original_loaded_name or (
                    original_loaded_name and name != original_loaded_name)
        if not is_name_field_readonly and is_new_template_or_name_changed:
            existing_names = fetch_template_names()
            if name in existing_names:
                messagebox.showerror("Duplicate Name",
                                     f"A template named '{name}' already exists.")
                return
        try:
            insert_or_update_template(name, "General", subject, body,
                                      creator_id=1,
                                      original_name=db_original_name_for_update)
            messagebox.showinfo("Saved",
                                f"Template '{name}' saved successfully.")
            self.refresh_template_dropdown()
            self.template_var.set(name)
            self.load_template(name, from_save_operation=True)
        except Exception as e:
            messagebox.showerror("Save Error",
                                 f"Failed to save template: {str(e)}")
            self.hint_label.configure(text="Error saving template.",
                                      foreground="red",
                                      style="RaisedSection.Hint.TLabel")

    def on_template_selected(self, event=None):
        selected = self.template_dropdown.get()
        if selected: self.load_template(selected)

    def enable_edit_mode(self):
        self._set_text_widget_state(self.subject_entry, tk.NORMAL)
        self._set_text_widget_state(self.body_text, tk.NORMAL)
        self.save_button.config(state="normal")
        self.edit_button.config(state="disabled")

        current_focus = self.focus_get()
        current_hint_text = self.hint_label.cget("text")
        msg_to_clear_when_body_focused = "Click on the Message body to enable tag selection."

        if current_focus == self.body_text:
            self.tag_dropdown.config(state="readonly")
            if current_hint_text == msg_to_clear_when_body_focused:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
        elif current_focus == self.subject_entry:
            self.tag_dropdown.config(state="disabled")
            if current_hint_text == msg_to_clear_when_body_focused:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
            self._update_tk_entry_border(self.subject_entry,
                                         FOCUS_BORDER_COLOR)
        else:
            if current_focus != self.name_entry and self.name_entry.cget(
                    'state') == 'readonly':
                self.subject_entry.focus()
            self.tag_dropdown.config(state="disabled")
            if current_hint_text == msg_to_clear_when_body_focused:
                self.hint_label.configure(text="",
                                          style="RaisedSection.Hint.TLabel")
            if self.focus_get() == self.subject_entry:
                self._update_tk_entry_border(self.subject_entry,
                                             FOCUS_BORDER_COLOR)
        self._update_save_as_button_state()

    def delete_template(self):
        name = self.template_var.get()
        if not name:
            messagebox.showwarning("No Selection",
                                   "No template selected to delete.")
            return
        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete template '{name}'? This cannot be undone."):
            return
        try:
            cursor = Database.get_cursor()
            cursor.execute("DELETE FROM dbo.templates WHERE name = ?", (name,))
            Database._Database__client.commit()
            messagebox.showinfo("Deleted", f"Template '{name}' deleted.")
            self.refresh_template_dropdown()
            self.clear_form()
            self.hint_label.configure(text=f"Template '{name}' deleted.",
                                      foreground=SUBTLE_TEXT_COLOR,
                                      style="RaisedSection.Hint.TLabel")
        except Exception as e:
            messagebox.showerror("Delete Error", f"Failed to delete: {str(e)}")
            self.hint_label.configure(text="Error deleting template.",
                                      foreground="red",
                                      style="RaisedSection.Hint.TLabel")


if __name__ == "__main__":
    class MainApplication(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.title("Food Pantry Notification System")
            self.geometry("950x750")
            apply_theme_styles(self)
            container = ttk.Frame(self, padding=10)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            self.frames = {}
            frame = TemplateCreatorGUI(container, self)
            self.frames[TemplateCreatorGUI] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(TemplateCreatorGUI)

        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

        def show_frame_by_name(self, frame_name_str):  # Dummy for _go_back
            print(f"Attempting to show frame: {frame_name_str}")


    class Database:
        _Database__client = type('MockClient', (), {
            'commit': lambda: print("DB Commit Mocked")})()

        @staticmethod
        def get_cursor():
            class MockCursor:
                def execute(self, query, params=None): pass

                def fetchall(self): return [
                    ("Event Reminder Tag", "event_name"),
                    ("Location Update Tag", "campus_location")]

            return MockCursor()


    mock_templates_db = {
        "Welcome Email": ("Welcome Email", "General", "Welcome to the Pantry!",
                          "Body of welcome... {{user_name}}"),
        "Event Announcement": ("Event Announcement", "Event",
                               "Upcoming Food Drive at {{campus_location}}",
                               "Join us for our event on {{event_date}}...")
    }


    def insert_or_update_template(name, cat, subj, body, creator_id,
                                  original_name):
        global mock_templates_db
        if original_name in mock_templates_db and original_name != name:
            del mock_templates_db[original_name]
        mock_templates_db[name] = (name, cat, subj, body)
        print(
            f"Mock DB: Saved/Updated Template - Name: '{name}', Original Name for lookup: '{original_name}'")


    def fetch_template_names():
        return list(mock_templates_db.keys())


    def fetch_template_by_name(name):
        return mock_templates_db.get(name)


    app = MainApplication()
    app.mainloop()