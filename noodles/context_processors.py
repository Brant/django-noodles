"""
Available context processors for django-noodles
"""
from noodles.models import SiteMeta

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