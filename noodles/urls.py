"""
Noodles URLs
"""
from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = patterns('noodles.views',    
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^contact/thanks/$', 'contact_thanks', name='contact_thanks'),
)

favicon_patterns = patterns('',
    (r'^favicon\.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico'),
    (r'^favicon\.png', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.png'),
    (r'^apple-touch-icon\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon.png'),
)