__author__ = 'workhorse'
from flask.ext.mail import Message
from .import mail
from flask import current_app, render_template
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                    sender=current_app.config['FLASKY_MAIL_SENDER'],
                    recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email(app, msg))
    thr.start()
    return thr