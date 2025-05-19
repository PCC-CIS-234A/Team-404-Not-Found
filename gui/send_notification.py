# Sayan Tajul
# CIS 234A
# 05/05/2025
# Sprint 1 Final - Send Notification with Templates, Validation, File Attachments, and Review

# Enabling High DPI Awareness. High DPI awareness helps produce sharper scaling. This is particularly useful for Zoom
# presentations.
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Imports for my Send Notification
import datetime
import configparser
import tkinter as tk
from tkinter import messagebox, filedialog
from logic.template_logic import fetch_template_names, fetch_template_by_name
import os
import winsound  # Windows built-in sound module
from logic.notification_logic import send_email_to_subscribers, process_tags
from tkinter import simpledialog
from data.database_access import connecttoourdb
from logic.tag_logic import prompt_for_tags
from logic.template_logic import fetch_template_names, fetch_template_by_name

# Defining my attachments list here (GLOBAL SCOPE)
selected_files = []

# Load email credentials from config.ini
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

SENDER_EMAIL = config.get('EMAIL', 'sender_email')
APP_PASSWORD = config.get('EMAIL', 'app_password')
print("Loaded INI Sections:", config.sections())

# Updated notification sending logic with logging here
def NotificationPage():
    subject = mainpagesubjectentry.get().strip()
    message = textmessage.get("1.0", tk.END).strip()

    # Prompt for dynamic tags from template content
    full_template_text = subject + "\n" + message
    user_filled_tags = prompt_for_tags(full_template_text)
    if user_filled_tags is None:
        return  # User canceled input

    # Replace tags with user values
    subject = process_tags(subject, user_filled_tags)
    message = process_tags(message, user_filled_tags)

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

    try: # Had some issues but currently fix hopefully
        conn = connecttoourdb()
        cursor = conn.cursor()

        # Debug: Print subscribers for double checking
        cursor.execute("SELECT first_name, email FROM dbo.users WHERE role = 'subscriber'")
        subscribers = [{"first_name": row[0], "email": row[1]} for row in cursor.fetchall()]

        print("DEBUG: Subscribers fetched:", subscribers)

        number_of_recipients = len(subscribers)
        print("DEBUG: Number of subscribers:", number_of_recipients)

        # Debug: Verify sender_username (double checking)
        sender_username = "Sarah Sam"
        print("DEBUG: Sender username:", sender_username)

        # Debug: Fetching sender ID to make sure
        cursor.execute("SELECT user_id FROM dbo.users WHERE username = ?", (sender_username,))
        sender_result = cursor.fetchone()
        print("DEBUG: Sender query result:", sender_result)

        sender_id = sender_result[0] if sender_result else None

        if not sender_id:
            messagebox.showerror("Sender Error", f"Sender '{sender_username}' not found. Check username.")
            return

        # Sending emails to subscribers
        send_email_to_subscribers(subject, message, subscribers, selected_files, user_filled_tags)

        # Inserting notification log into SQL (Team 404 Not Found)
        attachment_names = ", ".join([os.path.basename(file) for file in selected_files])
        cursor.execute("""
            INSERT INTO dbo.notifications (subject, message, date_sent, num_subscribers, sender_id, attachment_names)
            VALUES (?, ?, GETDATE(), ?, ?, ?)
        """, (subject, message, number_of_recipients, sender_id, attachment_names))

        conn.commit()

        messagebox.showinfo("Success", f"Notification sent successfully to {number_of_recipients} subscribers.")
        winsound.MessageBeep()
        cancelfieldsFun()  # Reset the form after success

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
    finally:
        conn.close()

# Cancel/Clear Functions as Professor recommneded (Currently Cancel Button)
def cancelfieldsFun():
    # Clearing subject and message fields
    mainpagesubjectentry.delete(0, tk.END)
    textmessage.delete("1.0", tk.END)

    # Clearing the attachments listbox
    attached_files_listbox.delete(0, tk.END)

    # Clearing the internal attachments list
    selected_files.clear()

def addingfileFun():
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_files.append(file_path)
        attached_files_listbox.insert(tk.END, file_path)  # Insert into Listbox

def removingfileFun():
    selected_indices = attached_files_listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            attached_files_listbox.delete(index)
            selected_files.pop(index)
    else:
        messagebox.showwarning("No Selection", "Please select a file to remove.")

# Loading Template Data When Selected
def load_selected_template(*args):
    selected_template = template_var.get()
    if selected_template != "Select a Template":
        try:
            subject, message = fetch_template_by_name(selected_template)
            mainpagesubjectentry.delete(0, tk.END)
            mainpagesubjectentry.insert(0, subject)
            textmessage.delete("1.0", tk.END)
            textmessage.insert(tk.END, message)
        except Exception as e:
            messagebox.showerror("Template Load Error", f"Could not load template:\n{e}")


# GUI Setup
mainpage = tk.Tk()
mainpage.title("Send Notification")

# Window Size and Center (Change if Needed Team 404 not found)
window_width = 1600
window_height = 1000  # Increased height slightly to fit more buttons and make it bigger
screen_width = mainpage.winfo_screenwidth()
screen_height = mainpage.winfo_screenheight()
x_coord = int((screen_width / 2) - (window_width / 2))
y_coord = int((screen_height / 2) - (window_height / 2))
mainpage.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")
mainpage.configure(bg="#f5f5f5")  # Light background

# PCC Style Colors (Picked by our team)
PCCblue = "#008099"
softcolorback = "#235578"
Linkpccblue = "#1690b4"

# GUI Components Below
# Template Dropdown Menu from Santhil
template_var = tk.StringVar(mainpage)
template_var.set("Select a Template")

try:
    template_names = fetch_template_names()
except Exception as e:
    template_names = []
    messagebox.showerror("Template Error", f"Failed to fetch templates: {e}")

template_menu = tk.OptionMenu(mainpage, template_var, *template_names, command=load_selected_template)
template_menu.pack(pady=(10, 10))

# Subject Label + Entry Box (change here for looks.)
tk.Label(
    mainpage,
    text="Subject:",
    font=("Helvetica", 30, "bold"),
    bg=mainpage["bg"],
    fg=softcolorback
).pack(pady=(5, 5))

mainpagesubjectentry = tk.Entry(mainpage, width=70)
mainpagesubjectentry.pack(pady=(0, 10))

# Message Label + Text Box (Change here team 404 if needed)
# Message Label
tk.Label(
    mainpage,
    text="Message:",
    font=("Helvetica", 12, "bold"),
    bg=mainpage["bg"],
    fg=softcolorback
).pack(pady=(5, 5))

# Frame to hold text box and scrollbar
message_frame = tk.Frame(mainpage, bg=mainpage["bg"])
message_frame.pack(pady=(0, 10))

# Scrollbar for longer messages
message_scrollbar = tk.Scrollbar(message_frame)
message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text Box with scrollbar, at first I forgot about the scrollbar but later I updated
textmessage = tk.Text(
    message_frame,
    height=12,
    width=70,
    yscrollcommand=message_scrollbar.set
)
textmessage.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure scrollbar to interact with text box
message_scrollbar.config(command=textmessage.yview)

# Frame to align file buttons horizontally side by side
file_buttons_frame = tk.Frame(mainpage, bg=mainpage["bg"])
file_buttons_frame.pack(pady=(5, 5))

# Add Attachment button
btn_add_attachment = tk.Button(
    file_buttons_frame, text="Add Attachments", bg=PCCblue, fg="white", command=addingfileFun
)
btn_add_attachment.pack(side=tk.LEFT, padx=10, pady=5)

# Remove Attachment button
btn_remove_attachment = tk.Button(
    file_buttons_frame, text="Remove Attachments", bg=PCCblue, fg="white", command=removingfileFun
)
btn_remove_attachment.pack(side=tk.LEFT, padx=10, pady=5)

# Attached Files Listbox (shows files being attached)
attached_files_listbox = tk.Listbox(mainpage, width=100, height=5, bg="#e6f2ff")
attached_files_listbox.pack(pady=(10, 10))

# Frame to align Send and Cancel buttons horizontally side by side
bottom_buttons_frame = tk.Frame(mainpage, bg=mainpage["bg"])
bottom_buttons_frame.pack(pady=(15, 20))

# Send Notification Button
btnsend = tk.Button(
    bottom_buttons_frame,
    text="Send Notification",
    bg=Linkpccblue,
    fg="white",
    font=("Helvetica", 11, "bold"),
    padx=12,
    pady=6,
    command=NotificationPage
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
    command=cancelfieldsFun
)
buttoncancel.pack(side=tk.LEFT, padx=10)

# Main GUI Loop
mainpage.mainloop()
