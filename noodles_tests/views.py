"""
Views for test cases
"""
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return render_to_response("noodles_tests/render_contact_form.html", {}, context_instance=RequestContext(request))