# coding: utf-8
from django.shortcuts import render_to_response
from wjzpw.web.component import RequestContext
from django.http import Http404
from wjzpw.web.models import FootItem


FOOT_ITEM_PAGE = "../views/foot_item.html"

def get_foot_item(request, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        raise Http404()
    item = FootItem.objects.get(id=item_id)
    return render_to_response(
    FOOT_ITEM_PAGE, {}, RequestContext(request, {
            'item':item,
        }),
    )

