from django.shortcuts import  render_to_response
from django.template.context import RequestContext
from wjzpw.web.forms import PersonalRegForm
from wjzpw.web.models import Province

register_page = "../views/personal/register.html"

"""
Personal registration
"""
def register(request):
    form = PersonalRegForm(request=request)

    if request.method == 'POST':
        # post register user
        form = PersonalRegForm(request.POST, request=request)
        if form.is_valid():
            form.save(**form.cleaned_data)

    # go to register page
    provinces = Province.objects.all()
    return render_to_response(
        register_page, {}, RequestContext(request, {
            'form':form,
            'provinces':provinces
        }),
    )

