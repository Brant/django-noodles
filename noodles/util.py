"""
Utilites
"""

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

def get_email_send_to_list():
    """
    Returns a list of addresses to send correspondance to
    """
    email_list = []
    
    try:
        email_list = settings.NOODLES_EMAIL_LIST
    except AttributeError:
        email_list = [email for name, email in settings.ADMINS]
    
    return email_list
    

def make_paginator(request, queryset, per_page=5):
    """
    Return a paginated object list
    
    Centralizes how many items per page
    """
    
    paginator = Paginator(queryset, per_page)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        ret = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ret = paginator.page(paginator.num_pages)
    
    return ret