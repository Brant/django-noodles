"""
NOODLE VIEWS!!!
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from noodles.forms import ContactForm


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