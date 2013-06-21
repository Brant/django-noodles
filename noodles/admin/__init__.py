"""
Admin configurations
"""
from django.contrib import admin

from noodles.models import SiteMeta, ContactSubmission


class SiteMetaAdmin(admin.ModelAdmin):
    """
    Blog Entry admin configuration
    """
    list_display = ["key", "value"]
    
    
class ContactSubmissionAdmin(admin.ModelAdmin):
    """
    Contact Submissions admin config
    """
    list_display = ["name", "email", "date"]

    
admin.site.register(SiteMeta, SiteMetaAdmin)
admin.site.register(ContactSubmission, ContactSubmissionAdmin)