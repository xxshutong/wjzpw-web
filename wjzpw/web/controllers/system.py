# coding: utf-8
from django.shortcuts import render_to_response
from wjzpw.web.component import RequestContext

FOOT_ITEM_PAGE = "../views/foot_item.html"

def get_foot_item(request, item_id):
    pass
    return render_to_response(
        FOOT_ITEM_PAGE, {}, RequestContext(request, {
        }),
    )