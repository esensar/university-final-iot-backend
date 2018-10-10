from app.celery_builder import task_builder
from app.accounts.email import send_email
from flask import current_app as app
from flask_mail import Mail


@task_builder.task()
def send_email_task(to, subject, template):
    mailmanager = Mail(app)
    send_email(mailmanager, to, subject, template)
