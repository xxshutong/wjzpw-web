# coding: utf-8
import datetime
from django.db.models import Q
from django.shortcuts import render_to_response
from wjzpw.web import models
from wjzpw.web.component import RequestContext
from django.http import Http404
from wjzpw.web.models import FootItem


FOOT_ITEM_PAGE = "../views/foot_item.html"
ANNOUNCEMENT_PAGE = "../views/announcement.html"

def get_foot_item(request, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        raise Http404()
    item = FootItem.objects.get(id=item_id)
    return render_to_response(
        FOOT_ITEM_PAGE, {}, RequestContext(request, {
            'item': item,
        }),
    )


def get_announce_list(request, announcement_id=None):
    announce_list = models.Announcement.objects.filter(Q(end_date__gte=datetime.datetime.today()) | Q(end_date=None)).order_by('-updated_at')
    selected_id = long(announcement_id) if announcement_id else 0;

    return render_to_response(
        ANNOUNCEMENT_PAGE, {}, RequestContext(request, {
            'announce_list': announce_list,
            'selected_id': selected_id
        })
    )

