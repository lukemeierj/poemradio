from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import escape
from mistune import markdown

register = template.Library()

@register.filter(name="markdown", needs_autoescape=True)
@stringfilter
def simpleMarkDown(value, autoescape=True):
    output = markdown(value, escape = autoescape, hard_wrap = True)
    return mark_safe(output)