import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import os
import winsound
from PIL import Image, ImageTk
from logic.notification_logic import send_email_to_subscribers
from data.db_manager import Database
from theme import apply_theme_styles, get_fonts

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
            self.message_box.delete(start, end)
            self.message_box.insert(start, f'<span style="color:{color}">{selected}</span>')
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

    def send_notification(self):
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", tk.END).strip()
        if not subject or not message:
            messagebox.showwarning("Missing Info", "Subject and Message are required.")
            return
        confirm = messagebox.askyesno("Review", f"Subject: {subject}\n\nPreview:\n{message}")
        if not confirm:
            return
        subscribers = Database.get_subscribers()
        sender_id = Database.get_sender_id("Sarah Sam")
        Database.log_notification(subject, message, len(subscribers), sender_id, selected_files)
        send_email_to_subscribers(subject, message, subscribers, selected_files, {})
        messagebox.showinfo("Sent", f"Notification sent to {len(subscribers)} subscribers.")
        winsound.MessageBeep()
        self.clear_fields()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Send Notification - PCC Free Food Pantry")
    root.geometry("1920x1080")
    app = SendNotificationPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
