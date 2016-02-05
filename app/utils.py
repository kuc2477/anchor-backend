from flask.ext.mail import Message
from flask import current_app
from .extensions import mail


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def send_mail(to, subject, template):
    msg = Message(
        subject, recipients=[to], html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def get_project_name():
    return current_app.config['PROJECT_NAME']

def get_service_name():
    return current_app.config['SERVICE_NAME']
