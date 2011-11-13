"""
Utilites
"""

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def make_paginator(request, qs, per_page=5):
    """
    Return a paginated object list
    
    Centralizes how many items per page
    """
    
    paginator = Paginator(qs, per_page)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        ret = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ret = paginator.page(paginator.num_pages)
    
    return ret