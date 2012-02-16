import urllib
import urlparse
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from wjzpw import settings
from wjzpw.webverse.forms.forms import RegistrationForm, LoginForm
from urllib import urlopen
from simplejson import loads
from wjzpw.webverse.models import UserProfile

landing_home_page = "../views/landing.html"
parent_inbox_page = "../views/parent/inbox.html"

def authentication_callback(request):
    """
    Callback from Facebook with the authorization code. Code will be used to get the access token which is for
    accessing the FB API.
    """
    signupForm = RegistrationForm()
    loginForm = LoginForm()

    # Check if the request code is returned.
    authcode = request.GET.get('code')
    if authcode is not None:
        graph_url = 'https://graph.facebook.com/oauth/access_token'
        params = urllib.urlencode({'client_id':settings.FACEBOOK_APP_ID,
                                   'redirect_uri':request.build_absolute_uri(settings.FACEBOOK_REDIRECT_URI),
                                   'client_secret':settings.FACEBOOK_APP_SECRET,
                                   'code':authcode})

        resp = urlopen(graph_url, params).read()
        qs = urlparse.parse_qs(resp)

        if qs.has_key('access_token'):
            access_token = qs['access_token'][0]
            graph_me = 'https://graph.facebook.com/me?access_token='+access_token
            me_resp = loads(urlopen(graph_me).read())
            email = me_resp['email']
            fb_username = me_resp['username']

            user = authenticate(email=email, token=access_token)
            if user is None:
                # Create the user since it doesn't yet exist. Need to auth again to set backend.
                newuser = User.objects.create_user(fb_username, email, '')
                UserProfile(user=newuser, email=email, type=0).save()
                user = authenticate(email=email, token=access_token)

            # Now set the login to this user.
            uprofile = UserProfile.objects.get(email=email)
            if user.is_active:
                uprofile.access_token = access_token
                uprofile.save()
                auth_login(request, user)

            # Redirect to the parent inbox on success FB signup/login.
            return redirect("/parent/inbox")

    # Return error if the facebook connect returns error.
    return render_to_response(
        landing_home_page, {}, RequestContext(request, {
            'formLogin': loginForm,
            'formSignup': signupForm,
            'errors':"You'll need to authorize our app to login with Facebook."
        }),
        )
