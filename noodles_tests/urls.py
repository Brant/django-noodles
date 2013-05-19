"""
Test case URLS
"""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
# from noodles.urls import urlpatterns


urlpatterns = patterns('',    
    url(r'^$', 'noodles_tests.views.home', name='test_home'),
    url(r'^contact/$', 'noodles.views.contact', name='contact', kwargs={"template_name": "noodles_tests/contact.html"}),
    url(r'^contact/thanks/$', 'noodles.views.contact_thanks', name='contact_thanks', kwargs={"template_name": "noodles_tests/contact_thanks.html"}),
    url(r'^processors/$', TemplateView.as_view(template_name="noodles_tests/all_processors.html"), name='all_processors'),
)