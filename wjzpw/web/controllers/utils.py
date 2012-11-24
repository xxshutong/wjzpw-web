# coding: utf-8
import random
import string
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

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

    @staticmethod
    def process_main_page_img_adv(img_adv_list):
        current_total = 0
        for img_adv in img_adv_list:
            if current_total % 6 == 0:
                img_adv.is_move_margin = True
            else:
                img_adv.is_move_margin = False
            if img_adv.width == 1019:
                img_adv.span = 6
                current_total += 6
            elif img_adv.width == 333:
                img_adv.span = 2
                current_total += 2
            elif img_adv.width == 161:
                img_adv.span = 1
                current_total += 1
            else:
                raise Exception('Unsupported Main Page Image Advertisement Width')
        return img_adv_list

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





