# coding: utf-8
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from wjzpw import settings
from wjzpw.web.forms.company import CompanyRegForm

from django.contrib.auth import login as djlogin

REGISTER_PAGE = "../views/company/register.html"

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