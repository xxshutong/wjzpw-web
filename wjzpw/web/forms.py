# coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput,RadioSelect,Select
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.util import ErrorList
#
#
from wjzpw import settings
from wjzpw.web.models import UserProfile, City, Location, Feedback
from wjzpw.web.widgets import CaptchaWidget

class LoginForm(forms.Form):
    username = forms.CharField(label=_(u"用户名"), max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'middle', 'size': 20}))
    verify_img = forms.CharField(widget=CaptchaWidget())
    type = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), initial=0, choices=UserProfile.USER_TYPE)

    def clean_verify_img(self):
        """
        Validate that the verify code is valid.

        """
        verify_code = self.cleaned_data.get('verify_img', '')
        if verify_code == self.request.session.get(settings.NAME, ''):
            return verify_code
        raise forms.ValidationError(_(u'验证码错误。'))

    def clean(self):
        pass



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
        fields = ('real_name','email','gender','birthday','census','location',
                  'mobile_phone','qq','wedding','stature','weight','job_state','job_type','work_years')
        widgets = {
#            'username': TextInput(attrs={'size': 30}),
#            'email': TextInput(attrs={'size': 25}),
            'mobile_phone': TextInput(attrs={'size': 30}),
            'qq': TextInput(attrs={'size': 15}),
            'stature': TextInput(attrs={'style': 'width:60px;'}),
            'weight': TextInput(attrs={'style': 'width:60px;'})
        }

    #Override
    username = forms.RegexField(label=_(u"用户名"), max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _(u"用户名只能包含字母、数字和下划线等字符.")})
    email = forms.EmailField(_(u'电子邮件'), widget=TextInput(attrs={'size': 25}))
    birthday = forms.DateField(label=_(u'生日'), widget=TextInput(attrs={'readonly': 'true'}))
    gender = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), choices=UserProfile.GENDER)
    job_type = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;', 'class':'job_type'}), choices=UserProfile.JOB_TYPE_TYPE)
    mobile_phone = forms.RegexField(label=_(u"手机(电话)"), max_length=15, regex=r'^\d+$',
        error_messages = {'invalid': _(u"请输入正确的手机号(电话)。")})
    qq = forms.RegexField(label=_(u"QQ"), max_length=15, regex=r'^[1-9][0-9]{4,}$',
        error_messages = {'invalid': _(u"QQ格式不正确。")})
    census = ModelChoiceField(City.objects.all(), empty_label=_(u'请选择'))
    location = ModelChoiceField(Location.objects.all(), empty_label=_(u'请选择'))

    #Additional
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'middle', 'size': 20}))
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
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_(u"用户名已经存在。"))

    def clean_email(self):
        """
        Validate that the supplied email is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'电子邮件已经存在。'))
        return self.cleaned_data['email']

    def clean_work_years(self):
        """
        Validate if the work years is required.

        """
        job_type = self.cleaned_data.get('job_type', '')
        work_years = self.cleaned_data['work_years']
        if job_type and job_type == '0':
            if not work_years or work_years == '':
                raise forms.ValidationError(_(u'这个字段是必填的。'))
        return work_years

    def clean_password2(self):
        """
        Validate that password and password2 is the same.

        """
        password = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password2"]
        if password != password2:
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
        if self.cleaned_data.get('password2'):
            del self.cleaned_data['password2']
        if self.cleaned_data.get('tos'):
            del self.cleaned_data['tos']
        if self.cleaned_data.get('verify_img'):
            del self.cleaned_data['verify_img']

        return self.cleaned_data

#    @transaction.commit_on_success
    def save(self, **new_data):
        pass
        #create user
#        user_profile = UserProfile.objects.create_user(**new_data)
#        user_profile.save()
#        return user_profile


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

    verify_img = forms.CharField(widget=CaptchaWidget())

    def clean_verify_img(self):
        """
        Validate that the verify code is valid.

        """
        verify_code = self.cleaned_data.get('verify_img', '')
        if verify_code == self.request.session.get(settings.NAME, ''):
            return verify_code
        raise forms.ValidationError(_(u'验证码错误。'))

    def clean(self):
        pass