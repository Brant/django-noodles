"""
Forms for Noodles
"""

from django import forms
from noodles.models import ContactSubmission

class ContactForm(forms.ModelForm):
    """
    Contact form, based on ContactSubmission model
    """
    class Meta:
        """
        Django Metadata
        """
        model = ContactSubmission
        exclude = ["date"]