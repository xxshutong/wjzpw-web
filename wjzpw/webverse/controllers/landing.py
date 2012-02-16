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

kid_home_page = "../views/kid/kid.html"
parent_home_page = "../views/parent/parent.html"
landing_home_page = "../views/landing.html"
index_page = "../views/index.html"
forget_passwrod_page = "../views/forgot_password.html"

def signup(request):
    signupForm = RegistrationForm()
    loginForm = LoginForm()
    fb_url = settings.FACEBOOK_AUTH_URL.format(request.build_absolute_uri(settings.FACEBOOK_REDIRECT_URI))

    if request.method == 'POST':
        signupForm = RegistrationForm(request.POST)
        if signupForm.is_valid():
            user_profile, username = signupForm.save(signupForm.cleaned_data)
            #login user and redirect user to add kid page
            user = authenticate(username = username,
                                    password = signupForm.cleaned_data['password1'])
            djlogin(request, user)
            return HttpResponseRedirect("/parent/settings/")

    return render_to_response(landing_home_page, RequestContext(request,
                            {
                                'fb_url':fb_url,
                                'formLogin':loginForm,
                                'formSignup':signupForm,
                            })
    )


def login(request):
    loginForm = LoginForm()
    signupForm = RegistrationForm()
    fb_url = settings.FACEBOOK_AUTH_URL.format(request.build_absolute_uri(settings.FACEBOOK_REDIRECT_URI))
    errors = ""
    login_error_message = u"Please enter a correct username and password. Note that both fields are case-sensitive."


    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['email_or_username']
            password = loginForm.cleaned_data['password']
            auth_user = UserManager.get_auth_user(username, password)

            if auth_user:
                # Authenticate user.
                user = authenticate(username = auth_user.username, password = password)
                if user is not None and not user.get_profile().is_deleted:
                    if user.is_active and user.is_staff:
                        user_profile = UserManager.get_user_profile(user.id)
                        if user_profile:
                            djlogin(request, user)
                            if user_profile.type == 0:
                                #redirect user to parent inbox
                                return redirect('/parent/inbox/')
                            else:
                                #redirect user to kid page
                                return redirect('/kid/activity/')
                        else:
                            errors = u"User have no user profile, please contact system admin."

                else:
                    errors = login_error_message
            else:
                errors = login_error_message
    
    return render_to_response(landing_home_page, RequestContext(request,
                            {
                                'formLogin':loginForm,
                                'formSignup':signupForm,
                                'fb_url':fb_url,
                                'errors':errors
                            })
    )

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

def home(request):
    return render_to_response(
        index_page, {},
        RequestContext(request, {}),
    )

def logout(request):
    """Logs user out."""
    signupForm = RegistrationForm()
    loginForm = LoginForm()
    fb_url = settings.FACEBOOK_AUTH_URL.format(request.build_absolute_uri(settings.FACEBOOK_REDIRECT_URI))

    djlogout(request)
    return render_to_response(landing_home_page, {}, RequestContext(request, {
            'fb_url':fb_url,
            'formLogin':loginForm,
            'formSignup':signupForm,
        }),
    )

def forgot_password(request):
    forgotpasswordForm = ForgotPasswordForm()
    send_mail_success = False
    if request.method == 'POST':
        forgotpasswordForm = ForgotPasswordForm(request.POST)
        if forgotpasswordForm.is_valid():
            username = forgotpasswordForm.cleaned_data['username']
            users = User.objects.filter(username = username)
            if users:
                user = users[0]
                newpasswd = utils.generate_password()
                user.set_password(newpasswd)
                user.save()
                send_mail_success = send_email((utils.forgot_password_mail_template % (user, newpasswd)), user.email, u'Your Metaverse Password')
                if send_mail_success:
                     return render_to_response(forget_passwrod_page, {}, RequestContext(request, {
                        'forgotpasswordForm':forgotpasswordForm,
                        'send_mail_success': send_mail_success,
                        }),
                     )
    return render_to_response(forget_passwrod_page, {}, RequestContext(request, {
        'forgotpasswordForm':forgotpasswordForm,
        }),
    )



