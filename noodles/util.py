"""
Utilites
"""
import Image, os

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

"""
Utilites
"""
import Image, os

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


class AssetsFromImageHandler(object):
    """
    Utility class for to handle creating various assets
        at various dimensions from a given image
    """
    
    def __init__(self, original_file_path, quality=100):
        """
        Instantiate with original ratio and file path
        """
        self._image = Image.open(original_file_path)
        original_w = self._image.size[0]
        original_h = self._image.size[1]
        self._ratio = float(original_h) / float(original_w)
        self._quality = quality
    
    def buffer_image(self, width, height, save_path=None):
        """ 
        Adds buffer space space to size the image properly 
        """
        target_ratio = float(height) / float(width)
        
        if target_ratio == self._ratio:
            buffered_image = self.create_any_size(width, height)
        elif target_ratio > self._ratio:
            # uploaded image is too wide
            height = int(self._image.size[0] * target_ratio)
            width = self._image.size[0]
            buffered_image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            offset = (0, ((height - self._image.size[1]) / 2))
            buffered_image.paste(self._image, offset)
        else:
            # uploaded image is too tall
            height = self._image.size[1]
            width = int(self._image.size[1] / target_ratio)
            buffered_image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            offset = ((width - self._image.size[0]) / 2, 0)
            buffered_image.paste(self._image, offset)
        
        if save_path:
            self._save_image(buffered_image, save_path)
            
        return buffered_image
            
    
    def create_any_size(self, width, height, save_path=None):
        """
        Take self._image and return it at any size
            It will stretch if ratio is not maintained
        """
        sized_image = self._image.resize((width, height), Image.ANTIALIAS) 
        if save_path:
            self._save_image(sized_image, save_path)
        return sized_image
    
    def create_width(self, width, save_path=None):
        """
        Return self._image sized based on width, 
            maintaining aspect ratio
        """
        return self.create_any_size(width, int(float(width) * float(self._ratio)), save_path)
    
    def create_height(self, height, save_path=None):
        """
        Return self._image sized based on height, 
            maintaining aspect ratio
        """
        return self.create_any_size(int(float(height) / float(self._ratio)), height, save_path)
    
    def _save_image(self, image, save_path):
        """
        save 'image' at the save path
        """
        image_path = os.path.dirname(save_path)
        if not os.path.isdir(image_path):
            os.makedirs(image_path)
        image.save(save_path, quality=self._quality)
        