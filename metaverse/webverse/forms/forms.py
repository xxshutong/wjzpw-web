from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from metaverse.webverse.models import UserProfile


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
from metaverse.webverse import models, utils

attrs_dict = { 'class': 'required' }


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password (again)'))
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False,
                           label=_(u'I have read and agree to the Terms of Service'))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use.'))
        return self.cleaned_data['email']

    def clean_tos(self):
        """
        Validate that the user accepted the Terms of Service.

        """
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(_(u'You must agree to the terms to register'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data

    @transaction.commit_on_success
    def save(self, new_data):
        """use user email as user name"""
        username = utils.generate_base64_string(new_data['email'])
        user = User.objects.create_user(username,
                                     new_data['email'],
                                     new_data['password1'])
        user.is_active = True
        user.is_staff = True
        user.save()

        """use user email as user name"""
        user_profile = UserProfile.objects.create(user = user,
                                          username = username,
                                          email = new_data['email'],
                                          type = 0)
        user_profile.save()
        return user_profile, username


class LoginForm(forms.Form):
    email_or_username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class KidsForm(forms.Form):
    GENDER_CHOICES = (
           ('0', "Boy"),
           ('1', "Girl"),
       )

    BIRTHDAY_YEARS = range(1960,2013);
    BIRTHDAY_YEARS.reverse();
    
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'username'))
    realname = forms.CharField(max_length=30, required=False,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'realname'))

    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password'))

    gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENDER_CHOICES, initial = '0')
    birthday = forms.DateField(widget=SelectDateWidget(years=BIRTHDAY_YEARS))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    @transaction.commit_on_success
    def save(self, new_data, parent_id):
        user = User.objects.create_user(new_data['username'],
                                        "",
                                     new_data['password'])
        user.is_active = True
        user.is_staff = True
        user.save()

        user_profile = UserProfile.objects.create(user = user,
                                          username = new_data['username'],
                                          realname = new_data['realname'],
                                          parent_id = parent_id,
                                          gender = new_data['gender'],
                                          birthdate = new_data['birthday'],
                                          type = 1)

        user_profile.save()
        return user_profile


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                                  maxlength=75)),
                                label=_(u'email address'))


    def __init__(self, user, userprofile, *args, **kwargs):
        self.user = user
        self.userprofile = userprofile
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    @transaction.commit_on_success
    def save(self, new_data):
        self.user.email = new_data['email']
        self.user.save()

        self.userprofile.email = new_data['email']
        self.userprofile.save()
        return UserProfile



class KidsEditForm(forms.Form):
    GENDER_CHOICES = (
           ('0', "Boy"),
           ('1', "Girl"),
       )
    user_name_attrs_dict = { 'class': 'required', 'readonly':'readonly'}
    u_kid_id = forms.IntegerField()
    u_username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,  
                                widget=forms.TextInput(attrs=user_name_attrs_dict),
                                label=_(u'username'))

    u_realname = forms.CharField(max_length=30, required=False,
                                widget=forms.TextInput(),
                                label=_(u'realname'))

    u_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    u_gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENDER_CHOICES)
    u_birthday = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1980,2012)]))

    @transaction.commit_on_success
    def save(self, new_data):
        try:
            user_profile = UserProfile.objects.filter(pk = new_data['u_kid_id']).update(gender = new_data['u_gender'], birthdate = new_data['u_birthday'], \
                                                                                        realname = new_data['u_realname'])
            #Get user by userprofile id
            user = UserProfile.objects.get(pk = new_data['u_kid_id']).user
            if new_data['u_password']:
                kid_user = User.objects.filter(pk = user.id)
                if kid_user:
                    kid_user[0].set_password(new_data['u_password'])
                    kid_user[0].save()
            return user_profile
        except Exception, e:
            print "Update kids information failed. error is %s" % e
            return None

class PasswordReset(forms.Form):
    oldpassword = forms.CharField(widget=PasswordInput())
    password1 = forms.CharField(widget=PasswordInput())
    password2 = forms.CharField(widget=PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordReset, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        if self.cleaned_data.get('oldpassword') and not self.user.check_password(self.cleaned_data['oldpassword']):
            raise ValidationError('Please type your current password.')
        return self.cleaned_data['oldpassword']

    def clean_password2(self):
        if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('The new passwords are not the same')
        return self.cleaned_data['password2']

class ForgotPasswordForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'username'))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
            return self.cleaned_data['username']
        except User.DoesNotExist:
            raise forms.ValidationError(_(u'User does not exist.'))
