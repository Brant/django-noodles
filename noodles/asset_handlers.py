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
            except IOError:     # image doesn't exist on disk
                filename = None

            if filename:
                obj_attr = getattr(model_obj, image_field)

                file_fullpath = obj_attr.path

                tmp = file_fullpath
                if tmp.endswith(filename):
                    tmp = tmp[0:len(tmp) - len(filename)]

                file_dir = tmp

                media_root = settings.MEDIA_ROOT
                if media_root.endswith(os.sep):
                    media_root = media_root[:-1]

                if tmp.startswith(media_root):
                    tmp = tmp[len(media_root)+1:-1]

                filepath = tmp

                self._asset_handlers.update({
                    image_field: {
                        "handler": AssetsFromImageHandler(file_fullpath, quality),
                        "path": filepath,
                        "filename": filename,
                        "original_directory": file_dir,
                    }
                })

        self.image_fields = image_fields
        self._model_obj = model_obj
