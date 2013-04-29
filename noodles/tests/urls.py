"""
Test case URLS
"""
from django.conf.urls import patterns, url

# from noodles.urls import urlpatterns


urlpatterns = patterns('',    
    url(r'^$', 'noodles.tests.views.home', name='test_home'),
    url(r'^contact/$', 'noodles.views.contact', name='contact'),
    url(r'^contact/thanks/$', 'noodles.views.contact_thanks', name='contact_thanks', kwargs={"template_name": "noodles/tests/contact_thanks.html"}),
    
)