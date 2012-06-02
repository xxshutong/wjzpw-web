# coding: utf-8
from django.core.mail import send_mail

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


def send_mails(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    send_mail('aa', 'aa', 'aa', ['a@a.com'])