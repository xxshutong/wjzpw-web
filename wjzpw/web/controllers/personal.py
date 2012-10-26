# coding: utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import  render_to_response, redirect
from django.utils import simplejson
from wjzpw import settings
from wjzpw.settings import SEARCH_JOB_SIZE
from wjzpw.web import models
from wjzpw.web.component import RequestContext
from wjzpw.web.forms.forms import PersonalRegForm, ResumeForm, EduExperienceForm, WorkExperienceForm, SearchJobForm
from wjzpw.web.models import Province, Job
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin

REGISTER_PAGE = "../views/personal/register.html"
RESUME_DETAIL_PAGE = "../views/personal/register_detail.html"
SEARCH_JOB_PAGE = "../views/personal/search_job.html"

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
            'form':form,
            'provinces':provinces,
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
            for i,work_experience in enumerate(work_experiences):
                work_experience_form = WorkExperienceForm(prefix=str(i+1), instance=work_experience)
                work_experience_forms.append(work_experience_form)
        else:
            work_experience_num = 1
            work_experience_form = WorkExperienceForm(prefix='1')
            work_experience_forms.append(work_experience_form)
    # Update resume detail or add new work experience
    else:
        selected_positions = []
        submit_type = request.POST.get('submit_type','submit')
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
            work_experience_forms.append(WorkExperienceForm(request.POST, prefix=i+1))
            i += 1

        # Submit resume detail
        if submit_type == 'submit':
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
        # Add new work experience
        elif submit_type == 'add_work_experience':
            work_experience_num += 1
            work_experience_forms.append(WorkExperienceForm(prefix=work_experience_num))
            position += str(work_experience_num-1)

    selected_positions = [resume_position.position for resume_position in models.ResumePositionR.objects.filter(resume=resume_form.instance)]
    return render_to_response(
        RESUME_DETAIL_PAGE, {}, RequestContext(request, {
            'resume_form': resume_form,
            'edu_experience_form': edu_experience_form,
            'work_experience_forms': work_experience_forms,
            'position': position,
            'work_experience_num': work_experience_num,
            'selected_positions': selected_positions
        }),
    )

def search_job(request):
    """
    找工作
    """
    job_list = None
    jobs = None
    if request.method == 'GET':
        search_form = SearchJobForm()
        job_list = Job.objects.filter(end_date__gt=datetime.datetime.now()).order_by('-updated_at')
    else:
        search_form = SearchJobForm(request.POST)
        if search_form.is_valid():
            filters = {'end_date__gt': datetime.datetime.now()}
            if search_form.cleaned_data['industry']:
                filters['company__cp_industry'] = search_form.cleaned_data['industry']
            if search_form.cleaned_data['location'] and search_form.cleaned_data['location'].id != 1:
                filters['location'] = search_form.cleaned_data['location']
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
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

    return render_to_response(
        SEARCH_JOB_PAGE, {}, RequestContext(request, {
            'jobs': jobs,
            'search_form': search_form,
            'menu': 'search_job'
        }
        ),
    )

def ajax_apply_job(request, job_id):
    """
    Apply a job by job ID
    """
    login_user = request.user
    if login_user and login_user.id:
        try:
            models.UserJobR.objects.get(user_profile=login_user.get_profile(), job=job_id, type='apply')
            data = {'result':'conflict'}
        except models.UserJobR.DoesNotExist:
            user_job_r = models.UserJobR(user_profile=login_user.get_profile(), job_id=job_id, type='apply')
            user_job_r.save()
            #TODO Send apply email to company
            data = {'result':'success'}
    else:
        data = {'result':'login_required'}
    return HttpResponse(simplejson.dumps(data))

def ajax_get_positions(request):
    """
    returns data displayed at autocomplete list -
    this function is accessed by AJAX calls
    """
    limit = 10
    query = request.GET.get('q', None)
    # it is up to you how query looks

    instances = models.Position.objects.filter(Q(name__icontains=query) | Q(spell__icontains=query)).order_by('name')[:limit]

    data = {}
    data['keys'] = [position.id for position in instances]
    data['values'] = [position.name for position in instances]

    data = simplejson.dumps(data)
    print data
    return HttpResponse(data, 'application/json')