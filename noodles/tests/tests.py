"""
Noodles Tests
"""
import os

from datetime import datetime

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.test.client import Client

from noodles.templatetags.noodles_tags import insidenav
from noodles.models import SiteMeta, ContactSubmission
from noodles import context_processors
from noodles.tests.models import NameSlugConcrete, ActiveTogglerConcrete, TitleDateSlugConcrete, LittleSluggerConcrete, BadLittleSluggerConcrete, LittleSluggerConcreteNoPersist
from noodles import util
from noodles.util import AssetsFromImageHandler
from noodles.tests.util import FakeRequest



class AssetFromImageTestCase(TestCase):
    """
    Tests relating to converting an image into assets
    """
    def setUp(self):
        """
        """
        
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(self.path, "_tmp.jpg")
        self.image_path = os.path.join(self.path, "happy.jpg")
        self.handler = AssetsFromImageHandler(self.image_path)
#         self.assertEquals(self.handler._ratio, float(float(2)/float(3)))
    
    def test_not_saving(self):
        """
        Test some features of the asset handler without saving
        """
#         buffered_image = self.handler.buffer_image(200, 100, self.save_path)
#         self.assertEquals(buffered_image.size[1], 700)
#         print buffered_image.size
        sized_image = self.handler.create_any_size(100, 200)
        self.assertEquals(sized_image.size[0], 100)
        self.assertEquals(sized_image.size[0], 200)

class ContactTestCase(TestCase):
    """
    Tests relating to Contact Form
    """
    urls = "noodles.tests.urls"
    
    def setUp(self):
        """
        Set some things up
        """
        self.client = Client()
    
    def test_render_form(self):
        """
        Test rendering of contact form from template inclusion tag
        """
        self.client.get("/")
        self.client.get("/contact/")
    
    def test_post_data(self):
        """
        Test post data handling for form
        """
        self.assertEquals(ContactSubmission.objects.all().count(), 0)
        resp = self.client.post("/contact/", {"name": "Timmy Tommy", "email": "my@email.com", "message": "Hi there!"}, follow=True)
        self.assertEquals(ContactSubmission.objects.all().count(), 1)
        self.assertTemplateUsed(resp, "noodles/tests/contact_thanks.html")
        submission = ContactSubmission.objects.all()[0]
        self.assertEquals(submission.email, "my@email.com")
        self.assertEquals(submission.name, "Timmy Tommy")
        self.assertEquals(submission.message, "Hi there!")


class EmailTestCase(TestCase):
    """
    Tests relating to email list mechanisms
    """
    def test_email_send_to_list_default(self):
        """
        Test empty ADMINS list and empty NOODLES_EMAIL_LIST
        """
        self.assertEquals([], util.get_email_send_to_list())

    @override_settings(ADMINS=[("Some Guy", "someone@nowhere.com"),])
    def test_email_send_to_list_fallback(self):
        """
        Test email list fallback mechanism
        """
        self.assertEquals(["someone@nowhere.com"], util.get_email_send_to_list())
    
    @override_settings(ADMINS=[("Some Guy", "someone@nowhere.com"),])
    @override_settings(NOODLES_EMAIL_LIST=["nobody@somewhere.com"])
    def test_email_send_to_list(self):
        """
        Test email list fallback mechanism
        """
        self.assertEquals(["nobody@somewhere.com"], util.get_email_send_to_list())
    
    
    def test_post_save_hook(self):
        """
        Test the post_save hook on saving contact submissions
        
        Just a coverage test, there doesnt seem to be any way to actually see
        the mail.outbox result from this
        """
        submission = ContactSubmission(name="Noone", email="noone@somewhere.com", message="Hi There")
        submission.save()


class ContextProcessorTestCase(TestCase):
    """
    Tests for context processors
    """
    def test_static_paths(self):
        """
        Test static paths context processor
        """
        paths = context_processors.static_paths("fake_request")
        self.assertIn(settings.STATIC_URL, paths["IMG"])
        self.assertIn(settings.STATIC_URL, paths["JS"])
        self.assertIn(settings.STATIC_URL, paths["CSS"])
    
    def test_site_meta(self):
        """
        Test SITE_META context processor
        """
        metadata = context_processors.site_meta("fake_request")
        self.assertDictEqual(metadata["SITE_META"], {})
        
        SiteMeta(key="KEY", value="VAL").save()
        metadata = context_processors.site_meta("fake_request")
        self.assertIn("KEY", metadata["SITE_META"])
        self.assertEquals(metadata["SITE_META"]["KEY"], "VAL")
        
    def test_site(self):
        """
        Test SITE_NAME and SITE_URL
        """
        self.assertEquals(context_processors.site("fake_request")["SITE_NAME"], "example.com")
        self.assertEquals(context_processors.site("fake_request")["SITE_URL"], "http://example.com")


class InsideNavTestCase(TestCase):
    """
    Tests for insidenav template filter
    """
    urls = "noodles.tests.urls"
    
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
        self.assertTrue(insidenav("/contact/thanks/", "/contact/"))
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
        

class LittleSluggerTestCase(TestCase):
    """
    Tests for the LittleSlugger abstract test case
    """
    def test_bad_slug_target(self):
        """
        Test poor (or lacking) get_slug_target implementations
        """
        bad = BadLittleSluggerConcrete()
        with self.assertRaises(NotImplementedError):
            bad.save()
    
    def test_slug_target(self):
        """
        Test well implementeed get_slug_target
        """
        fine = LittleSluggerConcrete(slug_target="Hello")
        fine.save()
        self.assertEquals("Hello", fine.slug_target)
        self.assertEquals("slug_target", fine.get_slug_target())
        self.assertEquals("Hello", fine.__unicode__())
        self.assertEquals("hello", fine.slug)
    
    def test_persisting_resave(self):
        """
        Test resaving objects with persisting slug
        """
        fine = LittleSluggerConcrete(slug_target="Hello")
        fine.save()
        self.assertEquals("hello", fine.slug)
        fine.slug_target = "Hello World"
        fine.save()
        self.assertEquals("hello", fine.slug)
        
    def test_not_persisting_resave(self):
        """
        Test resaving objects without a persisting slug
        """
        fine = LittleSluggerConcreteNoPersist(slug_target="Hello")
        fine.save()
        self.assertEquals("hello", fine.slug)
        fine.slug_target = "Hello World"
        fine.save()
        self.assertEquals("hello-world", fine.slug)


class NameSlugTestCase(TestCase):
    """
    Tests relating to NameSlug abstract model
    """
    def test_name_slug_properties(self):
        """
        Test the properties setup for NameSlug
        """
        name_slug = NameSlugConcrete(name="Something")
        name_slug.save()
        self.assertEquals(name_slug.get_slug_target(), "name")
        self.assertEquals(name_slug.__unicode__(), "Something")
        self.assertEquals(name_slug.slug, "something")
    
    def test_name_slug_persist(self):
        """
        NameSlug models should have a persistant slug
        """
        name_slug = NameSlugConcrete(name="Something")
        name_slug.save()
        self.assertEquals(name_slug.slug, "something")
        name_slug.name = "Something Else"
        name_slug.save()
        self.assertEquals(name_slug.slug, "something")


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
        