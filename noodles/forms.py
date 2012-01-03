"""
Forms for Noodles
"""

from django import forms
from django.forms.widgets import Input
from noodles.models import ContactSubmission


class EmailInput(Input):
    input_type = 'email'

class ContactForm(forms.ModelForm):
    """
    Contact form, based on ContactSubmission model
    """
    
    email = forms.CharField(widget=EmailInput)
    
    class Meta:
        """
        Django Metadata
        """
        model = ContactSubmission
        exclude = ["date"]
        