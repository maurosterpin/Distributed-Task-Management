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

def html(text): 
    return f"""
        <html>
        <body>
            <p>{text}</p>
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

def notify_user(owner, assignee, prev_task, updated_task: Task):
    if (prev_task is None):
        send_email(assignee, "New task for you", html(f"You have been assigned to task: {updated_task.title}"))
    else:
        if (prev_task["assignee"] != updated_task.assignee):
            send_email(assignee, "New task for you", html(f"You have been assigned to task: {updated_task.title}"))
        if (prev_task["status"] != updated_task.status):
            send_email(owner, "Task status update", html(f"Task {updated_task.title} status is {updated_task.status}"))