# Sayan Tajul
# CIS 234A
# 04/21/2025
# Sprint 1 Part 2 - Send Notification with Templates, Validation, File Attachments, and Review

# Enable High DPI Awareness. High DPI awareness helps produce sharper scaling. This is particularly useful for Zoom
# presentations.
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Imports for my Send Notification
import pyodbc
import tkinter as tk
from tkinter import messagebox, filedialog
from template_logic import fetch_template_names, fetch_template_by_name  # Template functions

# Connecting to our Database in SQL Server
def connecttoourdb():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cisdbss.pcc.edu;"
        "DATABASE=CIS234A_404 Team Not Found;"
        "UID=CIS234A_404 Team Not Found;"
        "PWD=NoErrors&2"
    )
    return pyodbc.connect(conn_str)


# Building the primary notification for my Send Function
def NotificationPage():
    subject = mainpagesubjectentry.get().strip()
    message = textmessage.get("1.0", tk.END).strip()

    # Field Required Validation
    if not subject or not message:
        messagebox.showwarning("Missing Information", "Subject and Message are required.")
        return

    # This function needs minimum length checking.
    if len(subject) < 5:
        messagebox.showwarning("Validation Error", "Subject must be at least 5 characters.")
        return
    if len(message) < 10:
        messagebox.showwarning("Validation Error", "Message must be at least 10 characters.")
        return

    # Every notification requires examination before dispatch.
    confirm = messagebox.askyesno("Review Notification",
                                  f"Subject:\n{subject}\n\nMessage:\n{message}\n\nDo you want to send it?")
    if not confirm:
        return

    try:
        conn = connecttoourdb()
        cursor = conn.cursor()

        # Creating table if it doesn't exist in our SQL Database
        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM sysobjects 
                WHERE name='notifications' AND xtype='U'
            )
            CREATE TABLE notifications (
                id INT IDENTITY(1,1) PRIMARY KEY,
                subject NVARCHAR(255) NOT NULL,
                message NVARCHAR(MAX) NOT NULL,
                date_sent DATETIME DEFAULT GETDATE()
            )
        """)
        conn.commit()

        # Data notification happens as the table changes.
        cursor.execute("""
            INSERT INTO notifications (subject, message) VALUES (?, ?)
        """, (subject, message))
        conn.commit()

        messagebox.showinfo("Success", "Notification sent and saved to SQL Server.")

    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")
    finally:
        conn.close()


# Cancel/Clear Functions as Professor recommneded
def cancelfieldsFun():
    mainpagesubjectentry.delete(0, tk.END)
    textmessage.delete("1.0", tk.END)


# Add/Remove Files Functions as Professors recommneded
selected_files = []


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

# Load Template Data When Selected
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
window_width = 1400
window_height = 1000  # Increased height slightly to fit more buttons
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
    font=("Helvetica", 20, "bold"),
    bg=mainpage["bg"],
    fg=softcolorback
).pack(pady=(5, 5))

mainpagesubjectentry = tk.Entry(mainpage, width=70)
mainpagesubjectentry.pack(pady=(0, 10))

# Message Label + Text Box (Change here team 404 if needed)
tk.Label(
    mainpage,
    text="Message:",
    font=("Helvetica", 12, "bold"),
    bg=mainpage["bg"],
    fg=softcolorback
).pack(pady=(5, 5))

textmessage = tk.Text(mainpage, height=12, width=70)
textmessage.pack(pady=(0, 10))

# File Buttons for adding files
btn_addingfileFun = tk.Button(mainpage, text="Add File", bg=PCCblue, fg="white", command=addingfileFun)
btn_addingfileFun.pack(pady=(5, 2))

btn_removingfileFun = tk.Button(mainpage, text="Remove File", bg=PCCblue, fg="white", command=removingfileFun)
btn_removingfileFun.pack(pady=(2, 10))

# Attached Files Listbox (shows files being attached)
attached_files_listbox = tk.Listbox(mainpage, width=100, height=5, bg="#e6f2ff")
attached_files_listbox.pack(pady=(10, 10))

# Send and Cancel Buttons as recommended
btnsend = tk.Button(
    mainpage,
    text="Send Notification",
    bg=Linkpccblue,
    fg="white",
    font=("Helvetica", 11, "bold"),
    padx=12,
    pady=6,
    command=NotificationPage
)
btnsend.pack(pady=10)

#Cancel Button as recommended.
buttoncancel = tk.Button(
    mainpage,
    text="Cancel",
    bg="red",
    fg="white",
    font=("Helvetica", 11, "bold"),
    padx=12,
    pady=6,
    command=cancelfieldsFun
)
buttoncancel.pack(pady=(5, 20))

# Main GUI Loop
mainpage.mainloop()
