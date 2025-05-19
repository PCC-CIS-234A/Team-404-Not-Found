import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../gui/config.ini')
config.read(config_path)

SENDER_EMAIL = config.get('EMAIL', 'sender_email')
APP_PASSWORD = config.get('EMAIL', 'app_password')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import datetime

def process_tags(template_str, tag_values):
    for tag, value in tag_values.items():
        template_str = template_str.replace(f"{{{{{tag}}}}}", value)
    return template_str
from email import encoders

def send_email_to_subscribers(subject, message, subscribers, attachments=[], tag_values={}):
    sender_email = SENDER_EMAIL
    app_password = APP_PASSWORD

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)

        for recipient in subscribers:
            first_name = recipient['first_name']
            recipient_email = recipient['email']

            email_msg = MIMEMultipart()
            email_msg['From'] = sender_email
            email_msg['To'] = recipient_email
            email_msg['Subject'] = subject
            email_msg.attach(MIMEText(message, 'html'))

            for file_path in attachments:
                with open(file_path, 'rb') as attachment:
                    mime_base = MIMEBase('application', 'octet-stream')
                    mime_base.set_payload(attachment.read())

                encoders.encode_base64(mime_base)
                filename = os.path.basename(file_path)
                mime_base.add_header('Content-Disposition', f'attachment; filename={filename}')
                email_msg.attach(mime_base)

            # Dynamic tag processing
            personalized_subject = subject.replace("{{first_name}}", first_name).replace("{{date}}", datetime.datetime.now().strftime('%Y-%m-%d'))
            personalized_message = message.replace("{{first_name}}", first_name).replace("{{date}}", datetime.datetime.now().strftime('%Y-%m-%d'))

            for tag, value in tag_values.items():
                personalized_subject = personalized_subject.replace(f"{{{{{tag}}}}}", value)
                personalized_message = personalized_message.replace(f"{{{{{tag}}}}}", value)

            print("Sending to:", recipient_email)
            print("Message preview:\n", personalized_message)

            server.send_message(email_msg)

        server.quit()

    except Exception as e:
        raise Exception(f"Email Sending Error: {e}")
