"""
Asset handlers
"""
import os

from django.conf import settings
from django.db.models import ImageField

from noodles.util import AssetsFromImageHandler


class ModelAssetsFromImageHandler:
    def __init__(self, model_obj):
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
                fileroot = settings.MEDIA_ROOT
                filepath = getattr(model_obj, image_field).field.upload_to
                file_fullpath = os.path.join(fileroot, filepath, filename)
                self._asset_handlers.update({image_field: {"handler": AssetsFromImageHandler(file_fullpath), "path": filepath, "filename": filename}})
            
        self.image_fields = image_fields
        self._model_obj = model_obj

        