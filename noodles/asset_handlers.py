"""
Asset handlers
"""
import os

from django.conf import settings
from django.db.models import ImageField

from noodles.util import AssetsFromImageHandler


class ModelAssetsFromImageHandler:
    def __init__(self, model_obj, quality=100):
        self._asset_handlers = {}
        image_fields = []

        for field in model_obj._meta.fields:
            if isinstance(field, ImageField):
                image_fields.append((field, field.name))

        for field, image_field in image_fields:

            try:
                filename = os.path.basename(getattr(model_obj, image_field).file.name)
            except ValueError:  # no image
                filename = None

            if filename:
                obj_attr = getattr(model_obj, image_field)

                file_fullpath = obj_attr.path

                tmp = file_fullpath
                if tmp.endswith(filename):
                    tmp = tmp[0:len(tmp) - len(filename)]

                if tmp.startswith(settings.MEDIA_ROOT):
                    tmp = tmp[len(settings.MEDIA_ROOT)+1:-1]

                filepath = tmp

                self._asset_handlers.update({image_field: {"handler": AssetsFromImageHandler(file_fullpath, quality), "path": filepath, "filename": filename}})

        self.image_fields = image_fields
        self._model_obj = model_obj


