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

landing_home_page = "../views/landing.html"

def index(request):
    """ Renders Dashboard/Home page. """
    signupForm = RegistrationForm()
    loginForm = LoginForm()
    fb_url = settings.FACEBOOK_AUTH_URL.format(request.build_absolute_uri(settings.FACEBOOK_REDIRECT_URI))

    return render_to_response(
        landing_home_page, {}, RequestContext(request, {
            'fb_url':fb_url,
            'formLogin':loginForm,
            'formSignup':signupForm,
        }),
    )

