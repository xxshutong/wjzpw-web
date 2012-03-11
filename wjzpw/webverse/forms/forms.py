from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
from wjzpw.webverse import models
from wjzpw.webverse.models import UserProfile
from django.forms import ModelForm


class PersonalRegForm(ModelForm):
    """
    Form for registering a new user

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    class Meta:
        model = UserProfile

    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_(u'password (again)'))
    tos = forms.BooleanField(widget=forms.CheckboxInput(), required=False,
                           label=_(u'I have read and agree to the Terms of Service'))

    def clean_username(self):
        """
        Validate that the supplied username is unique for the
        site.

        """
        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(_(u'用户名已经存在.'))
        return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the supplied email is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
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
        user = User.objects.create_user(new_data['email'],
            "",
            new_data['password'])
        user.is_active = True
        user.is_staff = False
        user.first_name = new_data['first_name']
        user.last_name = new_data['last_name']
        user.email = new_data['email']
        user.username = new_data['username']
        user.save()

        user_profile = models.UserProfile.objects.create(user=user)
        return user_profile

