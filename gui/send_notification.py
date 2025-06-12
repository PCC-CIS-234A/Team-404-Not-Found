# Sayan Tajul
# CIS 234A Sprint Final Presentation
# sayan_send_notification
# Date: 06/06/2025

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# import configparser
# import os
import winsound
from PIL import Image, ImageTk
from tkhtmlview import HTMLLabel
# from html import unescape
import re
from logic.notification_logic import send_email_to_subscribers
from data.db_manager import Database
from theme import apply_theme_styles
# from theme import get_fonts

selected_files = []


class SendNotificationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        apply_theme_styles(self)
        self.active_widget = None

        # Main layout container
        wrapper = tk.Frame(self, bg="white")
        wrapper.pack(expand=True, padx=30, pady=30)

        wrapper.columnconfigure(0, weight=1)
        wrapper.columnconfigure(1, weight=0)

        # === LEFT side: Content ===
        content_frame = tk.Frame(wrapper, bg="white")
        content_frame.grid(row=0, column=0, sticky="n")

        # Home nav
        top_nav = tk.Frame(content_frame, bg="white")
        top_nav.pack(anchor="nw", pady=5, fill="x")
        tk.Button(top_nav, text="⌂ Home", bg="#008099", fg="white", command=self.go_home).pack(side="left")

        # Template dropdown
        template_names = Database.fetch_template_names()
        self.template_var = tk.StringVar(value="Select a Template")
        ttk.OptionMenu(content_frame, self.template_var, self.template_var.get(),
                       *template_names, command=self.load_selected_template).pack(pady=5)

        # Subject
        tk.Label(content_frame, text="Subject:", font=("Helvetica", 12, "bold"), bg="white").pack()
        self.subject_entry = tk.Entry(content_frame, width=70)
        self.subject_entry.pack(pady=5)

        # Tags
        tk.Label(content_frame, text="Tags:", font=("Helvetica", 12, "bold"), bg="white").pack()
        self.tag_var = tk.StringVar()
        tag_dropdown = ttk.Combobox(content_frame, textvariable=self.tag_var,
                                    values=Database.get_all_tags(), state="readonly")
        tag_dropdown.bind("<<ComboboxSelected>>", self.insert_tag)
        tag_dropdown.pack(pady=5)

        # Message
        tk.Label(content_frame, text="Message:", font=("Helvetica", 12, "bold"), bg="white").pack()
        self.message_box = tk.Text(content_frame, height=10, width=70)
        self.message_box.pack(pady=5)

        # Formatting
        format_frame = tk.Frame(content_frame, bg="white")
        format_frame.pack(pady=5)
        for tag in ["Bold", "Italic", "Underline"]:
            tk.Button(format_frame, text=tag, bg="#008099", fg="white",
                      command=lambda t=tag.lower()[0]: self.wrap_tag(t)).pack(side="left", padx=5)

        # Text Color
        color_frame = tk.Frame(content_frame, bg="white")
        color_frame.pack(pady=5)
        tk.Label(color_frame, text="Text Color:", bg="white").pack(side="left")
        self.color_var = tk.StringVar(value="red")
        ttk.Combobox(color_frame, textvariable=self.color_var,
                     values=["red", "blue", "green", "orange", "purple", "black"],
                     state="readonly", width=10).pack(side="left", padx=5)
        tk.Button(color_frame, text="Apply Color", bg="#008099", fg="white",
                  command=self.apply_color).pack(side="left")

        # Attachments List
        self.attachment_listbox = tk.Listbox(content_frame, height=3, width=70)
        self.attachment_listbox.pack(pady=10)

        btn_row = tk.Frame(content_frame, bg="white")
        btn_row.pack(pady=5)
        tk.Button(btn_row, text="Add Attachment", bg="#008099", fg="white",
                  command=self.add_attachment).pack(side="left", padx=5)
        tk.Button(btn_row, text="Remove Attachment", bg="#008099", fg="white",
                  command=self.remove_attachment).pack(side="left", padx=5)

        # Image Preview
        self.image_preview_frame = tk.Frame(content_frame, bg="white")
        self.image_preview_frame.pack(pady=10)

        # === RIGHT side: Sidebar Buttons ===
        side_buttons = tk.Frame(wrapper, bg="white")
        side_buttons.grid(row=0, column=1, sticky="n", padx=(40, 10))

        tk.Button(side_buttons, text="Send Notification", width=20, bg="#008099", fg="white",
                  command=self.send_notification).pack(pady=5)
        tk.Button(side_buttons, text="Add Photo", width=20, bg="#008099", fg="white",
                  command=self.add_attachment).pack(pady=5)
        tk.Button(side_buttons, text="Clear Form", width=20, bg="#008099", fg="white",
                  command=self.clear_fields).pack(pady=5)
        tk.Button(side_buttons, text="Exit", width=20, bg="#008099", fg="white",
                  command=self.quit).pack(pady=5)

    def go_home(self):
        if self.controller:
            from manager_welcome import ManagerWelcome
            self.controller.show_frame(ManagerWelcome)

    def load_selected_template(self, selected_template):
        if selected_template != "Select a Template":
            subject, message = Database.fetch_template_subject_message(selected_template)
            self.subject_entry.delete(0, tk.END)
            self.subject_entry.insert(0, subject)
            self.message_box.delete("1.0", tk.END)
            self.message_box.insert(tk.END, message)

    def insert_tag(self, event):
        tag = self.tag_var.get()
        self.message_box.insert(tk.INSERT, tag)

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

            clean_selected = re.sub(r'</?span[^>]*>', '', selected)

            self.message_box.delete(start, end)
            self.message_box.insert(start, f'<span style="color:{color}">{clean_selected}</span>')
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please highlight text to color.")

    def add_attachment(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            selected_files.append(filepath)
            self.attachment_listbox.insert(tk.END, filepath)
            self.update_image_preview()

    def remove_attachment(self):
        selected = self.attachment_listbox.curselection()
        for i in reversed(selected):
            selected_files.pop(i)
            self.attachment_listbox.delete(i)
        self.update_image_preview()

    def update_image_preview(self):
        for widget in self.image_preview_frame.winfo_children():
            widget.destroy()
        for filepath in selected_files[:6]:
            try:
                img = Image.open(filepath)
                img.thumbnail((100, 100))
                img = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.image_preview_frame, image=img)
                lbl.image = img
                lbl.pack(side="left", padx=5)
            except Exception as e:
                print(f"Preview Error: {e}")

    def clear_fields(self):
        self.subject_entry.delete(0, tk.END)
        self.message_box.delete("1.0", tk.END)
        self.attachment_listbox.delete(0, tk.END)
        selected_files.clear()
        self.update_image_preview()

    def show_review_popup(self, subject, message_html):
        review_window = tk.Toplevel(self)
        review_window.title("Review Notification")
        review_window.geometry("800x600")
        review_window.configure(bg="white")
        review_window.grab_set()

        tk.Label(
            review_window,
            text=f"Subject: {subject}",
            font=("Helvetica", 14, "bold"),
            fg="#005c6d",
            bg="white"
        ).pack(pady=(15, 5))

        message_html = message_html.replace('\n', '<br>')

        container = tk.Frame(review_window, bg="white")
        container.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        html_view = HTMLLabel(
            scrollable_frame,
            html=message_html,
            width=90,
            background="white",
            padx=10,
            pady=10
        )
        html_view.pack(fill="both", expand=True)

        # === Image Preview in Review ===
        preview_frame = tk.Frame(scrollable_frame, bg="white")
        preview_frame.pack(pady=10)

        review_images = []  # prevent garbage collection
        for filepath in selected_files[:6]:
            try:
                img = Image.open(filepath)
                img.thumbnail((120, 120))
                img_tk = ImageTk.PhotoImage(img)
                review_images.append(img_tk)
                img_label = tk.Label(preview_frame, image=img_tk, bg="white")
                img_label.pack(side="left", padx=5)
            except Exception as e:
                print(f"Review Preview Error: {e}")

        review_window.image_refs = review_images  # store references on window

        button_frame = tk.Frame(review_window, bg="white")
        button_frame.pack(pady=(5, 15))

        btn_style = {
            "bg": "#008099",
            "fg": "white",
            "font": ("Helvetica", 10, "bold"),
            "width": 12,
            "padx": 5,
            "pady": 4,
            "relief": "flat"
        }

        tk.Button(button_frame, text="Send",
                  command=lambda: [review_window.destroy(), self.finalize_send(subject, message_html)],
                  **btn_style).pack(pady=3)
        tk.Button(button_frame, text="Cancel",
                  command=review_window.destroy, **btn_style).pack(pady=3)

    def finalize_send(self, subject, message_html):
        subscribers = Database.get_subscribers()
        sender_id = Database.get_sender_id("Sarah Sam")
        Database.log_notification(subject, message_html, len(subscribers), sender_id, selected_files)
        send_email_to_subscribers(subject, message_html, subscribers, selected_files, {})
        messagebox.showinfo("Sent", f"Notification sent to {len(subscribers)} subscribers.")
        winsound.MessageBeep()
        self.clear_fields()

    def send_notification(self):
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", tk.END).strip()
        if not subject or not message:
            messagebox.showwarning("Missing Info", "Subject and Message are required.")
            return

        self.show_review_popup(subject, message)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Send Notification - PCC Free Food Pantry")
    root.geometry("1920x1080")
    app = SendNotificationPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
