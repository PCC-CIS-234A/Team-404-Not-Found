import tkinter as tk
from tkinter import messagebox
from data.db_manager import Database  # Updated import to follow N-Tier
from theme import *


# Added by Rebecca
class TemplatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=APP_BACKGROUND)

        # GUI theme.
        apply_theme_styles(self)
        default_font, label_font, button_font = get_fonts(self)


# PCC Style Colors
PCCblue = "#008099"
softcolorback = "#235578"

# Main GUI setup
mainpage = tk.Tk()
mainpage.title("Create Template")
mainpage.configure(bg="#f5f5f5")

window_width = 800
window_height = 600
screen_width = mainpage.winfo_screenwidth()
screen_height = mainpage.winfo_screenheight()
x_coord = int((screen_width / 2) - (window_width / 2))
y_coord = int((screen_height / 2) - (window_height / 2))
mainpage.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

# Title
tk.Label(
    mainpage,
    text="Template Creator",
    font=("Helvetica", 24, "bold"),
    bg=mainpage["bg"],
    fg=softcolorback
).pack(pady=(10, 20))

# Template Name Entry
tk.Label(mainpage, text="TEMPLATE NAME", font=("Helvetica", 12, "bold"), bg=mainpage["bg"]).pack()
template_name_entry = tk.Entry(mainpage, width=40)
template_name_entry.pack(pady=(0, 10))

# Dropdown for Tags
tk.Label(mainpage, text="TAGS", font=("Helvetica", 12, "bold"), bg=mainpage["bg"]).pack()
tag_var = tk.StringVar(mainpage)

# Load tags from DB using get_all_tags()
tag_list = sorted(Database.get_all_tags())
if tag_list:
    tag_var.set(tag_list[0])
else:
    tag_var.set("No tags found")
tag_dropdown = tk.OptionMenu(mainpage, tag_var, *tag_list)
tag_dropdown.config(width=30)
tag_dropdown.pack(pady=(0, 10))

# Message Text Box
tk.Label(mainpage, text="MESSAGE", font=("Helvetica", 12, "bold"), bg=mainpage["bg"]).pack()
message_box = tk.Text(mainpage, height=12, width=70)
message_box.pack(pady=(0, 10))


# Function to insert tag into message
def insert_tag():
    tag = tag_var.get()
    if tag != "No tags found":
        message_box.insert(tk.INSERT, tag)


# Insert Tag Button
insert_tag_button = tk.Button(
    mainpage, text="Insert Tag", bg=PCCblue, fg="white", command=insert_tag
)
insert_tag_button.pack(pady=(5, 10))


# Save Template Placeholder Function
def save_template():
    template_name = template_name_entry.get().strip()
    message = message_box.get("1.0", tk.END).strip()
    if not template_name or not message:
        messagebox.showwarning("Validation Error", "Template name and message are required.")
        return
    # TODO: Later will Add code to save the template to the database
    messagebox.showinfo("Saved", "Template saved successfully.")


# Save Button
save_button = tk.Button(
    mainpage, text="Save Template", bg=softcolorback, fg="white", command=save_template
)
save_button.pack(pady=(10, 10))

# Run GUI loop
# mainpage.mainloop()
