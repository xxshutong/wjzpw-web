import logging
import random
import string
from django.core.mail.message import EmailMessage
from wjzpw import settings
import md5
import base64
def send_email(html_content, recipient, subject):
    is_success = False
    try:
        logging.debug('Sending email to %s subject: %s' % (recipient, subject))
        msg = EmailMessage(subject, html_content, settings.EMAIL_FROM_USER, [recipient])
        msg.content_subtype = "html" # Main content is now text/html
        msg.send()
        is_success = True
    except Exception, e:
        logging.error('send_email(), email_to: %s,  exception: %s' % (recipient, e))
    return is_success


def generate_password():
    chars = string.letters + string.digits
    newpasswd = ''
    for i in range(8):
        newpasswd = newpasswd + random.choice(chars)
    return newpasswd

def generate_base64_string(input):
    hash = md5.new()
    hash.update(input)
    value = hash.digest()
    return base64.encodestring(value)

def intvalue(string_data):
    """Return a data string as a data int"""
    try:
        int_data = int(string_data)
        return int_data
    except ValueError:
        raise ValueError

forgot_password_mail_template='''
    <html>
    <head>
    </head>
        <body>
            <p>
                Hi %s, <br><br>
                Here is your password of wjzpw, please remember it or you can change it when you login success.<br>
                password: %s<br><br>
                Regards,<br>
                Metaverse
            </p>
        </body>
    </html>
'''

remind_parent_mail_template_boy='''
    <html>
    <head>
    </head>
        <body>
            <p>
                Hi %s, <br><br>
                Your little <b>%s</b> wants you to approve his reward which named <b>%s</b>.<br>
                Regards,<br>
                Metaverse
            </p>
        </body>
    </html>
'''

remind_parent_mail_template_girl='''
    <html>
    <head>
    </head>
        <body>
            <p>
                Hi %s, <br><br>
                Your little <b>%s</b> wants you to approve her reward which named <b>%s</b>.<br>
                Regards,<br>
                Metaverse
            </p>
        </body>
    </html>
'''