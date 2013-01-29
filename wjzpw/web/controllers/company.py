# coding: utf-8
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils import simplejson
from wjzpw import settings
from wjzpw.settings import SEARCH_RESUME_SIZE
from wjzpw.web import models
from wjzpw.web.component import RequestContext
from wjzpw.web.forms.company import CompanyRegForm, JobForm

from django.contrib.auth import login as djlogin
from wjzpw.web.forms.forms import SearchResumeForm
from wjzpw.web.models import Resume, ResumePositionR

REGISTER_PAGE = "../views/company/register.html"
ADD_JOB_PAGE = "../views/company/add_job.html"
SEARCH_RESUME_PAGE = "../views/company/search_resume.html"
COMPANY_DASHBOARD_PAGE = "../views/company/dashboard.html"
COMPANY_DETAIL_PAGE = "../views/company/company_detail.html"
JOB_DETAIL_PAGE = "../views/company/job_detail.html"

def company_register(request):
    """
    Personal registration
    """
    error = ''
    form = CompanyRegForm(request=request)

    if request.method == 'POST':
        # post register company
        form = CompanyRegForm(request.POST, request=request)
        if form.is_valid():
            user_profile = form.save(**form.cleaned_data)

            # Login automatically
            user = authenticate(username=user_profile.user.username,
                password=form.cleaned_data.get('password', None))
            if user.is_active:
                djlogin(request, user)
                form.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                return redirect('/')
            else:
                error = u'账户未被激活。'

    # go to register page
    return render_to_response(
        REGISTER_PAGE, {}, RequestContext(request, {
            'form': form,
            'error': error
        }),
    )


@login_required
def add_job(request):
    """
    Add new job for company
    """
    error = ''
    if request.method == 'GET':
        form = JobForm()
    else:
        form = JobForm(request.POST)
        if form.is_valid():
            saved_job = form.save(request.user.get_profile(), **form.cleaned_data)
            return redirect('/company/job/%s' % saved_job.id)
    return render_to_response(
        ADD_JOB_PAGE, {}, RequestContext(request, {
            'form': form,
            'error': error,
            'menu': 'add_job'
        }),
    )


def search_person(request):
    """
    找人才
    """
    resume_list = None
    records = None
    if request.method == 'GET':
        search_form = SearchResumeForm()
        resume_list = Resume.objects.all().order_by('-updated_at')
    else:
        search_form = SearchResumeForm(request.POST)
        if search_form.is_valid():
            filters = {}
            if search_form.cleaned_data['industry']:
                filters['industry'] = search_form.cleaned_data['industry']
            if search_form.cleaned_data['location'] and search_form.cleaned_data['location'].id != 1:
                filters['location'] = search_form.cleaned_data['location']
            if search_form.cleaned_data['attendance_time'] and search_form.cleaned_data['attendance_time'] != '0':
                filters['attendance_time'] = search_form.cleaned_data['attendance_time']
            if search_form.cleaned_data['job_type']:
                filters['job_type'] = search_form.cleaned_data['job_type']
            if search_form.cleaned_data['filter_str']:
                if search_form.cleaned_data['type'] == '0':
                    filters['id__in'] = ResumePositionR.objects.filter(
                        position__name__contains=search_form.cleaned_data['filter_str']).values("resume_id")
                else:
                    filters['user_profile__real_name__contains'] = search_form.cleaned_data['filter_str']
            resume_list = Resume.objects.filter(**filters).order_by('-updated_at')

    if resume_list:
        paginator = Paginator(resume_list, SEARCH_RESUME_SIZE)
        page = request.GET.get('page', 1)
        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            records = paginator.page(1)
        except EmptyPage:
            records = paginator.page(paginator.num_pages)

    return render_to_response(
        SEARCH_RESUME_PAGE, {}, RequestContext(request, {
            'records': records,
            'search_form': search_form,
            'menu': 'search_person'
        }
        ),
    )


def ajax_invite_resume(request, resume_id, is_store=False):
    """
    Invite a resume by resume ID
    """
    action_type = "store" if is_store else "invite";
    login_user = request.user
    if login_user and login_user.id:
        if login_user.get_profile().type == 0:
            data = {'result': 'type_error'}
        else:
            try:
                models.CompanyResumeR.objects.get(user_profile=login_user.get_profile(), resume=resume_id,
                    type=action_type)
                data = {'result': 'conflict'}
            except models.CompanyResumeR.DoesNotExist:
                company_resume_r = models.CompanyResumeR(user_profile=login_user.get_profile(), resume_id=resume_id,
                    type=action_type)
                company_resume_r.save()
                if not is_store:
                    #TODO Send invite email to person
                    pass
                data = {'result': 'success'}
    else:
        data = {'result': 'login_required'}
    return HttpResponse(simplejson.dumps(data))


def ajax_store_resume(request, resume_id):
    """
    Store a resume by resume ID
    """
    return ajax_invite_resume(request, resume_id, is_store=True)


@login_required
def dashboard(request):
    """
    Navigate to company dashboard page
    """
    login_user = request.user
    if login_user and login_user.id:
        if login_user.get_profile().type == 1:
            store_list = models.CompanyResumeR.objects.filter(user_profile=login_user.get_profile(),
                type='store').order_by('-updated_at')
            invite_list = models.CompanyResumeR.objects.filter(user_profile=login_user.get_profile(),
                type='invite').order_by('-updated_at')
            return render_to_response(
                COMPANY_DASHBOARD_PAGE, {}, RequestContext(request, {
                    'store_list': store_list,
                    'invite_list': invite_list
                }
                ),
            )
    raise Http404

def company_detail(request, company_id):
    """
    Navigate to company detail page
    """
    filter = {'pk': company_id, 'type': 1}
    company = get_object_or_404(models.UserProfile, **filter)
    job_list = models.Job.objects.filter(company=company_id).order_by('-updated_at')
    return render_to_response(
        COMPANY_DETAIL_PAGE, {}, RequestContext(request, {
            'company': company,
            'job_list': job_list
        }),
    )

def job_detail(request, job_id):
    """
    Navigate to job detail page
    """
    job = get_object_or_404(models.Job, pk=job_id)
    job_list = models.Job.objects.filter(company=job.company.id).order_by('-updated_at')
    return render_to_response(
        JOB_DETAIL_PAGE, {}, RequestContext(request, {
            'job': job,
            'job_list': job_list
        })
    )