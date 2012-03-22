from StringIO import StringIO
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template.context import RequestContext
from random import choice
import Image
import ImageDraw
from wjzpw import settings
from wjzpw.webverse.controllers.utils import Utils
from wjzpw.webverse.forms import LoginForm
from wjzpw.webverse.models import City, Captcha
from django.utils import simplejson

dashboard_page = "../views/dashboard.html"

def dashboard(request):
    """ Renders Dashboard/Home page. """
    login_form = LoginForm()
    return render_to_response(
        dashboard_page, {}, RequestContext(request, {
            'login_form':login_form,
        }),
    )

def login(request):
    """ Renders Dashboard/Home page. """
    login_form = LoginForm(request.POST)
    return render_to_response(
        dashboard_page, {}, RequestContext(request, {
            'login_form':login_form,
            }),
    )

def ajax_get_city_by_province(request, province_id):
    """
    Get city list by province ID
    """
    data = ''
    if request.method == 'GET':
        city_list = City.objects.filter(province = int(province_id))
        data = simplejson.dumps(Utils.generate_options(city_list))
    return HttpResponse(data, 'application/json')

def verify_image(request):
    """
    Get verify code
    """
    captcha_text = Captcha(request).get()
    response = HttpResponse()
    if captcha_text:
        image = Image.new("RGBA", (settings.LENGTH * settings.FONT_SIZE - 26, settings.FONT_SIZE), (0,0,0,0))
        canvas = ImageDraw.Draw(image)

        for i in range(0, len(captcha_text)):
            # font = ImageFont.truetype(choice(captcha.FONTS), captcha.FONT_SIZE)
            # canvas.text((captcha.FONT_SIZE*i+2, -4), captcha_text[i], font = font, fill = choice(captcha.COLOURS))
            horizon = 1; verticality  = -1
            if i>0: horizon = (settings.FONT_SIZE - 5) * i
            if i%2 == 0: verticality = 2
            canvas.text((horizon, verticality), captcha_text[i], fill = choice(settings.COLOURS))

        out = StringIO()
        image.save(out, "PNG")
        out.seek(0)
        response['Content-Type'] = 'image/png'
        response.write(out.read())

    return response