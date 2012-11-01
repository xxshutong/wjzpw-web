# coding: utf-8
from django.template.context import Context, get_standard_processors
from wjzpw.web.models import Configuration, FootItem

class RequestContext(Context):
    """
    This subclass of template.Context automatically populates itself using
    the processors defined in TEMPLATE_CONTEXT_PROCESSORS.
    Additional processors can be specified as a list of callables
    using the "processors" keyword argument.
    """
    def __init__(self, request, dict=None, processors=None, current_app=None, use_l10n=None):
        if not dict:
            dict = {}

        # 基础配置信息
        configuration = Configuration.objects.filter()

        if configuration:
            dict['configuration'] = configuration[0]

        # ‘公共’尾部信息
        foot_items = FootItem.objects.filter(is_display=True).order_by('order')
        if foot_items:
            dict['foot_items'] = foot_items
            
        Context.__init__(self, dict, current_app=current_app, use_l10n=use_l10n)
        if processors is None:
            processors = ()
        else:
            processors = tuple(processors)
        for processor in get_standard_processors() + processors:
            self.update(processor(request))