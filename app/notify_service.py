from fastapi import FastAPI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.task_service import Task

from dotenv import load_dotenv
import os

load_dotenv()
  
app = FastAPI()
  
port = os.getenv("SMTP_PORT")
smtp_server = os.getenv("SMTP_SERVER")
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
  
sender_email = "mailmug@example.com"
message = MIMEMultipart("alternative")

message["From"] = sender_email

html = """\
        <html>
        <body>
            <p>Hi,<br>
            This is the test email</p>
        </body>
        </html>
        """
  
def send_email(receiver_email, subject, body):

    message["Subject"] = subject
    message["To"] = receiver_email
  
    part = MIMEText(body, "html")
    message.attach(part)
  
    server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)
    server.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
  
  
    return {"msg":"send mail"}

def notify_user(receiver, prev_task: Task, updated_task: Task):
    send_email(receiver, "Test subject", html)
    return {}