from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from wjzpw.webverse.forms import PersonalRegForm
from wjzpw.webverse.models import Province

register_page = "../views/personal/register.html"

"""
Personal registration
"""
def register(request):
    form = PersonalRegForm()

    if request.method == 'POST':
        # post register user
        form = PersonalRegForm(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)

    # go to register page
    provinces = Province.objects.all()
    return render_to_response(
        register_page, {}, RequestContext(request, {
            'form':form,
            'provinces':provinces
        }),
    )

