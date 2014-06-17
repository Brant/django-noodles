"""
Concrete models for test cases
"""
from django.db import models

from noodles.models import TitleDateSlug, ActiveToggler, LittleSlugger, NameSlug, HalfQuarterAssetsMixin, DefinedWidthsAssetsFromImagesMixin


class DefinedWidthAssetsConcrete(DefinedWidthsAssetsFromImagesMixin, models.Model):
    """
    Implenetation with an image field
    """
    some_image = models.ImageField(upload_to="images", null=True, blank=True)

    def get_dimensions(self):
        return [100, 200]


class HalfQuarterAssetsConcrete(HalfQuarterAssetsMixin, models.Model):
    """
    Implenetation with an image field
    """
    some_image = models.ImageField(upload_to="images", null=True, blank=True)


class NameSlugConcrete(NameSlug):
    """
    Simple Implementation
    """
    pass


class BadLittleSluggerConcrete(LittleSlugger):
    """
    No implemetation
    """
    pass


class LittleSluggerConcrete(LittleSlugger):
    slug_target = models.CharField(max_length=300)

    def get_slug_target(self):
        """
        Point at our 'slug_target'
        """
        return 'slug_target'


class LittleSluggerConcreteNoPersist(LittleSlugger):
    slug_target = models.CharField(max_length=300)

    def get_slug_target(self):
        """
        Point at our 'slug_target'
        """
        return ('slug_target', False)


class TitleDateSlugConcrete(TitleDateSlug):
    """
    Concreate class to test against
    """
    class Meta:
        """
        Django metadata
        """
        app_label = "noodles"


class ActiveTogglerConcrete(ActiveToggler):
    """
    Concrete class to test against
    """
    class Meta:
        """
        Django metadata
        """
        app_label = "noodles"
