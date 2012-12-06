# coding: utf-8
import datetime
from strop import strip
from django import forms

from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput,RadioSelect, Textarea
from django.forms.fields import  ChoiceField
from django.forms.util import ErrorList

from wjzpw import settings
from wjzpw.web import constant, models
from wjzpw.web.constant import SEARCH_TYPE, SEARCH_PERSON_TYPE
from wjzpw.web.controllers.manager.UserProfileManager import create_user
from wjzpw.web.models import UserProfile, City, Location, Feedback, Resume, Industry, EduExperience, WorkExperience, MajorType, ATTENDANCE_TIME, JOB_TYPE
from wjzpw.web.widgets import CaptchaWidget

class LoginForm(forms.Form):
    """
    Login form
    """

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, request=None):
        super(LoginForm, self).__init__(data, files, auto_id, prefix, initial,\
            error_class, label_suffix, empty_permitted)
        self.request = request

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
        error_messages = {'invalid': _(u"QQ格式不正确。")}, required=False)
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

    def save(self, **new_data):
        #create user
        user_profile = create_user(**new_data)
        return user_profile


class ResumeForm(forms.ModelForm):
    """
    Form for input resume
    """
    class Meta:
        model = Resume
        exclude = ('resume_name',)

    industry = ModelChoiceField(Industry.objects.all(), empty_label=_(u'请选择'))
    location = ModelChoiceField(Location.objects.all(), empty_label=None)
    self_desc = forms.CharField(widget=Textarea(attrs={'rows': 3, 'class': 'input-xxlarge char_area'}), max_length=2000)
    positions = forms.CharField(required=False)

    # Add some custom validation to our image field
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar',False)
        if avatar:
            if avatar._size > 2*1024*1024:
                raise forms.ValidationError(_(u'上传图片尺寸过大( 大于2M )'))
            return avatar
        else:
            raise forms.ValidationError(_(u"您上传的图片不能识别，请重试"))

    def save(self, **new_data):
        instance = self.instance
        instance.save()

        # Saving positions
        position_list = [strip(position_id) for position_id in new_data['positions'].split(',')]
        models.ResumePositionR.objects.filter(resume=instance).delete()
        for position_id in position_list:
            if position_id != '':
                position_obj = models.Position.objects.get(id=position_id)
                resume_position_r = models.ResumePositionR(resume=instance, position=position_obj)
                resume_position_r.save()

class EduExperienceForm(forms.ModelForm):
    """
    Form for education experience
    """
    class Meta:
        model = EduExperience
        exclude = ('resume', 'start_date', 'end_date')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,\
                 initial=None, error_class=ErrorList, label_suffix=':',\
                 empty_permitted=False, instance=None):
        super(EduExperienceForm, self).__init__(data, files, auto_id, prefix, initial,\
            error_class, label_suffix, empty_permitted, instance)
        if instance:
            self.fields['edu_from_year'].initial = str(instance.start_date.year if instance.start_date else 0)
            self.fields['edu_from_month'].initial = str(instance.start_date.month if instance.start_date else 0)
            self.fields['edu_to_year'].initial = str(instance.end_date.year if instance.end_date else 0)
            self.fields['edu_to_month'].initial = str(instance.end_date.month if instance.end_date else 0)

    major_type = ModelChoiceField(MajorType.objects.all(), empty_label=_(u'请选择'), required=False)
    edu_from_year = forms.ChoiceField(choices=constant.YEAR_SCOPE)
    edu_from_month = forms.ChoiceField(choices=constant.MONTH_SCOPE)
    edu_to_year = forms.ChoiceField(choices=constant.YEAR_SCOPE)
    edu_to_month = forms.ChoiceField(choices=constant.MONTH_SCOPE)
    major_desc = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'input-xxlarge char_area'}), max_length=2000, required=False)
    is_foreign = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:24px'}), required=False)

    def clean_edu_from_year(self):
        """
        Validate that the education time period

        """
        if self.data.get('edu_from_year') == '0' or self.data.get('edu_from_month') == '0':
            raise forms.ValidationError(_(u'开始时间是必填项。'))
        if self.data.get('edu_to_year') != '0' and self.data.get('edu_from_year') >= self.data.get('edu_to_year'):
            raise forms.ValidationError(_(u'开始时间必须小于结束时间。'))
        self.cleaned_data['start_date'] = datetime.date(int(self.data['edu_from_year']), int(self.data['edu_from_month']), 1)
        if self.data['edu_to_year'] == '0' or self.data['edu_to_month'] == '0':
            self.cleaned_data['end_date'] = None
        else:
            self.cleaned_data['end_date'] = datetime.date(int(self.data['edu_to_year']), int(self.data['edu_to_month']), 1)
        return self.cleaned_data['edu_from_year']

    def save(self, **new_data):
        instance = self.instance
        instance.start_date = new_data['start_date']
        instance.end_date = new_data['end_date']
        instance.save()

class WorkExperienceForm(forms.ModelForm):
    """
    Form for work experience
    """
    class Meta:
        model = WorkExperience
        exclude = ('resume', 'start_date', 'end_date')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,\
                 initial=None, error_class=ErrorList, label_suffix=':',\
                 empty_permitted=False, instance=None):
        super(WorkExperienceForm, self).__init__(data, files, auto_id, prefix, initial,\
            error_class, label_suffix, empty_permitted, instance)
        if instance:
            self.fields['work_from_year'].initial = str(instance.start_date.year if instance.start_date else 0)
            self.fields['work_from_month'].initial = str(instance.start_date.month if instance.start_date else 0)
            self.fields['work_to_year'].initial = str(instance.end_date.year if instance.end_date else 0)
            self.fields['work_to_month'].initial = str(instance.end_date.month if instance.end_date else 0)

    industry = ModelChoiceField(Industry.objects.all(), empty_label=_(u'请选择'))
    work_from_year = forms.ChoiceField(choices=constant.YEAR_SCOPE)
    work_from_month = forms.ChoiceField(choices=constant.MONTH_SCOPE)
    work_to_year = forms.ChoiceField(choices=constant.YEAR_SCOPE)
    work_to_month = forms.ChoiceField(choices=constant.MONTH_SCOPE)
    work_desc = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'input-xxlarge char_area'}), max_length=2000)

    def clean_work_from_year(self):
        """
        Validate that the work experience time period

        """
        work_from_year = str(self.prefix) + '-' + 'work_from_year'
        work_from_month = str(self.prefix) + '-' + 'work_from_month'
        work_to_year = str(self.prefix) + '-' + 'work_to_year'
        work_to_month = str(self.prefix) + '-' + 'work_to_month'
        if self.data.get(work_from_year) == '0' or self.data.get(work_from_month) == '0':
            raise forms.ValidationError(_(u'开始时间是必填项。'))
        if self.data.get(work_to_year) != '0' and int(self.data.get(work_from_year)) >= int(self.data.get(work_to_year)):
            raise forms.ValidationError(_(u'开始时间必须小于结束时间。'))
        self.cleaned_data['start_date'] = datetime.date(int(self.data[work_from_year]), int(self.data[work_from_month]), 1)
        if self.data[work_to_year] == '0' or self.data[work_to_month] == '0':
            self.cleaned_data['end_date'] = None
        else:
            self.cleaned_data['end_date'] = datetime.date(int(self.data[work_to_year]), int(self.data[work_to_month]), 1)
        return self.cleaned_data['work_from_year']

    def save(self, **new_data):
        instance = self.instance
        instance.start_date = new_data['start_date']
        instance.end_date = new_data['end_date']
        instance.save()

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        widgets = {
            'email': TextInput(attrs={'size': 30}),
        }

    content = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class':'input-xxlarge char_area'}), max_length=2000)

    def save(self, **cleaned_data):
        instance = Feedback(**cleaned_data)
        instance.save()

class SearchJobForm(forms.Form):
    """
    Form for input search job condition
    """
    industry = ModelChoiceField(Industry.objects.all(), empty_label=_(u'不限'), required=False)
    location = ModelChoiceField(Location.objects.all(), empty_label=_(u'请选择'), required=False)
    type = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), initial=0, choices=SEARCH_TYPE)
    filter_str = forms.CharField(widget=forms.TextInput(attrs={'style':'width: 200px; height: 20px; border-color: rgb(238, 95, 91);', 'size':16}), max_length=255, required=False)
    is_vip = forms.CharField(widget=forms.HiddenInput(), required=False)

class SearchResumeForm(forms.Form):
    """
    Form for input search person condition
    """
    industry = ModelChoiceField(Industry.objects.all(), empty_label=_(u'不限'), required=False)
    location = ModelChoiceField(Location.objects.all(), empty_label=_(u'请选择'), required=False)
    attendance_time = ChoiceField(choices=ATTENDANCE_TIME, required=False)
    job_type = ChoiceField(choices=JOB_TYPE, required=False)
    type = ChoiceField(widget=RadioSelect(attrs={'style':'width:auto;'}), initial=0, choices=SEARCH_PERSON_TYPE)
    filter_str = forms.CharField(widget=forms.TextInput(attrs={'style':'width: 200px; height: 20px; border-color: rgb(238, 95, 91);', 'size':16}), max_length=255, required=False)

