# coding: utf-8
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime
import random
from tinymce.models import HTMLField
from wjzpw import settings
from wjzpw.settings import RESUME_NUMBER_FORMAT
from wjzpw.web.constant import EDUCATION_TYPE, EXPERIENCE_TYPE, SEX_TYPE, SALARY_TYPE, PERSON_ACTION_TYPE, COMPANY_ACTION_TYPE, JOB_STATE_TYPE

#  * Use south migration tool to generate the migration script.
#        manage.py schemamigration web --auto
#        manage.py migrate
from wjzpw.web.controllers.utils import get_tuple_value_from_key


COMPANY_SCOPE_TYPE = (
    (0, u'请选择'),
    (1, u'小于50人'),
    (2, u'50至150之间'),
    (3, u'150至500之间'),
    (4, u'大于500')
    )

COMPANY_NATURE = (
    ('', u'请选择'),
    (1, _(u'外资(欧美)')),
    (2, _(u'外资(非欧美)')),
    (3, _(u'合资(欧美)')),
    (4, _(u'合资(非欧美)')),
    (5, _(u'国企')),
    (6, _(u'民营公司')),
    (7, _(u'外企代表处')),
    (8, _(u'政府机关')),
    (9, _(u'事业单位')),
    (10, _(u'非盈利机构')),
    (11, _(u'其他性质'))
    )

JOB_TYPE = (
    (1, _(u'全职')),
    (2, _(u'兼职')),
    (3, _(u'实习')),
    (4, _(u'全职/兼职'))
    )

ATTENDANCE_TIME = (
    (1, _(u'随时到岗')),
    (2, _(u'三天内')),
    (3, _(u'两周内')),
    (4, _(u'一个月内')),
    (5, _(u'三个月内')),
    (6, _(u'待定'))
    )



class AbstractModel(models.Model):
    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

### Basic data
class Province(models.Model):
    """
    Province info.
    """
    class Meta:
        verbose_name = _(u"省份")
        verbose_name_plural = _(u"基础信息-省份列表")
        ordering = ("name",)
        get_latest_by = "name"

    PROVINCE_TYPE = (
        (0, _(u'省份')),
        (1, _(u'直辖市'))
        )
    type = models.IntegerField(u'省份类型', max_length=2, choices=PROVINCE_TYPE, default=0)
    code = models.CharField(u'代码', max_length=5, blank=True)
    spell = models.CharField(u'拼音', max_length=50, blank=False)
    name = models.CharField(u'名称', max_length=255, blank=False)
    def __unicode__(self):
        return self.name

class City(models.Model):
    """
    City info.
    """
    class Meta:
        verbose_name_plural = _(u"基础信息-城市列表")
        verbose_name = _(u"城市")

    CITY_TYPE = (
        (0, 'City'),
        (1, 'Area')
        )
    type = models.IntegerField(u'城市类型', max_length=2, choices=CITY_TYPE, default=0)
    code = models.CharField(u'代码', max_length=5, blank=True)
    spell = models.CharField(u'拼音', max_length=50, blank=False)
    name = models.CharField(u'名称', max_length=255, blank=False)
    province = models.ForeignKey(Province, name='province', verbose_name="省份")
    def __unicode__(self):
        return self.name

class Location(models.Model):
    """
    Location info.
    """
    class Meta:
        verbose_name_plural = _(u"基础信息-工作地列表")
        verbose_name = _(u"工作地")

    spell = models.CharField(u'拼音', max_length=50, blank=False)
    name = models.CharField(u'名称', max_length=255, blank=False)
    order = models.IntegerField(u'顺序', max_length=2, default=0)
    def __unicode__(self):
        return self.name

class Industry(models.Model):
    """
    Industry info
    """
    class Meta:
        verbose_name_plural = _(u"基础信息-行业列表")
        verbose_name = _(u"行业")

    spell = models.CharField('拼音', max_length=50, blank=True)
    name = models.CharField('名称', max_length=255, blank=False)
    def __unicode__(self):
        return self.name

class Position(models.Model):
    """
    Position info separated by industry
    """
    class Meta:
        verbose_name_plural = _(u"基础信息-职位列表")
        verbose_name = _(u"职位")

    industry = models.ForeignKey(Industry, name='industry', verbose_name=u"行业类别", null=True, blank=True)
    spell = models.CharField(_(u'拼音'), max_length=50, blank=True)
    name = models.CharField(_(u'职位名称'), max_length=255)
    def __unicode__(self):
        return self.name

class Service(models.Model):
    class Meta:
        verbose_name_plural = _(u"公司-VIP服务列表")
        verbose_name = _(u"VIP服务")

    PERIOD_TYPE = (
        (0, u'免费'),
        (1, u'一个季度'),
        (2, u'半年'),
        (3, u'一年'),
        (4, u'一年(VIP)')
        )
    period = models.IntegerField(u'服务期限', max_length=2, choices=PERIOD_TYPE, default=0)
    price = models.IntegerField(u'价格', default=0)
    name = models.CharField(u'名称', max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class MajorType(models.Model):
    """
    Major info
    """
    class Meta:
        verbose_name = _(u"专业")
        verbose_name_plural = _(u"基础信息-专业列表")
        ordering = ("name",)
        get_latest_by = "name"
    spell = models.CharField(u'拼音', max_length=50, blank=True)
    name = models.CharField(u'名称', max_length=255, blank=False)
    def __unicode__(self):
        return self.name

### Account model group
class UserProfile(AbstractModel):
    """
    Profile for any users with access to the system.
    Points are updated here but can be computed by the awarded points - redeemed points. For performance.
    """
    class Meta:
        verbose_name_plural = _(u"系统-账户/公司列表")
        verbose_name = _(u"账户/公司")

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

    JOB_TYPE_TYPE = (
        (0, _(u'有工作经验的社会人士')),
        (1, _(u'在校生或者应届毕业生'))
        )

    WORK_YEARS_TYPE = (
        (0, _(u'1年')),
        (1, _(u'2年')),
        (2, _(u'3-5年')),
        (3, _(u'5-10年')),
        (4, _(u'10年以上'))
        )

    user = OneToOneField(User, verbose_name=u'Django用户')
    type = models.IntegerField(u'用户类型', max_length=2, choices=USER_TYPE, default=0, help_text=_(u'0:个人用户 1:企业用户 '))
    real_name = models.CharField(u'真实姓名', max_length=50, null=True, blank=False)
    gender = models.IntegerField(u'性别', max_length=2, choices=GENDER, default=2)
    birthday = models.DateField(u'生日', null=True, blank=True)
    census = models.ForeignKey(City, name='census', null=True, blank=True, verbose_name=u'户籍')
    location = models.ForeignKey(Location, name='location', null=True, blank=True, verbose_name=u'所在地')
    mobile_phone = models.CharField(u'手机/电话', max_length=20, default='')
    qq = models.CharField('QQ', max_length=20, null=True, blank=True)
    wedding = models.IntegerField(u'婚姻状况', max_length=2, choices=WEDDING_TYPE, default=0)
    stature = models.IntegerField(u'身高', null=True, blank=True)
    weight = models.IntegerField(u'体重', null=True, blank=True)
    job_state = models.IntegerField(u'求职状态', max_length=2, choices=JOB_STATE_TYPE, default=0)
    job_type = models.IntegerField(u'类型', max_length=2, choices=JOB_TYPE_TYPE, default=0)
    work_years = models.IntegerField(u'工作经验', max_length=2, choices=WORK_YEARS_TYPE, default=0, null=True, blank=True)
    points_balance = models.IntegerField(u'点数', default=0)
    cp_accept_notice = models.BooleanField(u'是否同意接收网站邮件', default=True)
    cp_name = models.CharField(u'公司名称', max_length=255, null=True)
    cp_license = models.CharField(u'营业执照', max_length=255, null=True, blank=True)
    cp_industry = models.ForeignKey(Industry, name='cp_industry', null=True, blank=True, verbose_name=u'公司所属行业')
    cp_nature = models.IntegerField(u'公司性质', choices=COMPANY_NATURE, null=True, blank=True)
    cp_scope = models.IntegerField(u'公司规模', max_length=2, choices=COMPANY_SCOPE_TYPE, default=0)
    cp_intro = models.CharField(u'公司简介', max_length=2000, null=True)
    cp_address = models.CharField(u'公司地址', max_length=2000, null=True, blank=True)
    cp_postcode = models.CharField(u'公司邮编', max_length=10, null=True, blank=True)
    cp_contact = models.CharField(u'联系人', max_length=50, null=True)
    cp_telephone = models.CharField(u'联系电话', max_length=15, null=True)
    cp_mobile_phone = models.CharField(u'联系人手机', max_length=15, null=True, blank=True)
    cp_fax = models.CharField(u'传真', max_length=15, null=True, blank=True)
    cp_website = models.CharField(u'网址', max_length=50, null=True, blank=True)
    cp_service = models.ForeignKey(Service, name='Service', null=True, blank=True, verbose_name=u'订购的服务')
    cp_service_begin = models.DateField(null=True, blank=True, verbose_name=u'服务开始时间')
    cp_job_last_updated = models.DateField(u'发布工作最后更新时间', null=True, blank=True, help_text=u'检查代码中是否每次更新JOB的时候都更新了该字段')

    #For Restful
    access_token = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    expires = models.IntegerField(null=True, blank=True)

    #    objects = UserProfileManager()
    def is_company(self): return self.type == 1

    def __unicode__(self):
        return self.user.username + "-" + self.user.email + "-" + (u'公司' if self.is_company() else u'求职者')

class Resume(AbstractModel):
    """
    个人简历
    """
    class Meta:
        verbose_name_plural = _(u"用户-简历列表")
        verbose_name = _(u"简历")

    user_profile = models.ForeignKey(UserProfile, name='user_profile', verbose_name=u"求职者")
    resume_name = models.CharField(_(u'简历名称'), max_length=100, default=_(u'我的简历'))
    job_type = models.IntegerField(_(u'职位类型'), max_length=2, choices=JOB_TYPE, default=1)
    industry = models.ForeignKey(Industry, name='industry', help_text=_(u'期望行业'), verbose_name=u"行业")
    location = models.ForeignKey(Location, name='location', help_text=_(u'期望工作地点'), verbose_name=u"工作地")
    is_supply_house = models.BooleanField(_(u'是否提供住房'), default=False)
    salary = models.IntegerField(_(u'待遇要求'), choices=SALARY_TYPE, default=0)
    attendance_time = models.IntegerField(_(u'到岗时间'), choices=ATTENDANCE_TIME, default=1)
    avatar = models.ImageField(_(u'简历头像'), upload_to='static/upload/avatars', null=True, blank=True)
    self_desc = models.CharField(_(u'自我评价'), max_length=2000, null=True, blank=True)

    def sex_str(self):
        return get_tuple_value_from_key(SEX_TYPE, self.user_profile.gender)

    def salary_str(self):
        return get_tuple_value_from_key(SALARY_TYPE, self.salary)

    def edu_background_str(self):
        return get_tuple_value_from_key(EDUCATION_TYPE, self.eduexperience_set.get().edu_background)

    def position_str(self):
        temp = "";
        for position in self.resumepositionr_set.all():
            temp = (", " if temp else "") + position.position.name
        return temp if temp else None

    def NO_str(self):
        return RESUME_NUMBER_FORMAT % self.id


    def __unicode__(self):
        return self.user_profile.user.username + "-" + self.resume_name

class ResumePositionR(AbstractModel):
    """
    Resume - position relation
    """
    resume = models.ForeignKey(Resume, name='resume')
    position = models.ForeignKey(Position, name='position')


class EduExperience(AbstractModel):
    """
    教育背景，最高学历
    """
    class Meta:
        verbose_name_plural = _(u"用户-教育背景列表")
        verbose_name = _(u"教育背景")

    resume = models.ForeignKey(Resume, name='resume')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100, null=True, blank=True)
    major_type = models.ForeignKey(MajorType, name='major_type', null=True, blank=True)
    edu_background = models.IntegerField(u'学历', max_length=2, choices=EDUCATION_TYPE, default=None)
    major_desc = models.CharField(max_length=2000, null=True, blank=True)
    is_foreign = models.BooleanField(u'是否是海外经历', default=False)

    def __unicode__(self):
        return self.resume.user_profile.user.username

class WorkExperience(AbstractModel):
    """
    工作经历
    """
    class Meta:
        verbose_name_plural = _(u"用户-工作经验列表")
        verbose_name = _(u"工作经验")

    resume = models.ForeignKey(Resume, name='resume')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    company_name = models.CharField(u'公司名', max_length=255)
    industry = models.ForeignKey(Industry, name='industry', help_text=_(u'行业'))
    scope = models.IntegerField(u'公司规模', max_length=2, choices=COMPANY_SCOPE_TYPE, default=0)
    nature = models.IntegerField(u'公司性质', choices=COMPANY_NATURE, default=None)
    department = models.CharField(u'部门', max_length=250)
    position = models.CharField(u'职位', max_length=250)
    work_desc = models.CharField(u'工作描述', max_length=2000)

    def __unicode__(self):
        return self.resume.user_profile.user.username

### Common service
class Job(AbstractModel):
    """
    岗位实体
    """
    class Meta:
        verbose_name_plural = _(u"公司-发布职位列表")
        verbose_name = _(u"发布的职位")

    AGE_SCOPE = (
        (0, u'不限'),
        (1, u'小于20'),
        (2, u'20至30'),
        (3, u'30至35'),
        (4, u'35以上')
        )

    company = models.ForeignKey(UserProfile, name='Company', verbose_name=u"公司")
    name = models.CharField(u'职位名称', max_length=255)
    job_type = models.IntegerField(u'职位类型', max_length=2, choices=JOB_TYPE, default=1)
    salary = models.IntegerField(_(u'薪水'), choices=SALARY_TYPE, default=0)
    department = models.CharField(u'部门', max_length=255, null=True, blank=True)
    number = models.IntegerField(u'招聘人数', null=True, blank=True)
    end_date = models.DateField(u'结束日期', null=True, blank=True)
    location = models.ForeignKey(Location, help_text=_(u'工作地点'), name='location', verbose_name=u"工作地点")
    edu_background = models.IntegerField(u'教育背景', max_length=2, choices=EDUCATION_TYPE, default='')
    work_experience = models.IntegerField(u'工作经验', max_length=2, choices=EXPERIENCE_TYPE, default=0)
    age = models.IntegerField(u'年龄要求', max_length=2, choices=AGE_SCOPE, default=0)
    sex = models.IntegerField(u'性别', max_length=2, choices=SEX_TYPE, default=0)
    description = models.CharField(u'描述', max_length=2000)

    def __unicode__(self):
        return self.company.cp_name + u'-' + self.name

    def work_experience_str(self):
        return get_tuple_value_from_key(EXPERIENCE_TYPE, self.work_experience)

    def sex_str(self):
        return get_tuple_value_from_key(SEX_TYPE, self.sex)

    def salary_str(self):
        return get_tuple_value_from_key(SALARY_TYPE, self.salary)

class UserJobR(AbstractModel):
    """
    用户收藏或者投递的工作列表
    """
    class Meta:
        verbose_name_plural = _(u"用户-收藏或者投递的工作列表")
        verbose_name = _(u"收藏或者投递的工作")

    user_profile = models.ForeignKey(UserProfile, name='user_profile', verbose_name=u"收藏者")
    job = models.ForeignKey(Job, name='job', verbose_name=u"收藏的工作")
    type = models.CharField(_(u'类型'), choices=PERSON_ACTION_TYPE, max_length=20)

    def __unicode__(self):
        return self.user_profile.user.username + ' - ' + self.job.name

class CompanyResumeR(AbstractModel):
    """
    公司收藏或者邀请的简历列表
    """
    class Meta:
        verbose_name_plural = _(u"公司-收藏或者邀请的简历列表")
        verbose_name = _(u"收藏或者邀请的简历")

    user_profile = models.ForeignKey(UserProfile, name='user_profile')
    resume = models.ForeignKey(Resume, name='resume')
    type = models.CharField(_(u'类型'), choices=COMPANY_ACTION_TYPE, max_length=20)

### Vip service
class PictureAdv(AbstractModel):
    """
    Picture advertisement
    """
    class Meta:
        verbose_name_plural = _(u"公司-图片广告列表")
        verbose_name = _(u"图片广告")

    IMG_ADV_TYPE = (
        (0, _(u'未指定')),
        (1, _(u'显示在首页'))
        )

    title = models.CharField(_(u'主题'), max_length=255)
    company = models.ForeignKey(UserProfile, name='Company', help_text=_(u'必须选择公司而非个人'), verbose_name=u'公司')
    type = models.IntegerField(_(u'广告用途'), max_length=2, choices=IMG_ADV_TYPE, default=0)
    start_date = models.DateField(_(u'起始日期'), default=datetime.datetime.today())
    end_date = models.DateField(_(u'结束日期'))
    img = models.ImageField(_(u'上传图片'), upload_to='static/upload/adv_images')
    width = models.IntegerField(_(u'图片宽度'), null=True, blank=True, help_text=_(u'首页图片广告宽度尺寸分三种：161.5, 333, 1019'))
    height = models.IntegerField(_(u'图片高度'), null=True, blank=True)
    url = models.URLField(_(u'链接网址'), help_text=_(u'若为空，则自动跳转到当前公司的招聘主页'))
    order = models.IntegerField(_(u'显示顺序'), default=0)


### Client service
class Feedback(AbstractModel):
    """
    Feedback from visitor or member
    """
    class Meta:
        verbose_name_plural = _(u"系统-用户反馈列表")
        verbose_name = _(u"用户反馈")

    TYPE = (
        (0, u'建议'),
        (1, u'咨询'),
        (2, u'投诉')
        )

    sender = models.CharField(u'发送者', max_length=50)
    email = models.EmailField(u'电子邮件', blank=True)
    mobile = models.CharField(u'手机号', max_length=50, null=True, blank=True)
    type = models.IntegerField(u'类型', max_length=2, choices=TYPE, default=0)
    subject = models.CharField(u'主题', max_length=255)
    content = models.CharField(u'内容', max_length=2000, blank=True)

class Announcement(AbstractModel):
    """
    Announcement for show in dashboard
    """
    class Meta:
        verbose_name_plural = _(u"系统-公告列表")
        verbose_name = _(u"公告")

    subject = models.CharField(u'主题', max_length=255)
    content = HTMLField(u'内容', max_length=10000)
    end_date = models.DateField(u'结束日期', blank=True, null=True, help_text=_(u'不填表示无失效日期'))

    def __unicode__(self):
        return self.subject

class FriendlyLink(AbstractModel):
    """
    Friend Link Model
    """
    class Meta:
        verbose_name_plural = _(u"系统-友情链接列表")
        verbose_name = _(u"友情链接")

    name = models.CharField(_(u'名称'), max_length=100)
    web_site = models.URLField(_(u'网站地址'), max_length=200)
    is_active = models.BooleanField(_(u'是否激活'), default=True)

    def __unicode__(self):
        return self.name

class ActiveToken(AbstractModel):
    """
    Store email tokens sent when user registers or changes email .
    """
    user = models.ForeignKey(User, null=True)
    token = models.CharField(max_length=256, null=True)
    new_email = models.EmailField(null=True, blank=True)
    password = models.CharField(_('password'), null=True, max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))

### Events summarize
class EventSearchJob(AbstractModel):
    pass

class EventSearchPerson(AbstractModel):
    pass

### Configuration
class Configuration(AbstractModel):
    class Meta:
        verbose_name_plural = _(u"系统-配置信息")
        verbose_name = _(u"配置")

    hot_line_one = models.CharField('Hot Line 1', max_length=20)
    hot_line_two = models.CharField('Hot Line 2', max_length=20, blank=True)
    qq = models.CharField('QQ', max_length=50)
    dashboard_image_1 = models.ImageField(u'首页图片1', upload_to='static/upload/config', help_text=u'首页公告下方的图片广告，建议275*140')

class FootItem(AbstractModel):
    '''
    用于显示页面尾部条目信息
    '''
    class Meta:
        verbose_name_plural = _(u"系统-尾部条目及自定义页面")
        verbose_name = _(u"尾部条目及自定义页面")

    name = models.CharField('条目名称', max_length=20)
    content = HTMLField('条目内容', max_length=10000)
    is_display = models.BooleanField('是否显示', default=True)
    order = models.IntegerField('排序号')
    def __unicode__(self):
        return self.name

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