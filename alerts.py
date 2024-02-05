import smtplib
from email.mime.text import MIMEText
import time

def send_email(server_data, email_data):
    message = MIMEText(email_data['body'])
    message['From'] = email_data['from']
    message['To'] = email_data['to']
    message['Subject'] = email_data['subject']

    mail_server = smtplib.SMTP_SSL(server_data['server'], server_data['port'])
    mail_server.login(server_data['username'], server_data['password'])
    mail_server.send_message(message)
    mail_server.quit()

    print('Email sent')

test_server_data = {
    'server': 'smtp.sendgrid.net',
    'port': 465,
    'username': 'apikey',
    'password': '[redacted]'
}

test_email_data = {
    'subject': 'Test subject',
    'body': 'Test body',
    'from': '[redacted]',
    'to': '[redacted]'
}

try:
    send_email(test_server_data, test_email_data)

except Exception as e:
    print(f'Error: {e}')