"""
Template tags and filters for noodles
"""
import re
from django import template
from noodles.forms import ContactForm

register = template.Library()

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
    
    if not path.__class__.__name__ == "unicode":
        path = request.path
    
    if pattern == '/':
        if pattern == path:
            return True
    else:
        try:
            if re.search(pattern, path):
                return True
        except AttributeError:
            pass
        return False
    
    return False