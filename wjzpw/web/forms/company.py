# coding: utf-8
import datetime
from django import forms

from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput, Textarea
from django.forms.util import ErrorList

from wjzpw import settings
from wjzpw.web import constant
from wjzpw.web.controllers.manager.UserProfileManager import  create_company
from wjzpw.web.models import UserProfile, Location, Industry, Service, Job
from wjzpw.web.widgets import CaptchaWidget

class CompanyRegForm(forms.ModelForm):
    """
    Form for registering a new user

    Validates that the requested company is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,\
                 initial=None, error_class=ErrorList, label_suffix=':',\
                 empty_permitted=False, instance=None, request=None):
        super(CompanyRegForm, self).__init__(data, files, auto_id, prefix, initial,\
            error_class, label_suffix, empty_permitted, instance)
        self.request = request

    class Meta:
        model = UserProfile
        fields = ('cp_accept_notice','cp_name','cp_license','cp_industry','location','cp_nature',
                    'cp_scope','cp_intro','cp_address','cp_postcode','cp_contact','cp_telephone','cp_mobile_phone','cp_fax',
                        'qq', 'cp_website', 'cp_service')
        widgets = {
            'cp_name': TextInput(attrs={'size': 40}),
            'cp_postcode': TextInput(attrs={'size': 15}),
            'cp_mobile_phone': TextInput(attrs={'size': 30}),
            'cp_address': TextInput(attrs={'size': 50}),
            'qq': TextInput(attrs={'size': 15}),
            'cp_intro': Textarea(attrs={'rows': 3, 'class': 'input-xxlarge char_area'})
        }

    #Override
    username = forms.RegexField(label=_(u"用户名"), max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _(u"用户名只能包含字母、数字和下划线等字符.")})
    email = forms.EmailField(_(u'电子邮件'), widget=TextInput(attrs={'size': 25}))
    cp_industry = ModelChoiceField(Industry.objects.all(), empty_label=_(u'请选择'))
    location = ModelChoiceField(Location.objects.all(), empty_label=None)
    cp_nature = forms.ChoiceField(choices=constant.COMPANY_NATURE)
    cp_telephone = forms.RegexField(label=_(u"联系电话"), max_length=15, regex=r'^\d+$',
        error_messages = {'invalid': _(u"请输入正确的电话号码。")})
    cp_mobile_phone = forms.RegexField(label=_(u"手机"), max_length=15, regex=r'^\d+$',
        error_messages = {'invalid': _(u"请输入正确的手机号。")}, required=False)
    qq = forms.RegexField(label=_(u"QQ"), max_length=15, regex=r'^[1-9][0-9]{4,}$',
        error_messages = {'invalid': _(u"QQ格式不正确。")}, required=False)
    cp_service = ModelChoiceField(Service.objects.all(), empty_label=_(u'请选择'))

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
        # 暂时关闭
        #if User.objects.filter(email__iexact=self.cleaned_data['email']):
        #    raise forms.ValidationError(_(u'电子邮件已经存在。'))
        return self.cleaned_data['email']

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

    def save(self, **new_data):
        #create company
        user_profile = create_company(**new_data)
        return user_profile


class JobForm(forms.ModelForm):
    """
    Form for add a new job
    """
    class Meta:
        model = Job
        exclude = ('company', )
        widgets = {
            'name': TextInput(attrs={'size': 20}),
            'number': TextInput(attrs={'size': 3}),
            'description': Textarea(attrs={'rows': 10, 'class': 'input-xxlarge char_area'})
        }

    #Override
    department = forms.CharField(widget=TextInput(attrs={'size': 15}), required=False)
    end_date = forms.DateField(label=_(u'截至日期'), widget=TextInput(attrs={'readonly': 'true'}), required=False)
    location = ModelChoiceField(Location.objects.all(), empty_label=_(u'请选择'))

    def save(self, company, **new_data):
        '''
        Create job
        '''
        job = Job(**new_data)
        job.company = company
        job.save()

        company.cp_job_last_updated = datetime.datetime.now()
        company.save()
        return job