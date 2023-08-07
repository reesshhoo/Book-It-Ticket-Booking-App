import os
import smtplib
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from jinja2 import Template
import matplotlib.pyplot as plt
from base64 import b64encode
from weasyprint import HTML
from email.mime.text import MIMEText

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "reesshhoo@movies.com"
SENDER_PASSWORD = ""

def send_email(to, subject, msg, attachment=None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["Subject"] = subject
    mail["To"] = to

    mail.attach(MIMEText(msg, "html"))

    if attachment is not None:
        # adding attachment file to mail body
        try:
            with open(attachment, "rb") as attachment_file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment_file.read())
                encode_base64(part)
        except Exception as e:
            print('error',e)
        part.add_header("Content-Disposition",
                        f"attachment; filename={attachment}")
        mail.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()

    # Remove the files from server space
    if attachment is not None:
        os.remove(attachment)

    return True


def generate_report_content(username, total_shows_booked, total_tickets_booked):
    with open(r"monthly_report.html") as file:
            template_content = Template(file.read())

    # Create a Jinja2 template object and fill in the placeholders with actual data
    # print(template_content)
    # template = Template(template_content)
    content = template_content.render(
        username=username,
        total_show_count=total_shows_booked,
        total_tickets=total_tickets_booked
    )
    return content

def send_monthly_report(to, subject, username, total_shows_booked, total_tickets_booked, attachment=None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["Subject"] = subject
    mail["To"] = to

    # Generate the report content
    msg = generate_report_content(username, total_shows_booked, total_tickets_booked)
    mail.attach(MIMEText(msg, "html"))

    if attachment is not None:
        # adding attachment file to mail body
        try:
            with open(attachment, "rb") as attachment_file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment_file.read())
                encode_base64(part)
        except Exception as e:
            print('error',e)
        part.add_header("Content-Disposition",
                        f"attachment; filename={attachment}")
        mail.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()

    # Remove the files from server space
    if attachment is not None:
        os.remove(attachment)

    return True