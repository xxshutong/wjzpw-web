# coding: utf-8
from StringIO import StringIO
import datetime
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import  render_to_response, redirect
from django.http import  HttpResponse
from random import choice
import Image
import ImageDraw
import json
from wjzpw import settings
from wjzpw.web import models
from wjzpw.web.component import RequestContext
from wjzpw.web.constant import EDUCATION_TYPE
from wjzpw.web.controllers.utils import Utils, get_tuple_value_from_key, send_html_mail, generate_valid_string, generate_password
from wjzpw.web.forms.forms import LoginForm, FeedbackForm, SearchJobForm
from wjzpw.web.models import City, Captcha, Announcement, FriendlyLink, Feedback, Job, UserProfile, Resume
from django.utils import simplejson
from django.contrib.auth import logout as djlogout, authenticate
from django.contrib.auth import login as djlogin
from django.utils.translation import ugettext_lazy as _

DASHBOARD_PAGE = "../views/dashboard.html"
LOGIN_PAGE = "../views/login.html"
FEEDBACK_PAGE = "../views/feedback.html"

def dashboard(request):
    """ Renders Dashboard/Home page. """
    login_form = LoginForm(request=request)
    search_job_form = SearchJobForm()

    # 公告
    announce_list = Announcement.objects.filter(Q(end_date__gte=datetime.datetime.today()) | Q(end_date=None)).order_by('-updated_at')[:settings.ANNOUNCEMENT_LIMIT_SIZE]

    # 友情链接
    link_list = FriendlyLink.objects.filter(is_active=True).order_by('updated_at')

    # VIP企业招聘
    vip_company_list = UserProfile.objects.filter(type=1).exclude(cp_service__period=0).order_by('-cp_job_last_updated')[:settings.DASHBOARD_VIP_SIZE]
    vip_job_list = Job.objects.filter(company__in=vip_company_list).order_by('-company__cp_job_last_updated', '-updated_at')
    vip_company_job_list = gather_job_info(vip_job_list)

    # 最新企业招聘
    company_list = UserProfile.objects.filter(type=1).order_by('-cp_job_last_updated')[:settings.DASHBOARD_JOB_SIZE]
    job_list = Job.objects.filter(company__in=company_list).order_by('-company__cp_job_last_updated', '-updated_at')
    company_job_list = gather_job_info(job_list)

    # 最新人才信息
    person_list = UserProfile.objects.filter(type=0, id__in=Resume.objects.all().values('user_profile__id')).order_by('-created_at')[:settings.DASHBOARD_PERSON_SIZE]
    person_obj_list = gather_person_info(person_list)

    return render_to_response(
        DASHBOARD_PAGE, {}, RequestContext(request, {
            'login_form':login_form,
            'search_job_form': search_job_form,
            'announce_list':announce_list,
            'link_list':link_list,
            'vip_company_job_list':vip_company_job_list,
            'company_job_list':company_job_list,
            'person_obj_list': person_obj_list,
            'menu': 'dashboard'
        }),
    )

def login(request, info=None):
    """
    Logs User in.
    """
    error = ''
    if request.method == 'GET':
        login_form = LoginForm(request=request)
    else:
        login_form = LoginForm(request.POST, request=request)

        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data.get('username', None),
                password=login_form.cleaned_data.get('password', None))
            if user:
                if user.is_active:
                    if not user.is_staff and not user.is_superuser:
                        djlogin(request, user)
                        login_form.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                        return redirect('/')
                    else:
                        error = _(u'用户名或密码错误。')
                else:
                    error = _(u'账户未被激活。')
            else:
                error = _(u'用户名或密码错误。')
    return render_to_response(
        LOGIN_PAGE, {}, RequestContext(request, {
            'login_form':login_form,
            'info': info,
            'error': error
        }
        ),
    )

def logout(request):
    """
    Logs user out.
    """
    djlogout(request)
    return redirect('/')

def feedback(request):
    """ Renders Feedback page. """
    success = False
    if request.method == 'GET':
        if request.user.is_active:
            user_profile = request.user.get_profile()
            kwargs = {'sender':(user_profile.real_name or user_profile.cp_name),'email':request.user.email}
            instance = Feedback(**kwargs)
            feedback_from = FeedbackForm(instance=instance)
        else:
            feedback_from = FeedbackForm()
    else:
        feedback_from = FeedbackForm(request.POST)
        if feedback_from.is_valid():
            feedback_from.save(**feedback_from.cleaned_data)
            success = True

    return render_to_response(
        FEEDBACK_PAGE, {}, RequestContext(request, {
            'feedback_from': feedback_from,
            'success': success,
            'menu': 'feedback'
            }),
    )

def ajax_get_city_by_province(request, province_id):
    """
    Get city list by province ID
    """
    data = ''
    if request.method == 'GET':
        city_list = City.objects.filter(province__id = int(province_id))
        data = simplejson.dumps(Utils.generate_options(city_list))
        print data
    return HttpResponse(data, 'application/json')

def verify_image(request):
    """
    Get verify code
    """
    captcha_text = Captcha(request).get()
    response = HttpResponse()
    if captcha_text:
        image = Image.new("RGBA", (settings.LENGTH * settings.FONT_SIZE - 26, settings.FONT_SIZE), (0,0,0,0))
        canvas = ImageDraw.Draw(image)

        for i in range(0, len(captcha_text)):
            horizon = 1; verticality  = -1
            if i>0: horizon = (settings.FONT_SIZE - 5) * i
            if i%2 == 0: verticality = 2
            canvas.text((horizon, verticality), captcha_text[i], fill = choice(settings.COLOURS))

        out = StringIO()
        image.save(out, "PNG")
        out.seek(0)
        response['Content-Type'] = 'image/png'
        response.write(out.read())

    return response

def ajax_forget_password(request):
    '''
    忘记密码
    '''
    email = request.GET.get('email_address', '')
    error = "Please input a correct email."
    user = None
    member = None
    if email:
        user = User.objects.filter(email=email)
        if user:
            user = user[0]
            member = models.UserProfile.objects.filter(user=user)
    if user and member:
        error = ''
        is_success = send_forgot_password_email(user, request)
        if not is_success:
            error = 'Send email failed.'

    return HttpResponse(json.dumps(error))

def activated_password(request, token=None):
    login_form = LoginForm(request)
    active_token = models.ActiveToken.objects.filter(Q(token=token), ~Q(password=None))
    if active_token:
        current_time = datetime.datetime.now()
        expire_time = current_time - datetime.timedelta(days=settings.EMAIL_EXPIRE_TIME)
        user = active_token[0].user
        e_active_token = active_token.filter(created_at__gte = expire_time)
        #Not Expire
        if e_active_token:
            password = active_token[0].password
            user.password = password
            user.save()
            models.ActiveToken.objects.filter(Q(user=user), ~Q(password=None)).delete()
            info = u'密码修改成功。'
        #Expire
        else:
            info = u"链接实效，系统自动重发，请重新查收邮件。"
            is_success = send_forgot_password_email(user, request)
            if not is_success:
                info = u'邮件发送失败。'
        return render_to_response(LOGIN_PAGE, {}, RequestContext(request, {'login_form':login_form, 'info':info}))

    else:
        return render_to_response('404.html', {}, RequestContext(request, {}))

def gather_job_info(job_list):
    """
    Group jobs by company one by one
    """
    company_job_list = []
    job_obj = {}
    prefix_company = None
    if job_list:
        for job in job_list:
            if job.company == prefix_company:
                job_obj['job_list'].append(job)
            else:
                if prefix_company:
                    job_obj['odd'] = len(company_job_list)/3%2 == 0
                    company_job_list.append(job_obj)
                job_obj['name'] = job.company.cp_name
                job_obj['id'] = job.company.id
                job_obj['job_list'] = []
                job_obj['job_list'].append(job)
            prefix_company = job.company
        job_obj['odd'] = len(company_job_list)/3%2 == 0
        company_job_list.append(job_obj)
    return company_job_list


def gather_person_info(person_list):
    """
    封装最新人才信息，供前台首页显示
    """
    person_obj_list = []
    person_obj = {}
    for person in person_list:
        person_obj['name'] = person.real_name
        person_obj['id'] = person.id
        edu_background = person.resume_set.all()[0].eduexperience_set.all()[0]
        person_obj['education'] = get_tuple_value_from_key(EDUCATION_TYPE, edu_background.edu_background)
        person_obj['major'] = edu_background.major
        person_obj_list.append(person_obj);
        person_obj['odd'] = len(person_obj_list)/3%2 == 0
        person_obj = {}
    return person_obj_list

def send_forgot_password_email(user, request):
    '''
    Send forget password email
    '''
    token = generate_valid_string()
    password = generate_password()
    user.set_password(password)
    hash_password = user.password
    url = "http://"+ request.META["HTTP_HOST"]+'/activated_password/%s/' % token
    try:
        send_html_mail(
            u'密码重置-吴江招聘网',
            (forgot_password_mail_template % ((user.get_profile().real_name if user.get_profile().real_name else user.get_profile().cp_name), password, url, settings.ADMIN_EMAIL)),
            settings.EMAIL_FROM_USER,
            [user.email,]
        )
    except Exception, e:
        print 'Send email failed-> %s' % e
        return False
    models.ActiveToken.objects.filter(Q(user=user), ~Q(password=None)).delete()
    kwargs = {}
    kwargs.update(token=token)
    kwargs.update(user=user)
    kwargs.update(password=hash_password)
    models.ActiveToken.objects.create(**kwargs)
    return True

forgot_password_mail_template = u'''
    <html>
    <head>
    </head>
        <body>
            <p>
                你好 %s, <br><br>
                这是你在吴江-招聘网的新密码.<br>
                新密码: %s<br>
                请点击下面的链接以激活你的新密码，并在激活后立马登陆修改成你想要的密码.<br>
                %s<br><br>
                如果你有任何疑问, 请联系 %s.<br><br>

                吴江-招聘网<br/><br/>

                本邮件由系统自动生成，请勿回复.
            </p>
        </body>
    </html>
'''