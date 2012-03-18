from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template.context import RequestContext
from wjzpw.webverse.controllers.utils import Utils
from wjzpw.webverse.models import City
from django.utils import simplejson

dashboard_page = "../views/dashboard.html"

def dashboard(request):
    """ Renders Dashboard/Home page. """
    return render_to_response(
        dashboard_page, {}, RequestContext(request, {
#            'formLogin':loginForm,
#            'formSignup':signupForm,
        }),
    )

"""
Get city list by province ID
"""
def ajax_get_city_by_province(request, province_id):
    data = ''
    if request.method == 'GET':
        city_list = City.objects.filter(province = int(province_id))
        data = simplejson.dumps(Utils.generate_options(city_list))
        print data
    return HttpResponse(data, 'application/json')
