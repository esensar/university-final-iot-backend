from flask_mail import Message


def send_email(mailmanager, to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template
    )
    mailmanager.send(msg)
