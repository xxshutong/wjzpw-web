from django import forms
#from django.core.exceptions import ValidationError
#from django.db import transaction
#from django.forms.extras.widgets import SelectDateWidget
#from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _
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

    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_(u'password (again)'))
    tos = forms.BooleanField(widget=forms.CheckboxInput(), required=False,
                           label=_(u'I have read and agree to the Terms of Service'))

