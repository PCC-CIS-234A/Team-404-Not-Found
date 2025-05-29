"""
Author: Sayan Tajul
Created: 05/20/2025
Last Modified: 05/28/2025
File: send_notification.py
Course: CIS 234A – PCC Sprint 2 Part 2

Description:
This module implements the "Send Notification" feature for the Food Insecurity Notification System.
It provides a user-friendly Tkinter GUI for composing and sending email notifications to pantry subscribers.

Key Features:
- Dropdown to select existing templates (auto-fills subject and message).
- Entry fields for subject, rich-text formatted message, and dynamic tag insertion.
- Rich text options include: bold, italic, underline, and color styling.
- Attachment handling: add, preview, and remove attachments.
- Confirmation popup before sending.
- Logs notifications in the database with subscriber count and sender ID.

Implements:
- PEP 8-compliant formatting
- N-Tier architecture with separation of GUI, logic, and data layers
- High DPI scaling, PCC-themed colors, and font styling

Note:
This file is part of the Sprint 2 – Part 2 development, improving upon previous Sprint 1 functionality
by adding formatting tools, enhanced template handling, and backend integration.
"""

# send_notification.py (Refactored GUI - Sprint 2 with PCC Colors, Fonts, High DPI, and Aligned Labels)
# Impprots
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import os
import winsound

from logic.notification_logic import send_email_to_subscribers
from data.db_manager import Database
from theme import apply_theme_styles, get_fonts

# Enable High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Global state
selected_files = []
active_widget = None

# Load credentials
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
SENDER_EMAIL = config.get('EMAIL', 'sender_email')
APP_PASSWORD = config.get('EMAIL', 'app_password')

# PCC Colors
PCC_BLUE = "#008099"
PCC_LIGHT_BLUE = "#e6f2ff"
PCC_FONT = ("Helvetica", 11)
PCC_LABEL_FONT = ("Helvetica", 12, "bold")


class SendNotificationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg="white")
        apply_theme_styles(self)

        # Layout containers
        top_nav = tk.Frame(self, bg="white")
        top_nav.pack(anchor="nw", padx=10, pady=5, fill="x")

        content_wrapper = tk.Frame(self, bg="white")
        content_wrapper.pack(fill="both", expand=True)

        main_content = tk.Frame(content_wrapper, bg="white")
        main_content.pack(side="left", padx=40, pady=20, fill="both", expand=True)

        side_buttons = tk.Frame(content_wrapper, bg="white")
        side_buttons.pack(side="left", padx=30, pady=80, anchor="n")

        # === Top Nav Buttons ===
        tk.Button(top_nav, text="⌂ Home", font=PCC_FONT, bg=PCC_BLUE, fg="white", command=self.go_home).pack(side="left", padx=(0, 10))
        tk.Button(top_nav, text="← Back", font=PCC_FONT, bg=PCC_BLUE, fg="white", command=self.go_back).pack(side="left")

        # === Template Dropdown ===
        template_frame = tk.Frame(main_content, bg="white")
        template_frame.pack(anchor="center", pady=(10, 0))
        tk.Label(template_frame, text="Template:", font=PCC_LABEL_FONT, bg="white").pack(anchor="center")
        self.template_var = tk.StringVar(value="Select a Template")
        try:
            template_names = Database.fetch_template_names()
        except Exception as e:
            messagebox.showerror("Template Error", str(e))
            template_names = []
        ttk.OptionMenu(template_frame, self.template_var, self.template_var.get(), *template_names, command=self.load_selected_template).pack()

        # === Subject ===
        subject_frame = tk.Frame(main_content, bg="white")
        subject_frame.pack(anchor="center", pady=(10, 10))
        tk.Label(subject_frame, text="Subject:", font=PCC_LABEL_FONT, bg="white").pack(anchor="center")
        self.subject_entry = tk.Entry(subject_frame, width=70, font=PCC_FONT, relief="solid", bd=1)
        self.subject_entry.pack(ipady=4)
        self.subject_entry.bind("<FocusIn>", lambda e: self.set_active_widget(self.subject_entry))

        # === Tags ===
        tags_frame = tk.Frame(main_content, bg="white")
        tags_frame.pack(anchor="center", pady=(10, 10))
        tk.Label(tags_frame, text="Tags:", font=PCC_LABEL_FONT, bg="white").pack(side="left", padx=(0, 10))
        self.selected_tag = tk.StringVar()
        common_tags = Database.get_all_tags()
        ttk.Combobox(tags_frame, textvariable=self.selected_tag, values=common_tags, state="readonly", width=30).pack(side="left")
        tk.Button(tags_frame, text="Insert Tag", font=PCC_FONT, bg=PCC_BLUE, fg="white", command=self.insert_tag).pack(side="left", padx=(10, 0))

        # === Message ===
        message_frame = tk.Frame(main_content, bg="white")
        message_frame.pack(anchor="center", pady=(10, 0))
        tk.Label(message_frame, text="Message:", font=PCC_LABEL_FONT, bg="white").pack(anchor="center")
        self.message_box = tk.Text(message_frame, height=12, width=70, font=PCC_FONT, relief="solid", bd=1)
        self.message_box.pack()
        scrollbar = tk.Scrollbar(message_frame, command=self.message_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.message_box.config(yscrollcommand=scrollbar.set)
        self.message_box.bind("<FocusIn>", lambda e: self.set_active_widget(self.message_box))

        # === Rich Text Buttons ===
        format_frame = tk.Frame(main_content, bg="white")
        format_frame.pack(anchor="center", pady=5)
        for tag in ["Bold", "Italic", "Underline"]:
            tk.Button(format_frame, text=tag, font=PCC_FONT, bg=PCC_BLUE, fg="white",
                      command=lambda t=tag.lower()[0]: self.wrap_tag(t)).pack(side="left", padx=5)

        # === Text Color ===
        color_frame = tk.Frame(main_content, bg="white")
        color_frame.pack(anchor="center", pady=5)
        tk.Label(color_frame, text="Text Color:", font=PCC_FONT, bg="white").pack(side="left")
        self.color_var = tk.StringVar(value="red")
        ttk.Combobox(color_frame, textvariable=self.color_var, values=["red", "blue", "green", "orange", "purple", "black"], state="readonly", width=10).pack(side="left", padx=5)
        tk.Button(color_frame, text="Apply Color", font=PCC_FONT, bg=PCC_BLUE, fg="white", command=self.apply_color).pack(side="left")

        # === Attachment Section ===
        attachment_frame = tk.Frame(main_content, bg="white")
        attachment_frame.pack(anchor="center", pady=(10, 2))
        self.attachment_listbox = tk.Listbox(attachment_frame, height=3, width=70, font=PCC_FONT, bg=PCC_LIGHT_BLUE)
        self.attachment_listbox.pack()
        tk.Button(attachment_frame, text="Add Attachments", font=PCC_FONT, bg=PCC_BLUE, fg="white", command=self.add_attachment).pack(pady=2)
        tk.Button(attachment_frame, text="Remove Attachments", font=PCC_FONT, bg=PCC_BLUE, fg="white", command=self.remove_attachment).pack(pady=2)

        # === Side Buttons (Now moved closer to form) ===
        for label, command in [
            ("Send Notification", self.send_notification),
            ("Add Image", self.add_attachment),
            ("Clear Form", self.clear_fields),
            ("Exit", self.quit)
        ]:
            tk.Button(side_buttons, text=label, font=PCC_FONT, bg=PCC_BLUE, fg="white", width=18, command=command).pack(pady=5)

    def go_home(self):
        print("Go to Welcome Page")

    def go_back(self):
        print("Go to Template Creation Page")

    def set_active_widget(self, widget):
        global active_widget
        active_widget = widget

    def insert_tag(self):
        tag = self.selected_tag.get()
        if tag and active_widget:
            if isinstance(active_widget, tk.Entry):
                active_widget.insert(active_widget.index(tk.INSERT), tag)
            elif isinstance(active_widget, tk.Text):
                active_widget.insert(tk.INSERT, tag)

    def wrap_tag(self, tag):
        try:
            start = self.message_box.index(tk.SEL_FIRST)
            end = self.message_box.index(tk.SEL_LAST)
            selected = self.message_box.get(start, end)
            self.message_box.delete(start, end)
            self.message_box.insert(start, f"<{tag}>{selected}</{tag}>")
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please highlight text to format.")

    def apply_color(self):
        try:
            start = self.message_box.index(tk.SEL_FIRST)
            end = self.message_box.index(tk.SEL_LAST)
            selected = self.message_box.get(start, end)
            color = self.color_var.get()
            self.message_box.delete(start, end)
            self.message_box.insert(start, f'<span style="color:{color}">{selected}</span>')
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please highlight text to color.")

    def add_attachment(self):
        path = filedialog.askopenfilename()
        if path:
            selected_files.append(path)
            self.attachment_listbox.insert(tk.END, path)

    def remove_attachment(self):
        selection = self.attachment_listbox.curselection()
        for i in reversed(selection):
            selected_files.pop(i)
            self.attachment_listbox.delete(i)

    def clear_fields(self):
        self.subject_entry.delete(0, tk.END)
        self.message_box.delete("1.0", tk.END)
        self.attachment_listbox.delete(0, tk.END)
        selected_files.clear()

    def load_selected_template(self, selected_template):
        if selected_template and selected_template != "Select a Template":
            try:
                subject, message = Database.fetch_template_subject_message(selected_template)
                self.subject_entry.delete(0, tk.END)
                self.subject_entry.insert(0, subject)
                self.message_box.delete("1.0", tk.END)
                self.message_box.insert(tk.END, message)
            except Exception as e:
                messagebox.showerror("Template Load Error", f"Could not load template:\n{e}")

    def send_notification(self):
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", tk.END).strip()

        if not subject or not message:
            messagebox.showwarning("Missing Info", "Subject and Message are required.")
            return

        if not messagebox.askyesno("Confirm", f"Subject: {subject}\n\nMessage Preview:\n{message[:500]}...\n\nSend this message?"):
            return

        try:
            subscribers = Database.get_subscribers()
            sender_id = Database.get_sender_id("Sarah Sam")
            Database.log_notification(subject, message, len(subscribers), sender_id, selected_files)
            send_email_to_subscribers(subject, message, subscribers, selected_files, {})
            messagebox.showinfo("Sent", f"Notification sent to {len(subscribers)} subscribers.")
            winsound.MessageBeep()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Send Notification")
    root.geometry("1920x1080")
    SendNotificationPage(root, None).pack(fill="both", expand=True)
    root.mainloop()
