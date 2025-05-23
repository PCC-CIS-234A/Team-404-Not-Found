# Sayan Tajul
# CIS 234A
# 05/19/2025
# Sprint 1 Final - Send Notification with Templates, Validation, File Attachments, and Review

# Modified version of original send_notification file
# Modified 5-23-2025 by RNixon


from tkinter import ttk
import configparser
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import winsound  # Windows built-in sound module
from logic.notification_logic import send_email_to_subscribers
from data.db_manager import Database
from theme import *

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


class SendNotificationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)

        main_page = ttk.Frame(self)
        main_page.pack(pady=5)

        PCCblue = "#008099"
        softcolorback = "#235578"
        Linkpccblue = "#1690b4"

        # GUI Components Below
        # Template Dropdown Menu from Santhil
        self.template_var = tk.StringVar(main_page)
        self.template_var.set("Select a Template")

        try:
            template_names = Database.fetch_template_names()
        except Exception as e:
            template_names = []
            messagebox.showerror("Template Error", f"Failed to fetch templates: {e}")

        template_menu = tk.OptionMenu(main_page, self.template_var, *template_names,
                                      command=lambda e: load_selected_template())
        template_menu.pack(pady=(10, 10))

        # Subject Label + Entry Box (change here for looks.)
        tk.Label(main_page, text="Subject:", font=("Helvetica", 12, "bold")).pack(pady=(5, 5))

        mainpagesubjectentry = tk.Entry(main_page, width=70)
        mainpagesubjectentry.pack(pady=(0, 10))
        mainpagesubjectentry.bind("<FocusIn>", lambda e: set_active_widget(mainpagesubjectentry))

        # Common Tags Dropdown
        tk.Label(main_page, text="Tags:", font=("Helvetica", 12, "bold")).pack(pady=(5, 5))

        common_tags = Database.get_all_tags()

        dropdown_frame = tk.Frame(main_page)
        dropdown_frame.pack(pady=(0, 10))
        selected_tag = tk.StringVar(main_page)
        selected_tag.set("")
        tag_dropdown = ttk.Combobox(dropdown_frame, textvariable=selected_tag, values=common_tags, state="readonly",
                                    width=30)
        tag_dropdown.pack(side=tk.LEFT, padx=10)

        insert_btn = tk.Button(dropdown_frame, text="Insert Tag", command=lambda: insert_tag(), bg=PCCblue, fg="white")
        insert_btn.pack(side=tk.LEFT)

        # Message Label + Text Box (Change here team 404 if needed)
        # Message Label
        tk.Label(main_page, text="Message:", font=("Helvetica", 12, "bold")).pack(pady=(5, 5))

        # Frame to hold text box and scrollbar
        message_frame = tk.Frame(main_page)
        message_frame.pack(pady=(0, 10))

        # Scrollbar for longer messages
        message_scrollbar = tk.Scrollbar(message_frame)
        message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text Box with scrollbar, at first I forgot about the scrollbar, but later I updated
        textmessage = tk.Text(message_frame, height=10, width=70, yscrollcommand=message_scrollbar.set)
        textmessage.pack(side=tk.LEFT, fill=tk.BOTH)
        textmessage.bind("<FocusIn>", lambda e: set_active_widget(textmessage))

        # Configure scrollbar to interact with text box
        message_scrollbar.config(command=textmessage.yview)

        # Formatting Buttons (Bold, Italic, Underline)
        format_buttons_frame = tk.Frame(main_page)
        format_buttons_frame.pack(pady=(5, 5))

        btn_bold = tk.Button(
            format_buttons_frame, text="Bold", command=lambda: wrap_selected_text("b"),
            bg=PCCblue, fg="white"
        )
        btn_bold.pack(side=tk.LEFT, padx=5)

        btn_italic = tk.Button(
            format_buttons_frame, text="Italic", command=lambda: wrap_selected_text("i"),
            bg=PCCblue, fg="white"
        )
        btn_italic.pack(side=tk.LEFT, padx=5)

        btn_underline = tk.Button(
            format_buttons_frame, text="Underline", command=lambda: wrap_selected_text("u"),
            bg=PCCblue, fg="white"
        )
        btn_underline.pack(side=tk.LEFT, padx=5)

        # Frame to align file buttons horizontally side by side
        file_buttons_frame = tk.Frame(main_page)
        file_buttons_frame.pack(pady=(5, 5))

        # Color Dropdown and Apply Button
        color_frame = tk.Frame(main_page)
        color_frame.pack(pady=(5, 5))

        tk.Label(color_frame, text="Text Color:").pack(side=tk.LEFT, padx=5)

        color_options = ["red", "blue", "green", "orange", "purple", "black"]
        selected_color = tk.StringVar(main_page)
        selected_color.set("red")

        color_dropdown = ttk.Combobox(color_frame, textvariable=selected_color, values=color_options, state="readonly",
                                      width=10)
        color_dropdown.pack(side=tk.LEFT, padx=5)

        btn_apply_color = tk.Button(
            color_frame, text="Apply Color", bg=PCCblue, fg="white",
            command=lambda: wrap_color_text(selected_color.get())
        )
        btn_apply_color.pack(side=tk.LEFT, padx=5)

        # Add Attachment button
        btn_add_attachment = tk.Button(
            file_buttons_frame, text="Add Attachments", bg=PCCblue, fg="white", command=lambda: adding_file()
        )
        btn_add_attachment.pack(side=tk.LEFT, padx=10, pady=5)

        # Remove Attachment button
        btn_remove_attachment = tk.Button(
            file_buttons_frame, text="Remove Attachments", bg=PCCblue, fg="white", command=lambda: removing_file()
        )
        btn_remove_attachment.pack(side=tk.LEFT, padx=10, pady=5)

        # Attached Files Listbox (shows files being attached)
        attached_files_listbox = tk.Listbox(main_page, width=70, height=2, bg="#e6f2ff")
        attached_files_listbox.pack(pady=(10, 10))

        # Frame to align Send and Cancel buttons horizontally side by side
        bottom_buttons_frame = tk.Frame(main_page)
        bottom_buttons_frame.pack(pady=(15, 20))

        # Send Notification Button
        btnsend = tk.Button(
            bottom_buttons_frame,
            text="Send Notification",
            font=("Helvetica", 11, "bold"),
            padx=12,
            pady=6,
            command=lambda: send_notification()
        )
        btnsend.pack(side=tk.LEFT, padx=10)

        # Cancel Button
        buttoncancel = tk.Button(
            bottom_buttons_frame,
            text="Cancel",
            bg=PCCblue,
            fg="white",
            font=("Helvetica", 11, "bold"),
            padx=12,
            pady=6,
            command=lambda: cancel_fields()
        )
        buttoncancel.pack(side=tk.LEFT, padx=10)

        def set_active_widget(widget):
            global active_widget
            active_widget = widget

        def wrap_selected_text(tag):
            try:
                start = textmessage.index(tk.SEL_FIRST)
                end = textmessage.index(tk.SEL_LAST)
                selected = textmessage.get(start, end)
                wrapped = f"<{tag}>{selected}</{tag}>"
                textmessage.delete(start, end)
                textmessage.insert(start, wrapped)
            except tk.TclError:
                messagebox.showwarning("No Selection", "Please highlight some text in the message box to format.")

        def wrap_color_text(color):
            try:
                start = textmessage.index(tk.SEL_FIRST)
                end = textmessage.index(tk.SEL_LAST)
                selected = textmessage.get(start, end)
                wrapped = f'<span style="color:{color}">{selected}</span>'
                textmessage.delete(start, end)
                textmessage.insert(start, wrapped)
            except tk.TclError:
                messagebox.showwarning("No Selection", "Please highlight some text in the message box to apply color.")

        def insert_tag():
            tag = selected_tag.get()
            if tag and active_widget:
                if isinstance(active_widget, tk.Entry):
                    pos = active_widget.index(tk.INSERT)  # Get current cursor position
                    active_widget.insert(pos, tag)
                elif isinstance(active_widget, tk.Text):
                    active_widget.insert(tk.INSERT, tag)
                else:
                    messagebox.showwarning("No Target", "Click on the Subject or Message box before inserting a tag.")

        # Cancel/Clear Functions as Professor recommneded (Currently Cancel Button)
        def cancel_fields():
            # Clearing subject and message fields
            mainpagesubjectentry.delete(0, tk.END)
            textmessage.delete("1.0", tk.END)

            # Clearing the attachments listbox
            attached_files_listbox.delete(0, tk.END)

            # Clearing the internal attachments list
            selected_files.clear()

        def send_notification():
            subject = mainpagesubjectentry.get().strip()
            message = textmessage.get("1.0", tk.END).strip()

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
                Database.log_notification(subject, message, number_of_recipients, sender_id, selected_files)

                if not sender_id:
                    messagebox.showerror("Sender Error", f"Sender '{sender_username}' not found. Check username.")
                    return

                send_email_to_subscribers(subject, message, subscribers, selected_files, {})

                messagebox.showinfo("Success", f"Notification sent successfully to {number_of_recipients} subscribers.")
                winsound.MessageBeep()
                cancel_fields()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred:\n{e}")

        def adding_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                selected_files.append(file_path)
                attached_files_listbox.insert(tk.END, file_path)  # Insert into Listbox

        def removing_file():
            selected_indices = attached_files_listbox.curselection()
            if selected_indices:
                for index in reversed(selected_indices):
                    attached_files_listbox.delete(index)
                    selected_files.pop(index)
            else:
                messagebox.showwarning("No Selection", "Please select a file to remove.")

        # Loading Template Data When Selected
        def load_selected_template(*args):
            selected_template = self.template_var.get()
            if selected_template != "Select a Template":
                try:
                    subject, message = Database.fetch_template_by_name(selected_template)
                    mainpagesubjectentry.delete(0, tk.END)
                    mainpagesubjectentry.insert(0, subject)
                    textmessage.delete("1.0", tk.END)
                    textmessage.insert(tk.END, message)
                except Exception as e:
                    messagebox.showerror("Template Load Error", f"Could not load template:\n{e}")
