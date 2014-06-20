"""
NOODLE VIEWS!!!
"""
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from noodles.forms import ContactForm


def json_response(request, response_data=None, content_type="application/json"):
    """
    shortcut function for returing a json response
    """
    if not response_data:
        response_data = {}

    return HttpResponse(json.dumps(response_data), content_type=content_type)


def contact(request, template_name="noodles/contact.html"):
    """
    Contact form

    Also a submission endpoint
    """
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("contact_thanks"))

    response_data = {"form": form}

    return render_to_response(template_name, response_data, context_instance=RequestContext(request))


def contact_thanks(request, template_name="noodles/contact_thanks.html"):
    """
    Thank you page, after a contact submission
    """
    return render_to_response(template_name, {}, context_instance=RequestContext(request))
