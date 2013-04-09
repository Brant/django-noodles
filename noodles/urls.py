"""
Noodles URLs
"""
from django.conf.urls import patterns, include, url


urlpatterns = patterns('noodles.views',    
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^contact/thanks/$', 'contact_thanks', name='contact_thanks'),
)

