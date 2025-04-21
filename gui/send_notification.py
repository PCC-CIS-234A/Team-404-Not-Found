# Sayan Tajul
# CIS 234A
# 04/18/2025
# Working on story 2 Send Notification

import tkinter as tk
from tkinter import messagebox


def NotificationPage ():
    """
This function runs when I hit the send button.
It makes sure the fields aren't blank and then shows a message
pretending it was sent to 5 people (for now!).
Later, I’ll connect this to real data.
    """
    subject = mainpagesubjectentry.get().strip()
    message = textmessage.get("1.0", tk.END).strip()

    if not subject or not message:
        messagebox.showwarning("Missing Information", "Subject and Message are required.")
        return

    #  A (Dummy) practice run copies delivery to receivers.
    countofrecientt = 5
    messagebox.showinfo("Success", f"Notification sent to {countofrecientt} recipients.")


# Making the primary screen area.
mainpage = tk.Tk()
mainpage.title("Send Notification")

# GUI SIZE: Change these values to change how big the interface is.
# If needed by my Classmates
window_width = 700    # ← adjust width here
window_height = 500   # ← adjust height here

# Putting the window in the middle.
screen_width = mainpage.winfo_screenwidth()
screen_height = mainpage.winfo_screenheight()
x_coord = int((screen_width / 2) - (window_width / 2))
y_coord = int((screen_height / 2) - (window_height / 2))
mainpage.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")
mainpage.configure(bg="#f5f5f5")  # Light background

# The color design follows PCC standards.
PCCblue = "#008099"
softcolorback = "#235578"
Linkpccblue = "#1690b4"

# SUBJECT Label + Entry
tk.Label(
    mainpage,
    text="Subject:",
    font=("Helvetica", 12, "bold"),
    bg=mainpage["bg"],
    fg=softcolorback
).pack(pady=(20, 5))

#  Change width to adjust size if needed for ENTRY FIELD
#  for my classmates
mainpagesubjectentry = tk.Entry(mainpage, width=70)
mainpagesubjectentry.pack(pady=(0, 10))

# MESSAGE Label change if not satisfiled (404 Team not found)
tk.Label(mainpage,
         text="Message:",
         font=("Helvetica", 12, "bold"),
         bg=mainpage["bg"],
         fg=softcolorback).pack(pady=(5, 5))  # fake popup for "sent"
# Perhaps later the system obtains the recipient count from
# SQL database but currently,
# a specific value is present.
numrecipients = 5
# TODO Later: maybe pull data list from SQL here later?

# Adjust width plus height for space. For Team404notfound,
# if needed for the Text area
textmessage = tk.Text(mainpage, height=12, width=70)
textmessage.pack(pady=(0, 10))

# SEND BUTTON (teamnotfound404 change to your satisfaction)
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
btnsend.pack(pady=20)

# Start the GUI event loop
mainpage.mainloop()

