from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from wjzpw.webverse import utils

register_page = "../views/personal/register.html"

def register(request):
    return render_to_response(
        register_page, {}, RequestContext(request, {
        }),
    )

