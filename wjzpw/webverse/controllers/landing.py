from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

dashboard_page = "../views/dashboard.html"

def dashboard(request):
    """ Renders Dashboard/Home page. """
    return render_to_response(
        dashboard_page, {}, RequestContext(request, {
#            'formLogin':loginForm,
#            'formSignup':signupForm,
        }),
    )

