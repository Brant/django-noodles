"""
Noodles Tests
"""
from datetime import datetime
from django.test import TestCase

from noodles.templatetags.noodles_tags import insidenav
from noodles.testing.models import *

class FakeRequest(object):
    """
    just provide a few things for testing purposes
    to mimic a request object
    """
    def __init__(self, path):
        self.path = unicode(path) 

class InsideNavTestCase(TestCase):
    urls = "noodles.testing.urls"
    
    def setUp(self):
        """
        set a few things up
        """
        self.root_url = FakeRequest("/")
        self.contact_url = FakeRequest("/contact/thanks/")
    
    def test_root_path(self):
        """
        The root url really should only match itself
        """
        self.assertTrue(insidenav(self.root_url, "/"))
        self.assertFalse(insidenav(self.root_url, "/contact"))
        
    def test_unicode_only(self):
        """
        Django passes around unicodes instead of strings
        """
        with self.assertRaises(AttributeError):
            insidenav("/contact/thanks/", "/contact/")
        
        self.assertTrue(u"/contact/thanks/", "/contact/")
        
    def test_inside_nav(self):
        """
        Test functionality
        """
        self.assertTrue(insidenav(self.contact_url, "/contact"))
        self.assertTrue(insidenav(self.contact_url, "/contact/"))
        self.assertTrue(insidenav(self.contact_url, "contact"))
        self.assertFalse(insidenav(self.contact_url, "asdf"))
        self.assertFalse(insidenav(self.contact_url, "/asdf/"))
        

class ActiveTogglerTestCase(TestCase):
    """
    Tests for the ActiveToggler abstract model
    """
    def setUp(self):
        """
        Set some things up
        """
        self.obj_1 = ActiveTogglerConcrete()
        self.obj_2 = ActiveTogglerConcrete()
        
        self.obj_1.save()
        self.obj_2.save()
        
    def test_toggling(self):
        """
        Make sure our toggling works
        
        ... thats about all the model does...
        """
        self.obj_1.active = True
        self.obj_1.save()
        self.assertTrue(self.obj_1.active)
        self.assertFalse(self.obj_2.active)
        
        self.obj_2.active = True
        self.obj_2.save()
        
        self.assertEquals(ActiveTogglerConcrete.objects.filter(active=True).count(), 1)
        

class TitleDateSlugTestCase(TestCase):
    """
    Tests for the TitleDateSlug abstract model
    """
    def setUp(self):
        """
        Set some stuff up for the tests
        """
        self.mod = TitleDateSlugConcrete(title="Some People")
        self.mod_2 = TitleDateSlugConcrete(title="Some People")
        self.mod_3 = TitleDateSlugConcrete(title="Some People")

    def test_slugify_during_save(self):
        """
        Slug should be auto generated
        """
        self.mod.save()
        self.assertEquals(self.mod.slug, "some-people")
    
    def test_slugify_not_used(self):
        """
        If slug is present, it shoud not be overwritten
        """
        self.mod.slug = "hello"
        self.mod.save()
        self.assertEquals(self.mod.slug, "hello")
    
    def test_duplicate_slugs(self):
        """
        The save shouldnt allow duplicate slugs
        """
           
        self.mod_2.save()
        self.assertEquals(self.mod_2.slug, "some-people")
        
        self.mod.save()
        self.assertEquals(self.mod.slug, "some-people-1")
        
        self.mod_3.save()
        self.assertEquals(self.mod_3.slug, "some-people-2")
        
    
    def test_date_during_save(self):
        """
        Date should be auto generated
        """
        self.mod = TitleDateSlugConcrete(title="Some People")
        self.mod.save()
        self.assertNotEquals(self.mod.date, None)
    
    def test_date_not_generated(self):
        """
        Date should not be generated if it is supplied
        """
        some_date = datetime.now()
        self.mod.date = some_date
        self.mod.save()
        self.assertEquals(self.mod.date, some_date)
        
        self.mod.date = None
        self.mod.save()
        self.assertNotEquals(self.mod.date, some_date)
        self.assertNotEquals(self.mod.date, None)
        