# Sayan Tajul
# CIS 234A
# 05/19/2025
# Sprint 1 Final - Send Notification with Templates, Validation, File Attachments, and Review

# Modified version of send_notification.py
# Modified 5-22-2025 by RNixon

# CURRENTLY DOES NOT WORK!!

from tkinter import ttk
import configparser
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import winsound  # Windows built-in sound module
from logic.notification_logic import send_email_to_subscribers
from data.db_manager import Database
from theme import *


class SendNotifPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        mainpage = ttk.Frame(self)
        mainpage.pack(pady=20)

        PCCblue = "#008099"
        softcolorback = "#235578"
        Linkpccblue = "#1690b4"

        # GUI Components Below
        # Template Dropdown Menu from Santhil
        template_var = tk.StringVar(mainpage)
        template_var.set("Select a Template")

        try:
            template_names = Database.fetch_template_names()
        except Exception as e:
            template_names = []
            messagebox.showerror("Template Error", f"Failed to fetch templates: {e}")

        template_menu = tk.OptionMenu(mainpage, template_var, *template_names, command=self.load_selected_template)
        template_menu.pack(pady=(10, 10))

        # Subject Label + Entry Box (change here for looks.)
        tk.Label(
            mainpage,
            text="Subject:",
            font=("Helvetica", 30, "bold"),
        ).pack(pady=(5, 5))

        mainpagesubjectentry = tk.Entry(mainpage, width=70)
        mainpagesubjectentry.pack(pady=(0, 10))
        mainpagesubjectentry.bind("<FocusIn>", lambda e: self.set_active_widget(mainpagesubjectentry))

        # Common Tags Dropdown
        tk.Label(
            mainpage,
            text="TAGS",
            font=("Helvetica", 12, "bold"),
        ).pack(pady=(5, 5))

        common_tags = Database.get_all_tags()

        dropdown_frame = tk.Frame(mainpage)
        dropdown_frame.pack(pady=(0, 10))
        selected_tag = tk.StringVar(mainpage)
        selected_tag.set("")
        tag_dropdown = ttk.Combobox(dropdown_frame, textvariable=selected_tag, values=common_tags, state="readonly",
                                    width=30)
        tag_dropdown.pack(side=tk.LEFT, padx=10)

    # Defining my attachments list here (GLOBAL SCOPE)
    selected_files = []

    # Track which field is active (subject or message)
    active_widget = None  # To store last focused widget

    # Load email credentials from config.ini
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)

    SENDER_EMAIL = config.get('EMAIL', 'sender_email')
    APP_PASSWORD = config.get('EMAIL', 'app_password')
    print("Loaded INI Sections:", config.sections())


    def send_notification(self):
        subject = self.mainpagesubjectentry.get().strip()
        message = self.textmessage.get("1.0", tk.END).strip()

        sender_username = "Sarah Sam"  # Manager username from your DB

        # Validating subject and message input here
        if not subject or not message:
            messagebox.showwarning("Missing Information", "Subject and Message are required.")
            return
        if len(subject) < 5 or len(message) < 10:
            messagebox.showwarning("Validation Error", "Subject must be at least 5 characters; message at least 10.")
            return

        # Confirming sending notification
        confirm = messagebox.askyesno("Review Notification",
                                      f"Subject:\n{subject}\n\nMessage:\n{message}\n\nDo you want to send it?")
        if not confirm:
            return

        try:
            subscribers = Database.get_subscribers()
            number_of_recipients = len(subscribers)
            sender_id = Database.get_sender_id(sender_username)
            Database.log_notification(subject, message, number_of_recipients, sender_id, self.selected_files)

            if not sender_id:
                messagebox.showerror("Sender Error", f"Sender '{sender_username}' not found. Check username.")
                return

            send_email_to_subscribers(subject, message, subscribers, self.selected_files, {})

            messagebox.showinfo("Success", f"Notification sent successfully to {number_of_recipients} subscribers.")
            winsound.MessageBeep()
            self.cancel_fields()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


    def set_active_widget(self, widget):
        global active_widget
        active_widget = widget

    # Cancel/Clear Functions as Professor recommneded (Currently Cancel Button)
    def cancel_fields(self):
        # Clearing subject and message fields
        self.mainpagesubjectentry.delete(0, tk.END)
        self.textmessage.delete("1.0", tk.END)

        # Clearing the attachments listbox
        self.attached_files_listbox.delete(0, tk.END)

        # Clearing the internal attachments list
        self.selected_files.clear()

    def adding_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_files.append(file_path)
            self.attached_files_listbox.insert(tk.END, file_path)  # Insert into Listbox

    def removing_file(self):
        selected_indices = self.attached_files_listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                self.attached_files_listbox.delete(index)
                self.selected_files.pop(index)
        else:
            messagebox.showwarning("No Selection", "Please select a file to remove.")

    # Loading Template Data When Selected
    def load_selected_template(self, *args):
        selected_template = self.template_var.get()
        if selected_template != "Select a Template":
            try:
                subject, message = Database.fetch_template_by_name(selected_template)
                self.mainpagesubjectentry.delete(0, tk.END)
                self.mainpagesubjectentry.insert(0, subject)
                self.textmessage.delete("1.0", tk.END)
                self.textmessage.insert(tk.END, message)
            except Exception as e:
                messagebox.showerror("Template Load Error", f"Could not load template:\n{e}")


