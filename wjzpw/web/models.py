# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Defines the model for Digido.
#
# NOTE!!
#  # DO NOT NAME attribute with "id" or "*_id". The publishing code will weed
#    those out as keys and not include them in the serialization.
#
#  * Use south migration tool to generate the migration script.
#        manage.py schemamigration web --auto
#        manage.py migrate
import datetime
import random
from wjzpw import settings
#from wjzpw.web.manager import UserProfileManager

class AbstractModel(models.Model):
    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

### Account model group
class Province(models.Model):
    """
    Province info.
    """
    class Meta:
        verbose_name = _(u"省份")
        verbose_name_plural = _(u"省份列表")
        ordering = ("name",)
        get_latest_by = "name"

    PROVINCE_TYPE = (
        (0, _(u'省份')),
        (1, _(u'直辖市'))
    )
    type = models.IntegerField('省份类型', max_length=2, choices=PROVINCE_TYPE, default=0)
    code = models.CharField('代码', max_length=5, blank=True)
    spell = models.CharField('拼音', max_length=50, blank=False)
    name = models.CharField('名称', max_length=255, blank=False)
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
    type = models.IntegerField('城市类型', max_length=2, choices=CITY_TYPE, default=0)
    code = models.CharField('代码', max_length=5, blank=True)
    spell = models.CharField('拼音', max_length=50, blank=False)
    name = models.CharField('名称', max_length=255, blank=False)
    province = models.ForeignKey(Province, name='province')
    def __unicode__(self):
        return self.name

class Location(models.Model):
    """
    Location info.
    """
    spell = models.CharField('拼音', max_length=50, blank=False)
    name = models.CharField('名称', max_length=255, blank=False)
    order = models.IntegerField('顺序', max_length=2, default=0)
    def __unicode__(self):
        return self.name

class Industry(models.Model):
    """
    Industry info
    """
    spell = models.CharField('拼音', max_length=50, blank=True)
    name = models.CharField('名称', max_length=255, blank=False)
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
    period = models.IntegerField('服务期限', max_length=2, choices=PERIOD_TYPE, default=0)
    price = models.IntegerField('价格', default=0)
    name = models.CharField('名称', max_length=255, blank=False)

class UserProfile(AbstractModel):
    """
    Profile for any users with access to the system.
    Points are updated here but can be computed by the awarded points - redeemed points. For performance.
    """
    USER_TYPE = (
        (0, _(u'个人用户')),
        (1, _(u'企业用户'))
    )

    GENDER = (
        (0, _(u'男')),
        (1, _(u'女')),
        (2, _(u'保密'))
    )

    WEDDING_TYPE = (
        (0, _(u'保密')),
        (1, _(u'已婚')),
        (2, _(u'未婚')),
        (3, _(u'离异'))
    )

    JOB_STATE_TYPE = (
        (0, _(u'目前处于离职状态，可立即上岗')),
        (1, _(u'目前在职，正考虑换个环境')),
        (2, _(u'对现有工作很满意，有更好机会才考虑')),
        (3, _(u'应届生')),
        (4, _(u'目前暂无跳槽打算'))
    )

    JOB_TYPE_TYPE = (
        (0, _(u'有工作经验的社会人才')),
        (1, _(u'在校生或者应届毕业生'))
    )

    WORK_YEARS_TYPE = (
        (0, _(u'1年')),
        (1, _(u'2年')),
        (2, _(u'3-5年')),
        (3, _(u'5-10年')),
        (4, _(u'10年以上'))
    )

    COMPANY_SCOPE_TYPE = (
        (0, '< 50'),
        (1, '50 < 150'),
        (2, '150 < 500'),
        (3, '> 500')
    )

    user = OneToOneField(User)
    type = models.IntegerField('User Type', max_length=2, choices=USER_TYPE, default=0)
    real_name = models.CharField('真实姓名', max_length=50, null=True, blank=False)
    gender = models.IntegerField('性别', max_length=2, choices=GENDER, default=2)
    birthday = models.DateField('生日', null=True, blank=True)
    census = models.ForeignKey(City, name='census')
    location = models.ForeignKey(Location, name='location')
    mobile_phone = models.CharField('手机/电话', max_length=20)
    qq = models.CharField('QQ', max_length=20)
    wedding = models.IntegerField('婚姻状况', max_length=2, choices=WEDDING_TYPE, default=0)
    stature = models.IntegerField('身高', null=True, blank=True)
    weight = models.IntegerField('体重', null=True, blank=True)
    job_state = models.IntegerField('求职状态', max_length=2, choices=JOB_STATE_TYPE, default=0)
    job_type = models.IntegerField('类型', max_length=2, choices=JOB_TYPE_TYPE, default=0)
    work_years = models.IntegerField('工作经验', max_length=2, choices=WORK_YEARS_TYPE, default=0, null=True, blank=True)
    points_balance = models.IntegerField('点数', default=0)
    cp_accept_notice = models.BooleanField('Accept Notice', default=True)
    cp_name = models.CharField('Company Name', max_length=255, null=True)
    cp_license = models.CharField('Business License', max_length=255, null=True)
    cp_industry = models.ForeignKey(Industry, name='Industry Type', null=True, blank=True)
    cp_scope = models.IntegerField('Company Scope', max_length=2, choices=COMPANY_SCOPE_TYPE, default=0)
    cp_intro = models.CharField('Company Intro', max_length=50, null=True)
    cp_address = models.CharField('Company Address', max_length=2000, null=True)
    cp_postcode = models.CharField('Address Postcode', max_length=10, null=True)
    cp_contact = models.CharField('Contact Name', max_length=50, null=True)
    cp_telephone = models.CharField('Contact Telephone', max_length=15, null=True, blank=True)
    cp_mobile_phone = models.CharField('Contact Mobile Phone', max_length=15, null=True, blank=True)
    cp_fax = models.CharField('Contact Fax', max_length=15, null=True, blank=True)
    cp_website = models.CharField('Web Site', max_length=50, null=True, blank=True)
    cp_service = models.ForeignKey(Service, name='Service', null=True, blank=True)
    cp_service_begin = models.DateField(null=True, blank=True)
#    is_active = models.BooleanField(_('active'), default=True, help_text=_("Designates whether this user should be treated as active. Unselect this instead of deleting accounts."))
#    last_login = models.DateTimeField(_('最后登陆时间'), default=datetime.datetime.now)
#    date_joined = models.DateTimeField(_('注册时间'), default=datetime.datetime.now)

    #For Restful
    access_token = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    expires = models.IntegerField(null=True, blank=True)

#    objects = UserProfileManager()

    def __unicode__(self):
        return self.user.username + "-" + self.user.email


### Common service
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

### Vip service
class PictureAdv(AbstractModel):
    """
    Picture advertisement
    """
    IMG_ADV_TYPE = (
        (0, _(u'未指定')),
        (1, _(u'显示在首页'))
    )

    title = models.CharField(_(u'主题'), max_length=255)
    company = models.ForeignKey(UserProfile, name='Company', help_text=_(u'必须选择公司而非个人'))
    type = models.IntegerField(_(u'广告用途'), max_length=2, choices=IMG_ADV_TYPE, default=0)
    start_date = models.DateField(_(u'起始日期'), default=datetime.datetime.today())
    end_date = models.DateField(_(u'结束日期'))
    img = models.ImageField(_(u'上传图片'), upload_to='adv_img')
    width = models.IntegerField(_(u'图片宽度'), null=True, blank=True)
    height = models.IntegerField(_(u'图片高度'), null=True, blank=True)
    url = models.URLField(_(u'链接网址'), help_text=_(u'若为空，则自动跳转到当前公司的招聘主页'))
    order = models.IntegerField(_(u'显示顺序'), default=0)


### Client service
class Feedback(AbstractModel):
    """
    Feedback from visitor or member
    """
    TYPE = (
        (0, 'Suggest'),
        (1, 'Consult'),
        (2, 'Complain')
    )

    sender = models.CharField('Sender', max_length=50)
    email = models.EmailField(_('电子邮件'), blank=True)
    type = models.IntegerField('Type', max_length=2, choices=TYPE, default=0)
    subject = models.CharField('Subject', max_length=255)
    content = models.CharField('Content', max_length=2000, blank=True)

class Announcement(AbstractModel):
    """
    Announcement for show in dashboard
    """
    subject = models.CharField('Subject', max_length=255)
    content = models.CharField('Content', max_length=10000)
    end_date = models.DateField('End Date', blank=True)

class FriendlyLink(AbstractModel):
    """
    Friend Link Model
    """
    name = models.CharField(_(u'名称'), max_length=100)
    web_site = models.URLField(_(u'网站地址'), max_length=200)
    is_active = models.BooleanField(_(u'是否激活'), default=True)

### Events summarize
class EventSearchJob(AbstractModel):
    pass

class EventSearchPerson(AbstractModel):
    pass

### Configuration
class Configuration(AbstractModel):
    hot_line_one = models.CharField('Hot Line 1', max_length=20)
    hot_line_two = models.CharField('Hot Line 2', max_length=20, blank=True)
    qq = models.CharField('QQ', max_length=50)

### Others
class Captcha:
    """
    验证码
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.create()

    @staticmethod
    def text():
        return ''.join([random.choice(settings.LETTERS) for i in range(settings.LENGTH)])

    def get(self):
        return self.request.session.get(settings.NAME, '')

    def destroy(self):
        self.request.session[settings.NAME] = ''

    def create(self):
        self.request.session[settings.NAME] = self.text()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)