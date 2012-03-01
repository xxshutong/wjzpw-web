from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from wjzpw import settings
from wjzpw.webverse import utils
from wjzpw.webverse.forms.forms import RegistrationForm, LoginForm, ForgotPasswordForm
from wjzpw.webverse.model.users import UserManager
from wjzpw.webverse.utils import send_email, generate_password

dashboard_page = "../views/dashboard.html"

def dashboard(request):
    """ Renders Dashboard/Home page. """
    signupForm = RegistrationForm()
    loginForm = LoginForm()

    return render_to_response(
        dashboard_page, {}, RequestContext(request, {
            'formLogin':loginForm,
            'formSignup':signupForm,
        }),
    )

