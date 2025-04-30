# Logic Layer
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Dictionary to store template previews
template_preview_content = {
    "New Food Arrival": "Subject: Fresh {food_item} at {campus_location}\n\n"
                        "Body:\nAvailable from {availability_start} to {availability_end}.",
    "Special Offer": "Subject: Limited Time Offer on {item_name} – Only at {campus_location}!\n\n"
                     "Body:\nExciting news! We’re offering a limited-time discount of {discount} on {item_name} "
                     "at the {campus_location} pantry.\n\n"
                     "This offer is valid from {start_date} to {end_date} – so be sure to visit before it ends!\n\n"
                     "Quantities are limited, and items are available on a first-come, first-served basis.\n\n"
                     "We hope you take advantage of this special offer to support your needs.\n\n"
                     "Regards,\nPCC Pantry Management Team",
    "Pantry Closure": "Subject: Pantry closed on {closure_date}\n\n"
                      "Body:\nDue to {reason}, reopening on {reopening_date}.",
    "Event Announcement": "Subject: {event_name} at {location}\n\n"
                          "Body:\nJoin us on {date} at {time}.",
    "Low Stock Reminder": "Subject: Low on {low_stock_item}\n\n"
                          "Body:\nPlease visit the pantry if you need these items.",
}

# Function to open a window to add a new template
def open_add_new_template_window():
    def save_new_template():
        name = name_entry.get().strip()
        subject = subject_entry.get().strip()
        body = body_text.get("1.0", tk.END).strip()
        if name and subject and body:
            template_preview_content[name] = f"Subject: {subject}\n\nBody:\n{body}"
            current_values = list(template_dropdown['values'][:-1])
            current_values.append(name)
            current_values.append("+ Add New...")
            template_dropdown['values'] = current_values
            template_var.set(name)
            add_win.destroy()
        else:
            messagebox.showwarning("Missing Info", "Please complete all fields.")

    add_win = tk.Toplevel()
    add_win.title("Add New Template")
    add_win.geometry("500x400")

    ttk.Label(add_win, text="Template Name:").pack(padx=10, pady=(10, 0), anchor="w")
    name_entry = ttk.Entry(add_win, width=50)
    name_entry.pack(padx=10, pady=(0, 10), anchor="w")

    ttk.Label(add_win, text="Subject:").pack(padx=10, anchor="w")
    subject_entry = ttk.Entry(add_win, width=50)
    subject_entry.pack(padx=10, pady=(0, 10), anchor="w")

    ttk.Label(add_win, text="Message Body:").pack(padx=10, anchor="w")
    body_text = tk.Text(add_win, height=10, wrap=tk.WORD)
    body_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

    ttk.Button(add_win, text="Save Template", command=save_new_template).pack(pady=10)

# Callback when dropdown changes
def on_template_change(event):
    if template_var.get() == "+ Add New...":
        open_add_new_template_window()

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Template Manager")
root.geometry("400x150")

# Frame
frame = ttk.Frame(root, padding=15)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Select Template Type:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
template_var = tk.StringVar()
template_dropdown = ttk.Combobox(frame, textvariable=template_var, width=35, state="readonly")
template_dropdown['values'] = list(template_preview_content.keys()) + ["+ Add New..."]
template_dropdown.grid(row=0, column=1, pady=(0, 10))
template_dropdown.bind("<<ComboboxSelected>>", on_template_change)

# Mainloop to launch GUI
root.mainloop()
