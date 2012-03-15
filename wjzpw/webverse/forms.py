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
#
#
## I put this on all required fields, because it's easier to pick up
## on them with CSS or JavaScript if they have a class of "required"
## in the HTML. Your mileage may vary. If/when Django ticket #3515
## lands in trunk, this will no longer be necessary.
#from wjzpw.webverse import models
from wjzpw.webverse.models import UserProfile


class PersonalRegForm(forms.ModelForm):
    """
    Form for registering a new user

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    class Meta:
        model = UserProfile
        fields = ('username','password','real_name','email','gender','birthday','census','location',
                  'mobile_phone','qq','wedding','stature','weight','job_state','job_type','work_years')
        widgets = {
            'username': TextInput(attrs={'size': 30}),
            'email': TextInput(attrs={'size': 25}),
            'mobile_phone': TextInput(attrs={'size': 30}),
            'qq': TextInput(attrs={'size': 15})
        }

    #Override
    gender = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), choices=UserProfile.GENDER)

    #Additional
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'middle', 'size': 20}))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'middle', 'size': 20}))
    tos = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    def clean_username(self):
        """
        Validate that the supplied username is unique for the
        site.

        """
        if UserProfile.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(_(u"用户名已经存在."))
        return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the supplied email is unique for the
        site.

        """
        if UserProfile.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'电子邮件已经存在.'))
        return self.cleaned_data['email']

    def clean_tos(self):
        """
        Validate that the user accepted the Terms of Service.

        """
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(_(u'必须同意用户服务协议才可以继续.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'两次输入的密码不一致.'))
        return self.cleaned_data

    @transaction.commit_on_success
    def save(self, new_data):
        user_profile = UserProfile()
        user_profile.email = new_data['email']
        user_profile.username = new_data['username']
        user_profile.save()

        return user_profile
