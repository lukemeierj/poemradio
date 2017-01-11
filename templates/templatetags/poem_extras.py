from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name="simpleMarkDown")
@stringfilter
def simpleMarkDown(value):
    return value.lower()