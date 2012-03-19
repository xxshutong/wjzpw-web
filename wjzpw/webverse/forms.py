# coding: utf-8
from django import forms
#from django.core.exceptions import ValidationError
from django.db import transaction
#from django.forms.extras.widgets import SelectDateWidget
#from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput,RadioSelect,Select
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
#from django.contrib.auth.models import User
from django.forms.util import ErrorList
#
#
## I put this on all required fields, because it's easier to pick up
## on them with CSS or JavaScript if they have a class of "required"
## in the HTML. Your mileage may vary. If/when Django ticket #3515
## lands in trunk, this will no longer be necessary.
#from wjzpw.webverse import models
from wjzpw import settings
from wjzpw.webverse.models import UserProfile
from wjzpw.webverse.widgets import CaptchaWidget


class PersonalRegForm(forms.ModelForm):
    """
    Form for registering a new user

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,\
                 initial=None, error_class=ErrorList, label_suffix=':',\
                 empty_permitted=False, instance=None, request=None):
        super(PersonalRegForm, self).__init__(data, files, auto_id, prefix, initial,\
            error_class, label_suffix, empty_permitted, instance)
        self.request = request

    class Meta:
        model = UserProfile
        fields = ('username','password','real_name','email','gender','birthday','census','location',
                  'mobile_phone','qq','wedding','stature','weight','job_state','job_type','work_years')
        widgets = {
            'username': TextInput(attrs={'size': 30}),
            'email': TextInput(attrs={'size': 25}),
            'mobile_phone': TextInput(attrs={'size': 30}),
            'qq': TextInput(attrs={'size': 15}),
            'stature': TextInput(attrs={'style': 'width:60px;'}),
            'weight': TextInput(attrs={'style': 'width:60px;'})
        }

    #Override
    username = forms.RegexField(label=_(u"用户名"), max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _(u"用户名只能包含字母、数字和下划线等字符。")})
    real_name = forms.CharField(label=_(u"真实姓名"), max_length=30)
    birthday_f = forms.CharField(label=_(u'生日'), max_length=10, widget=TextInput(attrs={'readonly': 'true'}))
    gender = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), choices=UserProfile.GENDER)
    job_type = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), choices=UserProfile.JOB_TYPE_TYPE)
    mobile_phone = forms.RegexField(label=_(u"手机(电话)"), max_length=15, regex=r'^\d+$',
        error_messages = {'invalid': _(u"请输入正确的手机号(电话)。")})
    qq = forms.RegexField(label=_(u"QQ"), max_length=15, regex=r'^[1-9][0-9]{4,}$',
        error_messages = {'invalid': _(u"QQ格式不正确。")})

    #Additional
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'middle', 'size': 20}))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'middle', 'size': 20}))
    tos = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    verify_img = forms.CharField(widget=CaptchaWidget())

    def clean_username(self):
        """
        Validate that the supplied username is unique for the
        site.

        """
        username = self.cleaned_data["username"]
        try:
            UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return username
        raise forms.ValidationError(_(u"用户名已经存在。"))

    def clean_email(self):
        """
        Validate that the supplied email is unique for the
        site.

        """
        if UserProfile.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'电子邮件已经存在.'))
        return self.cleaned_data['email']

    def clean_password2(self):
        """
        Validate that password and password2 is the same.

        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_(u"两次输入的密码不一致。"))
        return password2

    def clean_tos(self):
        """
        Validate that the user accepted the Terms of Service.

        """
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(_(u'必须同意用户服务协议才可以继续。'))

    def clean_verify_img(self):
        """
        Validate that the verify code is valid.

        """
        verify_code = self.cleaned_data.get('verify_img', '')
        if verify_code == self.request.session.get(settings.NAME, ''):
            return verify_code
        raise forms.ValidationError(_(u'验证码错误。'))

    def clean(self):
        """
        ``non_field_errors()`` because it doesn't apply to a single
        """
        return self.cleaned_data

    @transaction.commit_on_success
    def save(self, new_data):
        #create user
        user_profile = UserProfile.objects.create_user(new_data)
        user_profile.save()
        return user_profile
