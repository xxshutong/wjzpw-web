# coding: utf-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from wjzpw.web.forms.company import CompanyRegForm

REGISTER_PAGE = "../views/company/register.html"

def company_register(request):
    """
    Personal registration
    """
    error = ''
    form = CompanyRegForm(request=request)

#    if request.method == 'POST':
#        # post register user
#        form = PersonalRegForm(request.POST, request=request)
#        if form.is_valid():
#            user_profile = form.save(**form.cleaned_data)
#
#            # Login automatically
#            user = authenticate(username=user_profile.user.username,
#                password=form.cleaned_data.get('password', None))
#            if user:
#                if user.is_active:
#                    if not user.is_staff and not user.is_superuser:
#                        djlogin(request, user)
#                        form.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
#                        return redirect('/personal/resume_detail/')
#                    else:
#                        error = u'用户名或密码错误。'
#                else:
#                    error = u'账户未被激活。'
#            else:
#                error = u'用户名或密码错误。'

    # go to register page
#    provinces = Province.objects.all()
    return render_to_response(
        REGISTER_PAGE, {}, RequestContext(request, {
            'form':form,
            'error': error
        }),
    )