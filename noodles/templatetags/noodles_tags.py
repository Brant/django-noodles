"""
Template tags and filters for noodles
"""
import re

from django import template
from django.utils.safestring import mark_safe

from noodles.forms import ContactForm
from noodles.util import add_links_to_string, add_mailto_to_string

register = template.Library()


@register.filter
def auto_links(value, autoescape=None):
    """
    Automatically generate links from text
    """

    # no idea what these 3 lines do...
    esc = None
    if autoescape:
        esc = conditional_escape

    value = mark_safe(add_links_to_string(value, esc))
    value = mark_safe(add_mailto_to_string(value, esc))

    return value

auto_links.needs_autoescape = True


@register.inclusion_tag('noodles/contact_form.html')
def contact_form():
    """
    Render the contact form
    """
    return { "form": ContactForm }
    

@register.filter
def insidenav(request, pattern):
    """
    Check if a given HttpRequest object is inside a url pattern
    
    TODO: Unit Test(s)
    """
    
    path = request
    
    if not path.__class__.__name__ == "unicode" and not isinstance(request, str):
        path = request.path
    
    if pattern == '/':
        if pattern == path:
            return True
    else:
        if re.search(pattern, path):
            return True
    
    return False