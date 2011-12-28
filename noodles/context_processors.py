"""
Available context processors for django-noodles
"""
from django.conf import settings

from noodles.models import SiteMeta

def static_paths(request):
    """
    """
    return {
        "IMG": "%s%s/" % (settings.STATIC_URL, "img"),
        "JS": "%s%s/" % (settings.STATIC_URL, "js"),
        "CSS": "%s%s/" % (settings.STATIC_URL, "css")
    }

def site_meta(request):
    """
    Make metadata available as a context processor
    
    available like this:
        {{ SITE_META.key }}
    """
    meta = SiteMeta.objects.all()
    
    SITE_META = {}
    
    for data in meta:
        SITE_META.update({data.key: data.value})
        
    return {'SITE_META': SITE_META}