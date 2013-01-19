# coding: utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponse, Http404
from django.shortcuts import  render_to_response, redirect, get_object_or_404
from django.template import loader
from django.utils import simplejson
from django.utils.html import strip_tags
from wjzpw import settings
from wjzpw.settings import SEARCH_JOB_SIZE
from wjzpw.web import models
from wjzpw.web.component import RequestContext
from wjzpw.web.controllers.utils import send_html_mail
from wjzpw.web.forms.forms import PersonalRegForm, ResumeForm, EduExperienceForm, WorkExperienceForm, SearchJobForm
from wjzpw.web.models import Province, Job
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin

REGISTER_PAGE = "../views/personal/register.html"
RESUME_DETAIL_PAGE = "../views/personal/register_detail.html"
SEARCH_JOB_PAGE = "../views/personal/search_job.html"
RESUME_VIEW_PAGE = "../views/personal/resume_view.html"
PERSONAL_DASHBOARD_PAGE = "../views/personal/dashboard.html"

def personal_register(request):
    """
    Personal registration
    """
    error = ''
    form = PersonalRegForm(request=request)

    if request.method == 'POST':
        # post register user
        form = PersonalRegForm(request.POST, request=request)
        if form.is_valid():
            user_profile = form.save(**form.cleaned_data)

            # Login automatically
            user = authenticate(username=user_profile.user.username,
                password=form.cleaned_data.get('password', None))
            if user:
                if user.is_active:
                    if not user.is_staff and not user.is_superuser:
                        djlogin(request, user)
                        form.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                        return redirect('/personal/resume_detail/')
                    else:
                        error = u'用户名或密码错误。'
                else:
                    error = u'账户未被激活。'
            else:
                error = u'用户名或密码错误。'

    # go to register page
    provinces = Province.objects.all()
    return render_to_response(
        REGISTER_PAGE, {}, RequestContext(request, {
            'form': form,
            'provinces': provinces,
            'error': error
        }),
    )


@login_required
@transaction.commit_on_success
def resume_detail(request):
    """
    Resume detail
    """
    position = '#'
    work_experience_forms = []
    work_experience_num = int(request.POST.get('work_experience_num', 0))
    # 指定是否需要跳转到预览简历页面
    is_view = False
    # Show existing resume detail
    if request.method == 'GET':
        # Resume
        resumes = models.Resume.objects.filter(user_profile=request.user.get_profile())
        if resumes:
            resume_form = ResumeForm(instance=resumes[0])
        else:
            resume = models.Resume(user_profile=request.user.get_profile())
            resume_form = ResumeForm(instance=resume)

        # EduExperience
        edu_experiences = models.EduExperience.objects.filter(resume=resume_form.instance)
        if edu_experiences:
            edu_experience_form = EduExperienceForm(instance=edu_experiences[0])
        else:
            edu_experience = models.EduExperience(resume=resume_form.instance)
            edu_experience_form = EduExperienceForm(instance=edu_experience)

        # WorkExperience
        work_experiences = models.WorkExperience.objects.filter(resume=resume_form.instance).order_by('start_date')
        if work_experiences:
            work_experience_num = len(work_experiences)
            for i, work_experience in enumerate(work_experiences):
                work_experience_form = WorkExperienceForm(prefix=str(i + 1), instance=work_experience)
                work_experience_forms.append(work_experience_form)
        else:
            work_experience_num = 1
            work_experience_form = WorkExperienceForm(prefix='1')
            work_experience_forms.append(work_experience_form)
    # Update resume detail or add new work experience
    else:
        submit_type = request.POST.get('submit_type', 'submit')
        is_view = (submit_type == 'submit_and_view')
        # Resume
        resumes = models.Resume.objects.filter(user_profile=request.user.get_profile())
        if resumes:
            resume_form = ResumeForm(request.POST, request.FILES, instance=resumes[0])
        else:
            resume_form = ResumeForm(request.POST, request.FILES)
            # EduExperience
        edu_experiences = models.EduExperience.objects.filter(resume=resume_form.instance)
        if edu_experiences:
            edu_experience_form = EduExperienceForm(request.POST, instance=edu_experiences[0])
        else:
            edu_experience_form = EduExperienceForm(request.POST)

        # WorkExperience
        i = 0
        while i < work_experience_num:
            work_experience_forms.append(WorkExperienceForm(request.POST, prefix=i + 1))
            i += 1

        # Submit resume detail
        if submit_type == 'submit' or submit_type == 'submit_and_view':
            multiple_work_result = True
            for work_experience_form in work_experience_forms:
                multiple_work_result = multiple_work_result and work_experience_form.is_valid()
            if resume_form.is_valid()\
               and edu_experience_form.is_valid()\
            and multiple_work_result:
                resume_form.save(**resume_form.cleaned_data)
                edu_experience_form.instance.resume = resume_form.instance
                edu_experience_form.save(**edu_experience_form.cleaned_data)
                models.WorkExperience.objects.filter(resume=resume_form.instance).delete()
                for work_experience_form in work_experience_forms:
                    work_experience_form.instance.resume = resume_form.instance
                    work_experience_form.save(**work_experience_form.cleaned_data)
            else:
                is_view = False
        # Add new work experience
        elif submit_type == 'add_work_experience':
            work_experience_num += 1
            work_experience_forms.append(WorkExperienceForm(prefix=work_experience_num))
            position += str(work_experience_num - 1)

    selected_positions = [resume_position.position for resume_position in
                          models.ResumePositionR.objects.filter(resume=resume_form.instance)]
    return render_to_response(
        RESUME_DETAIL_PAGE, {}, RequestContext(request, {
            'resume_form': resume_form,
            'edu_experience_form': edu_experience_form,
            'work_experience_forms': work_experience_forms,
            'position': position,
            'work_experience_num': work_experience_num,
            'selected_positions': selected_positions,
            'is_view': is_view
        }),
    )


def resume_view(request, resume_id):
    """
    预览、展示简历
    """
    resume_kwargs = prepare_resume_parameters(request, resume_id);
    return render_to_response(
        RESUME_VIEW_PAGE, {}, RequestContext(request, resume_kwargs),
    )

def prepare_resume_parameters(request, resume_id):
    resume = get_object_or_404(models.Resume, pk=resume_id)
    edu_experience = get_object_or_404(models.EduExperience, resume=resume)
    resume_position_r = models.ResumePositionR.objects.filter(resume=resume)
    work_experiences = models.WorkExperience.objects.filter(resume=resume).order_by('-start_date')
    # 判断是否可以访问简历的联系方式
    have_access_contact = False
    if request.user.is_active and (request.user.get_profile() == resume.user_profile
                                   or request.user.get_profile().cp_service):
        have_access_contact = True
    return {
        'resume': resume,
        'edu_experience': edu_experience,
        'resume_position_r': resume_position_r,
        'work_experiences': work_experiences,
        'have_access_contact': have_access_contact
    }


def search_job(request, is_vip=''):
    """
    找工作，is_vip主要用于页面点击更多VIP招聘的时候传输过来的
    """
    job_list = None
    records = None
    if request.method == 'GET':
        search_form = SearchJobForm(initial={'is_vip': ('true' if is_vip else 'false')})
        job_list = Job.objects.filter(end_date__gt=datetime.datetime.now()).order_by('-updated_at')
    else:
        search_form = SearchJobForm(request.POST)
        if search_form.is_valid():
            filters = {'end_date__gt': datetime.datetime.now()}
            if search_form.cleaned_data['industry']:
                filters['company__cp_industry'] = search_form.cleaned_data['industry']
            if search_form.cleaned_data['location'] and search_form.cleaned_data['location'].id != 1:
                filters['location'] = search_form.cleaned_data['location']
            if search_form.cleaned_data['is_vip'] and search_form.cleaned_data['is_vip'] == 'true':
                filters['company__cp_service__period__gt'] = 0
            if search_form.cleaned_data['filter_str']:
                if search_form.cleaned_data['type'] == '0':
                    filters['name__contains'] = search_form.cleaned_data['filter_str']
                else:
                    filters['company__cp_name__contains'] = search_form.cleaned_data['filter_str']
            job_list = Job.objects.filter(**filters).order_by('-updated_at')

    if job_list:
        paginator = Paginator(job_list, SEARCH_JOB_SIZE)
        page = request.GET.get('page', 1)
        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            records = paginator.page(1)
        except EmptyPage:
            records = paginator.page(paginator.num_pages)

    return render_to_response(
        SEARCH_JOB_PAGE, {}, RequestContext(request, {
            'records': records,
            'search_form': search_form,
            'menu': 'search_job'
        }
        ),
    )

@transaction.commit_on_success
def ajax_apply_job(request, job_id, is_store=False):
    """
    Apply a job by job ID
    """
    action_type = "store" if is_store else "apply";
    login_user = request.user
    if login_user and login_user.id:
        if login_user.get_profile().type == 1:
            data = {'result': 'type_error'} # Company cannot apply a job
        else:
            try:
                models.UserJobR.objects.get(user_profile=login_user.get_profile(), job=job_id, type=action_type)
                data = {'result': 'conflict'}
            except models.UserJobR.DoesNotExist:
                user_job_r = models.UserJobR(user_profile=login_user.get_profile(), job_id=job_id, type=action_type)
                user_job_r.save()
                if not is_store:
                    # 发送申请工作邮件
                    send_apply_email(request, login_user, job_id)
                data = {'result': 'success'}
    else:
        data = {'result': 'login_required'}
    return HttpResponse(simplejson.dumps(data))

def send_apply_email(request, login_user, job_id):
    """
    发送申请工作邮件
    """
    job = get_object_or_404(models.Job, pk=job_id)
    resume = models.Resume.objects.get(user_profile=login_user.get_profile())
    resume_kwargs = prepare_resume_parameters(request, resume.id);
    html_content = loader.render_to_string(RESUME_VIEW_PAGE, resume_kwargs)
    text_content = strip_tags(html_content)
    try:
        result = send_html_mail(
            u'(wj-zpw.com)申请贵公司%s (%s)' % (job.name, job.location),
            text_content,
            html_content,
            (u'吴江招聘网-' + login_user.get_profile().real_name),
            [job.company.user.email,]
        )
        if result != 1:
            raise Exception('Send email failed.');
    except Exception, e:
        raise Exception('Send email failed-> %s' % e)

def ajax_store_job(request, job_id):
    """
    Store a job by job ID
    """
    return ajax_apply_job(request, job_id, is_store=True)


def ajax_get_positions(request):
    """
    returns data displayed at autocomplete list -
    this function is accessed by AJAX calls
    """
    limit = 10
    query = request.GET.get('q', None)
    # it is up to you how query looks

    instances = models.Position.objects.filter(Q(name__icontains=query) | Q(spell__icontains=query)).order_by('name')[
                :limit]

    data = {}
    data['keys'] = [position.id for position in instances]
    data['values'] = [position.name for position in instances]

    data = simplejson.dumps(data)
    print data
    return HttpResponse(data, 'application/json')


@login_required
def dashboard(request):
    """
    Navigate to company dashboard page
    """
    login_user = request.user
    if login_user and login_user.id:
        if login_user.get_profile().type == 0:
            store_list = models.UserJobR.objects.filter(user_profile=login_user.get_profile(),
                type='store').order_by('-updated_at')
            apply_list = models.UserJobR.objects.filter(user_profile=login_user.get_profile(),
                type='apply').order_by('-updated_at')
            return render_to_response(
                PERSONAL_DASHBOARD_PAGE, {}, RequestContext(request, {
                    'store_list': store_list,
                    'apply_list': apply_list
                }
                ),
            )
    raise Http404