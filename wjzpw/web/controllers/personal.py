from django.db import transaction
from django.shortcuts import  render_to_response
from django.template.context import RequestContext
from wjzpw.web import models
from wjzpw.web.forms import PersonalRegForm, ResumeForm, EduExperienceForm, WorkExperienceForm
from wjzpw.web.models import Province

REGISTER_PAGE = "../views/personal/register.html"
RESUME_DETAIL_PAGE = "../views/personal/register_detail.html"

def personal_register(request):
    """
    Personal registration
    """
    form = PersonalRegForm(request=request)

    if request.method == 'POST':
        # post register user
        form = PersonalRegForm(request.POST, request=request)
        if form.is_valid():
            form.save(**form.cleaned_data)

    # go to register page
    provinces = Province.objects.all()
    return render_to_response(
        REGISTER_PAGE, {}, RequestContext(request, {
            'form':form,
            'provinces':provinces
        }),
    )

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
        work_experience_num = 1
        resume_form = ResumeForm()
        edu_experience_form = EduExperienceForm()
        work_experience_form = WorkExperienceForm(prefix='1')
        work_experience_forms.append(work_experience_form)
    # Update resume detail or add new work experience
    else:
        submit_type = request.POST.get('submit_type','submit')
        resume_form = ResumeForm(request.POST)
        edu_experience_form = EduExperienceForm(request.POST)
        i = 0
        while i < work_experience_num:
            work_experience_forms.append(WorkExperienceForm(request.POST, prefix=i+1))
            i += 1

        # Submit resume detail
        if submit_type == 'submit':
            if resume_form.is_valid()\
                and edu_experience_form.is_valid()\
                    and work_experience_form.is_valid():
                resume_form.save()
                edu_experience_form.save()
                work_experience_form.save()
        # Add new work experience
        elif submit_type == 'add_work_experience':
            work_experience_num += 1
            work_experience_forms.append(WorkExperienceForm(prefix=work_experience_num))
            position += str(work_experience_num-1)

    return render_to_response(
        RESUME_DETAIL_PAGE, {}, RequestContext(request, {
            'resume_form': resume_form,
            'edu_experience_form': edu_experience_form,
            'work_experience_forms': work_experience_forms,
            'position': position,
            'work_experience_num': work_experience_num
        }),
    )