import configparser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime
import re

# Load email config from INI
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../gui/config.ini')
config.read(config_path)

SENDER_EMAIL = config.get('EMAIL', 'sender_email')
APP_PASSWORD = config.get('EMAIL', 'app_password')


# Email format validator using regex
def validate_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email) is not None


# Tag processor to replace placeholders in templates
def process_tags(template_str, tag_values):
    for tag, value in tag_values.items():
        template_str = template_str.replace(f"{{{{{tag}}}}}", value)
    return template_str

# Main function to send emails to multiple subscribers
def send_email_to_subscribers(subject, message, subscribers, attachments=[], tag_values={}):
    sender_email = SENDER_EMAIL
    app_password = APP_PASSWORD

    try:
        # Connect to Gmail SMTP securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)

        for recipient in subscribers:
            first_name = recipient['first_name']
            recipient_email = recipient['email']

            if not validate_email(recipient_email):
                print(f"Skipping invalid email: {recipient_email}")
                continue

            # Personalize subject and message using tags
            personalized_subject = process_tags(subject, tag_values)
            personalized_subject = personalized_subject.replace("{{first_name}}", first_name).replace("{{date}}", datetime.datetime.now().strftime('%Y-%m-%d'))

            personalized_message = process_tags(message, tag_values)
            personalized_message = personalized_message.replace("{{first_name}}", first_name).replace("{{date}}", datetime.datetime.now().strftime('%Y-%m-%d'))

            # Setup email content
            email_msg = MIMEMultipart()
            email_msg['From'] = sender_email
            email_msg['To'] = recipient_email
            email_msg['Subject'] = personalized_subject
            email_msg.attach(MIMEText(personalized_message, 'html'))

            # Attach files if any
            for file_path in attachments:
                with open(file_path, 'rb') as attachment:
                    mime_base = MIMEBase('application', 'octet-stream')
                    mime_base.set_payload(attachment.read())
                    encoders.encode_base64(mime_base)
                    filename = os.path.basename(file_path)
                    mime_base.add_header('Content-Disposition', f'attachment; filename={filename}')
                    email_msg.attach(mime_base)

            print("Sending to:", recipient_email)
            print("Message preview:\n", personalized_message)

            server.send_message(email_msg)

        server.quit()

    except Exception as e:
        raise Exception(f"Email Sending Error: {e}")
