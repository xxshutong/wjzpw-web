from django.shortcuts import  render_to_response
from django.template.context import RequestContext
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

def resume_detail(request):
    """
    Resume detail
    """
    if request.method == 'GET':
        resume_form = ResumeForm()
        edu_experience_form = EduExperienceForm()
        work_experience_form = WorkExperienceForm()
    else:
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume_form.save()

    return render_to_response(
        RESUME_DETAIL_PAGE, {}, RequestContext(request, {
            'resume_form': resume_form,
            'edu_experience_form': edu_experience_form,
            'work_experience_form': work_experience_form
        }),
    )