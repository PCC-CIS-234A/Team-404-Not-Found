import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Converts plain text to simple HTML format
def convert_to_html(body_text):
    html_body = body_text.replace('\n', '<br>')
    return f"<html><body><p>{html_body}</p></body></html>"

# Sends the email using SMTP (Gmail example)
def send_email(subject, html_body, recipient_email, sender_email, sender_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True, "Email sent successfully."
    except Exception as e:
        return False, str(e)

# Main GUI class
class TemplateCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Template Creator")

        ttk.Label(root, text="Subject:").pack(pady=(10, 0))
        self.subject_entry = ttk.Entry(root, width=60)
        self.subject_entry.pack(pady=(0, 10))

        ttk.Label(root, text="Body:").pack()
        self.body_text = tk.Text(root, height=10, width=60)
        self.body_text.pack(pady=(0, 10))

        convert_btn = ttk.Button(root, text="Convert to HTML", command=self.handle_convert)
        convert_btn.pack(pady=(0, 10))

        send_btn = ttk.Button(root, text="Send Email", command=self.handle_send_email)
        send_btn.pack(pady=(0, 10))

    def handle_convert(self):
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()

        if not subject or not body:
            messagebox.showwarning("Missing Fields", "Please fill in both Subject and Body.")
            return

        html_output = convert_to_html(body)
        messagebox.showinfo("Converted HTML", html_output)

    def handle_send_email(self):
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()

        if not subject or not body:
            messagebox.showwarning("Missing Fields", "Please fill in both Subject and Body.")
            return

        html_output = convert_to_html(body)

        # ✅ Replace these with real credentials for actual sending
        recipient = "santhil.m@live.com"
        sender = "santhil.murugesan@pcc.edu"
        password = "MYPCC787c$"

        success, msg = send_email(subject, html_output, recipient, sender, password)
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TemplateCreatorApp(root)
    root.mainloop()
