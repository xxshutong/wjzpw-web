# coding: utf-8
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect
from wjzpw import settings
from wjzpw.settings import SEARCH_RESUME_SIZE
from wjzpw.web.component import RequestContext
from wjzpw.web.forms.company import CompanyRegForm, JobForm

from django.contrib.auth import login as djlogin
from wjzpw.web.forms.forms import SearchResumeForm
from wjzpw.web.models import Resume, ResumePositionR

REGISTER_PAGE = "../views/company/register.html"
ADD_JOB_PAGE = "../views/company/add_job.html"
SEARCH_RESUME_PAGE = "../views/company/search_resume.html"

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
            'form':form,
            'error': error
        }),
    )

@login_required
def add_job(request):
    '''
    Add new job for company
    '''
    error = ''
    if request.method == 'GET':
        form = JobForm()
    else:
        form = JobForm(request.POST)
        if form.is_valid():
            form.save(request.user.get_profile(), **form.cleaned_data)
            #TODO redirect to job view page in future
    return render_to_response(
        ADD_JOB_PAGE, {}, RequestContext(request, {
            'form':form,
            'error': error,
            'menu': 'add_job'
        }),
    )


def search_person(request):
    """
    找人才
    """
    resume_list = None
    resumes = None
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
            if search_form.cleaned_data['attendance_time']:
                filters['attendance_time'] = search_form.cleaned_data['attendance_time']
            if search_form.cleaned_data['job_type']:
                filters['job_type'] = search_form.cleaned_data['job_type']
            if search_form.cleaned_data['filter_str']:
                if search_form.cleaned_data['type'] == '0':
                    filters['id__in'] = ResumePositionR.objects.filter(position__name__contains=search_form.cleaned_data['filter_str']).values("resume_id")
                else:
                    filters['user_profile__real_name__contains'] = search_form.cleaned_data['filter_str']
            resume_list = Resume.objects.filter(**filters).order_by('-updated_at')

    if resume_list:
        paginator = Paginator(resume_list, SEARCH_RESUME_SIZE)
        page = request.GET.get('page', 1)
        try:
            resumes = paginator.page(page)
        except PageNotAnInteger:
            resumes = paginator.page(1)
        except EmptyPage:
            resumes = paginator.page(paginator.num_pages)

    return render_to_response(
        SEARCH_RESUME_PAGE, {}, RequestContext(request, {
            'resumes': resumes,
            'search_form': search_form,
            'menu': 'search_person'
        }
        ),
    )

