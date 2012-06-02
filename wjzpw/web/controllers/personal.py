# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import  render_to_response, redirect
from django.template.context import RequestContext
from django.utils import simplejson
from wjzpw import settings
from wjzpw.web import models
from wjzpw.web.forms.forms import PersonalRegForm, ResumeForm, EduExperienceForm, WorkExperienceForm
from wjzpw.web.models import Province
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin

REGISTER_PAGE = "../views/personal/register.html"
RESUME_DETAIL_PAGE = "../views/personal/register_detail.html"

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