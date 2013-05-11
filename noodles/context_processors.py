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


def site(request):
    """
    Return site.name and site.domain as a URL
    """
    THIS_SITE = Site.objects.get_current()
    return {
        "SITE_NAME": THIS_SITE.name,
        "SITE_URL": "http://%s" % THIS_SITE.domain
    }


SITE_META = {}
def site_meta(request):
    """
    Make metadata available as a context processor
    
    available like this:
        {{ SITE_META.key }}
    """
    META = SiteMeta.objects.all()
    for data in META:
        SITE_META.update({data.key: data.value})    
    return {'SITE_META': SITE_META}


def noodle_processors(request):
    """
    ALL THE NOODLES!
    """
    return site(request).update(site_meta(request)).update(static_paths(request))
