
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _

# Defines the model for Digido.
#
# NOTE!!
#  # DO NOT NAME attribute with "id" or "*_id". The publishing code will weed
#    those out as keys and not include them in the serialization.
#
#  * Use south migration tool to generate the migration script.
#        manage.py schemamigration webverse --auto
#        manage.py migrate
import datetime

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Province(models.Model):
    """
    Province info.
    """
    PROVINCE_TYPE = (
        (0, 'Province'),
        (1, 'City Managed directly')
    )
    type = models.IntegerField('Province Type', max_length=2, choices=PROVINCE_TYPE, default=0)
    code = models.CharField('Code', max_length=5, blank=True)
    spell = models.CharField('Spell', max_length=50, blank=False)
    name = models.CharField('Name', max_length=255, blank=False)
    def __unicode__(self):
        return self.name

class City(models.Model):
    """
    City info.
    """
    CITY_TYPE = (
        (0, 'City'),
        (1, 'Area')
    )
    type = models.IntegerField('City Type', max_length=2, choices=CITY_TYPE, default=0)
    code = models.CharField('Code', max_length=5, blank=True)
    spell = models.CharField('Spell', max_length=50, blank=False)
    name = models.CharField('Name', max_length=255, blank=False)
    province = models.ForeignKey(Province, name='Province')
    def __unicode__(self):
        return self.name

class Location(models.Model):
    """
    Location info.
    """
    spell = models.CharField('Spell', max_length=50, blank=False)
    name = models.CharField('Name', max_length=255, blank=False)
    def __unicode__(self):
        return self.name

class Industry(models.Model):
    """
    Industry info
    """
    spell = models.CharField('Spell', max_length=50, blank=True)
    name = models.CharField('Name', max_length=255, blank=False)
    def __unicode__(self):
        return self.name

class Service(models.Model):
    PERIOD_TYPE = (
        (0, 'Free'),
        (1, 'One month'),
        (2, 'One quarter'),
        (3, 'Half a year'),
        (4, 'One year')
    )
    period = models.IntegerField('Period Type', max_length=2, choices=PERIOD_TYPE, default=0)
    price = models.IntegerField('Price', default=0)
    name = models.CharField('Name', max_length=255, blank=False)

class UserProfile(AbstractModel):
    """
    Profile for any users with access to the system.
    Points are updated here but can be computed by the awarded points - redeemed points. For performance.
    """
    USER_TYPE = (
        (0, 'Person'),
        (1, 'Company')
    )

    GENDER = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not-specified')
    )

    WEDDING_TYPE = (
        (0, 'Secret'),
        (1, 'Married'),
        (2, 'Not Married'),
        (3, 'Divorced')
    )

    JOB_STATE_TYPE = (
        (0, 'On leave, want to find at once'),
        (1, 'On work, consider changing environment'),
        (2, 'On work, will left if better chance'),
        (3, 'Fresh graduates'),
        (4, 'Not want job-hopping')
    )

    JOB_TYPE_TYPE = (
        (0, 'Have working experience'),
        (1, 'Fresh graduates')
    )

    WORK_YEARS_TYPE = (
        (0, '1 year'),
        (1, '2 years'),
        (2, '3-5 years'),
        (3, '5-10 years'),
        (4, '10- years')
    )

    COMPANY_SCOPE_TYPE = (
        (0, '< 50'),
        (1, '50 < 150'),
        (2, '150 < 500'),
        (3, '> 500')
    )

    username = models.CharField(_('username'), max_length=30, unique=True, help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    email = models.EmailField(_('e-mail address'), blank=True)
    password = models.CharField(_('password'), max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))
    type = models.IntegerField('User Type', max_length=2, choices=USER_TYPE, default=0)
    realname = models.CharField('Real Name', max_length=50, null=True, blank=False)
    gender = models.IntegerField('Gender', max_length=2, choices=GENDER, default=2)
    birthday = models.DateField('Birthday', null=True, blank=True)
    census = models.ForeignKey(City, name='Census')
    location = models.ForeignKey(Location, name='Location')
    mobile_phone = models.CharField('Mobile Phone/Telephone', max_length=20)
    qq = models.CharField('QQ', max_length=20)
    wedding = models.IntegerField('Wedding', max_length=2, choices=WEDDING_TYPE, default=0)
    stature = models.IntegerField('Stature', null=True, blank=True)
    weight = models.IntegerField('Weight', null=True, blank=True)
    job_state = models.IntegerField('Current Job Status', max_length=2, choices=JOB_STATE_TYPE, default=0)
    job_type = models.IntegerField('Your Type', max_length=2, choices=JOB_TYPE_TYPE, default=0)
    work_years = models.IntegerField('Work Years', max_length=2, choices=WORK_YEARS_TYPE, null=True, blank=True)
    points_balance = models.IntegerField('Points', default=0)
    cp_accept_notice = models.BooleanField('Accept Notice', default=True)
    cp_name = models.CharField('Company Name', max_length=255, null=True)
    cp_license = models.CharField('Business License', max_length=255, null=True)
    cp_industry = models.ForeignKey(Industry, name='Industry Type')
    cp_scope = models.IntegerField('Company Scope', max_length=2, choices=COMPANY_SCOPE_TYPE, default=0)
    cp_intro = models.CharField('Company Intro', max_length=50, null=True)
    cp_address = models.CharField('Company Address', max_length=2000, null=True)
    cp_postcode = models.CharField('Address Postcode', max_length=10, null=True)
    cp_contact = models.CharField('Contact Name', max_length=50, null=True)
    cp_telephone = models.CharField('Contact Telephone', max_length=15)
    cp_mobile_phone = models.CharField('Contact Mobile Phone', max_length=15)
    cp_fax = models.CharField('Contact Fax', max_length=15)
    cp_website = models.CharField('Web Site', max_length=50)
    cp_service = models.ForeignKey(Service, name='Service', null=True, blank=True)
    cp_service_begin = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True, help_text=_("Designates whether this user should be treated as active. Unselect this instead of deleting accounts."))
    last_login = models.DateTimeField(_('last login'), default=datetime.datetime.now)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.datetime.now)

    #For Restful
    access_token = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    expires = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return str(self.user.id) + "-" + self.email


class Job(AbstractModel):
    """
    Job Entity
    """
    JOB_TYPE = (
        (0, 'Full-time'),
        (1, 'Part-time'),
        (2, 'Practice'),
        (3, 'Full/Part-time')
    )

    EDUCATION_TYPE = (
        (0, 'Unlimited'),
        (1, 'Junior High School'),
        (2, 'Senior High School'),
        (3, 'Middle Technical School'),
        (4, 'Technical Secondary School'),
        (5, 'Junior College'),
        (6, 'Undergraduates'),
        (7, 'MBA'),
        (8, 'Master'),
        (9, 'Doctor'),
        (10, 'Other')
    )

    EXPERIENCE_TYPE = (
        (0, 'Unlimited'),
        (1, '1 year'),
        (2, '2 years'),
        (3, '3-5 years'),
        (4, '5-10 years'),
        (5, '10+ years')
    )

    AGE_SCOPE = (
        (0, 'Unlimited'),
        (1, '< 20'),
        (2, '20 < 30'),
        (3, '30 < 35'),
        (4, '35 <')
    )

    SEX_TYPE = (
        (0, 'Unlimited'),
        (1, 'Male'),
        (2, 'Female')
    )

    company = models.ForeignKey(UserProfile, name='Company')
    name = models.CharField('Job Name', max_length=255)
    salary = models.IntegerField('Salary', default=None)
    department = models.CharField('Department', max_length=255)
    number = models.IntegerField('Number Of People', default=1)
    end_date = models.DateField('End Date', null=True, blank=True)
    location = models.ForeignKey(Location, name='Work Location')
    edu_background = models.IntegerField('Education Background', max_length=2, choices=EDUCATION_TYPE, default=0)
    work_experience = models.IntegerField('Work Experience', max_length=2, choices=EXPERIENCE_TYPE, default=0)
    age = models.IntegerField('Age Scope', max_length=2, choices=AGE_SCOPE, default=0)
    sex = models.IntegerField('Sex', max_length=2, choices=SEX_TYPE, default=0)
    description = models.CharField('Description', max_length=2000)

    def __unicode__(self):
        return str(self.user.id) + '-' + self.user.email + '-' + self.activity.name

class Feedback(models.Model):
    """
    Feedback from visitor or member
    """
    TYPE = (
        (0, 'Suggest'),
        (1, 'Consult'),
        (2, 'Complain')
    )

    sender = models.CharField('Sender', max_length=50)
    email = models.CharField('Email', max_length=100)
    type = models.IntegerField('Type', max_length=2, choices=TYPE, default=0)
    subject = models.CharField('Subject', max_length=255)
    content = models.CharField('Content', max_length=2000)

class Announcement(AbstractModel):
    """
    Announcement for show in dashboard
    """
    subject = models.CharField('Subject', max_length=255)
    content = models.CharField('Content', max_length=10000)
    end_date = models.DateField('End Date', blank=True)

class FriendlyLink(models.Model):
    """
    Friend Link Model
    """
    name = models.CharField('Name', max_length=100)
    web_site = models.CharField('Web Site', max_length=100)
    is_active = models.BooleanField('Is Activated', default=True)


class Configuration(models.Model):
    hot_line_one = models.CharField('Hot Line 1', max_length=20)
    hot_line_two = models.CharField('Hot Line 2', max_length=20, blank=True)
    qq = models.CharField('QQ', max_length=50)


