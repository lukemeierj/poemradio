from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import escape


register = template.Library()



@register.filter(name="markdown", needs_autoescape=True)
@stringfilter
def simpleMarkDown(value, autoescape=True):
    text = escape(value)
    formatting = ['italic', 'bold', 'bold italic']
    inFormatted = [False, False, False]
    special = "*"
    format = ''
    output = ''
    inFormatting = False
    for char in text:
        if char not in special and not inFormatting:
            output += char;
        elif char not in special and inFormatting:
            numSpecial = len(format)
            inFormatting = False
            format = ''
            if inFormatted[numSpecial-1]:
                output += "</span>" 
            else:
                output += "<span class = '%s'>" % formatting[numSpecial-1]
                inFormatted[numSpecial-1] = True
            output+= char

        elif char in special:
            format += char
            inFormatting = True
    for _ in inFormatted:
        if _:
            output += "</span>"
    return mark_safe(output)