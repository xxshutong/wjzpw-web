from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

register_page = "../views/personal/register.html"

"""
Personal registration
"""
def register(request):
#    form = PersonalRegForm()
    a = 'ddd'
    return render_to_response(
        register_page, {}, RequestContext(request, {
#            'form':form
        }),
    )

