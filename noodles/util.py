"""
Utilites
"""
import os
import re

from PIL import Image, ExifTags

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings


def add_mailto_to_string(value, esc=None):
	"""
	TODO: Unit Test
	"""
	if not esc:
		esc = lambda x: x

	pat = re.compile(r'([A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+)')
	value = pat.sub(r"<a href='mailto:\1'>\1</a>", esc(value))

	return value


def add_links_to_string(value, esc=None, extra_class=None):
	"""
	TODO: Unit Test
	"""
	if not esc:
		esc = lambda x: x

	# find all likely links
	pat = re.compile(r"((https?://)?([-\w]+\.[-\w\.]+)+\w(:\d+)?(/([-\w/_\.]*(\?\S+)?)?)*)", re.IGNORECASE | re.DOTALL)
	value = pat.sub(r"<a target='_blank' href='\1'>\1</a>", esc(value))

	# make sure partial email addresses arent converted to links
	value = re.sub(r"\@<a target='_blank' href=\'([\w\.]+)\'>([\w\.]+)</a>", r"@\1", value)
	value = re.sub(r"<a target='_blank' href=\'([\w\.]+)\'>([\w\.]+)</a>\@", r"\1@", value)

	# make sure phone numbers aren't turned into http hyperlinks
	value = re.sub(r"<a target='_blank' href=\'([\d\.]+)\'>([\d\.]+)</a>", r"\1", value)

	# add http anyhwere that it isn't
	value = re.sub(r"href=\'([^(http)])", r"href='http://\1", value)

	if extra_class:
		value = value.replace("<a target=", "<a class='%s' target=" % extra_class)

	return value



def has_changed(instance, field):
    """ check if a field has changed on a particular instance """
    if not instance.pk:
        return True
    old_value = instance.__class__._default_manager.filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value


class AssetFromImage:
    """
    Represents an asset produced from ImageFields by models.AssetsFromImagesMixin
    """
    def __init__(self, path):
        """
        save path to asset and produce
            url for asset based on static_url
        """
        self.path = path
        self.url = "%s%s" % (settings.MEDIA_URL, path)

    def __unicode__(self):
        return u"%s" % self.path

    def __str__(self):
        return "%s" % self.path


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
        self.original_w = self._image.size[0]
        self.original_h = self._image.size[1]
        self._ratio = float(self.original_h) / float(self.original_w)
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
        self.correct_orientation()
        sized_image = self._image.resize((width, height), Image.ANTIALIAS)
        if save_path:
            self._save_image(sized_image, save_path)
        return sized_image

    def correct_orientation(self):
        """
        Corrects images taken on the fly with a camera
        """
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        if hasattr(self._image, '_getexif'):  # only present in JPEGs
            e = self._image._getexif()        # returns None if no EXIF data
            if e is not None:
                exif = dict(e.items())

                try:
                    orientation = exif[orientation]

                    if orientation == 3:
                        self._image = self._image.transpose(Image.ROTATE_180)
                    elif orientation == 6:
                        self._image = self._image.transpose(Image.ROTATE_270)
                    elif orientation == 8:
                        self._image = self._image.transpose(Image.ROTATE_90)
                except KeyError:  # images with messed up metadata (TAGS)
                    pass

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
