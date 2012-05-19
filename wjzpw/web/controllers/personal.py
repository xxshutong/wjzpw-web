from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import  render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
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
        resume = models.Resume.objects.get(user_profile=request.user.get_profile())

        work_experience_num = 1
        resume_form = ResumeForm()
        edu_experience_form = EduExperienceForm()
        work_experience_form = WorkExperienceForm(prefix='1')
        work_experience_forms.append(work_experience_form)
        selected_positions = [resume_position.position for resume_position in models.ResumePositionR.objects.filter(resume=resume)]
    # Update resume detail or add new work experience
    else:
        selected_positions = []
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