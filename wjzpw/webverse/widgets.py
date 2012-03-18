# coding: utf-8
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class CaptchaWidget(Widget):

    def render(self, name, value, attrs = None):
        """
        验证码HTML内容
        """

        attrs = self.build_attrs(attrs, name=name)
        output = [u'<input %s style="text-transform:uppercase;vertical-align:top;" size="10"/>' % flatatt(attrs)]
        output.append(u'<img height="23" src="/verify_image/" />')

        return mark_safe(u'&nbsp;'.join(output))