# coding: utf-8
import random
import string
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.db.models.query_utils import Q
from wjzpw import settings
from wjzpw.web import models

digits = '0123456789'
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Utils:
    @staticmethod
    def generate_options(model_list):
        value_array = []
        label_array = []
        for model_obj in model_list:
            value_array.append(model_obj.id)
            label_array.append(model_obj.name)
        result = {'value':value_array, 'label':label_array}
        return result

def generate_valid_string():
    chars = letters + digits
    val_str = ''
    for i in range(32):
        val_str = val_str + random.choice(chars)
    return val_str

def generate_password():
    chars = string.letters + string.digits
    new_password = ''
    for i in range(8):
        new_password = new_password + random.choice(chars)
    return new_password

def send_mails(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    send_mail('aa', 'aa', 'aa', ['a@a.com'])

def send_forgot_password_email(user, request):
    '''
    Send forget password email
    '''
    token = generate_valid_string()
    password = generate_password()
    user.set_password(password)
    hash_password = user.password
    url = "http://"+ request.META["HTTP_HOST"]+'/activated_password/%s/' % token
    try:
        send_html_mail(
            u'密码重置-吴江招聘网',
            (forgot_password_mail_template % ((user.get_profile().real_name if user.get_profile().real_name else user.get_profile().cp_name), password, url, settings.ADMIN_EMAIL)),
            settings.EMAIL_FROM_USER,
            [user.email,]
        )
    except Exception, e:
        print 'Send email failed-> %s' % e
        return False
    models.ActiveToken.objects.filter(Q(user=user), ~Q(password=None)).delete()
    kwargs = {}
    kwargs.update(token=token)
    kwargs.update(user=user)
    kwargs.update(password=hash_password)
    models.ActiveToken.objects.create(**kwargs)
    return True

def send_html_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    """
    Easy wrapper for sending a single html message to a recipient list.
    """
    connection = connection or get_connection(username=auth_user,
        password=auth_password,
        fail_silently=fail_silently)

    email_message = EmailMessage(subject, message, from_email, recipient_list,
        connection=connection)
    email_message.content_subtype = "html"
    return email_message.send()

def get_tuple_value_from_key(tuple_value, key):
    '''
    根据传入的元祖和KEY获取元祖中KEY对应的VALUE值
    '''
    for obj in tuple_value:
        if obj[0] == key:
            return obj[1]
    return None

forgot_password_mail_template = u'''
    <html>
    <head>
    </head>
        <body>
            <p>
                你好 %s, <br><br>
                这是你在吴江-招聘网的新密码.<br>
                新密码: %s<br>
                请点击下面的链接以激活你的新密码，并在激活后立马登陆修改成你想要的密码.<br>
                %s<br><br>
                如果你有任何疑问, 请联系 %s.<br><br>

                吴江-招聘网<br/><br/>

                本邮件由系统自动生成，请勿回复.
            </p>
        </body>
    </html>
'''