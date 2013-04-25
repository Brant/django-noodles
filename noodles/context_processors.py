"""
Available context processors for django-noodles
"""
from django.conf import settings
from django.contrib.sites.models import Site

from noodles.models import SiteMeta


def static_paths(request):
    """
    Return URLS to our static areas
    """
    return {
        "IMG": "%s%s/" % (settings.STATIC_URL, "img"),
        "JS": "%s%s/" % (settings.STATIC_URL, "js"),
        "CSS": "%s%s/" % (settings.STATIC_URL, "css")
    }


THIS_SITE = Site.objects.get_current()
def site(request):
    """
    Return site.name and site.domain as a URL
    """
    return {
        "SITE_NAME": THIS_SITE.name,
        "SITE_URL": "http://%s" % THIS_SITE.domain
    }
    

META = SiteMeta.objects.all()
SITE_META = {}
for data in META:
    SITE_META.update({data.key: data.value})
    

def site_meta(request):
    """
    Make metadata available as a context processor
    
    available like this:
        {{ SITE_META.key }}
    """    
    return {'SITE_META': SITE_META}