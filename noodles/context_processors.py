"""
Available context processors for django-noodles
"""
from django.conf import settings
from django.contrib.sites.models import Site
from noodles.models import SiteMeta

def static_paths(request):
    """
    """
    return {
        "IMG": "%s%s/" % (settings.STATIC_URL, "img"),
        "JS": "%s%s/" % (settings.STATIC_URL, "js"),
        "CSS": "%s%s/" % (settings.STATIC_URL, "css")
    }
    
def site(request):
    """
    Return site.name and site.domain as a URL
    """
    site = Site.objects.get_current()
    return {
        "SITE_NAME": site.name,
        "SITE_URL": "http://%s/" % site.domain
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