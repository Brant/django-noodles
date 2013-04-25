"""
Some abstract models
"""
from datetime import timedelta, datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings

from noodles.util import get_email_send_to_list


def find_slug_matches(obj, slug):
    """
    Return a queryset of matches of the type of 'obj' with a slug of 'slug'
    """
    if obj.id:
        return obj.__class__.objects.filter(~Q(pk=obj.id), slug=slug)

    return obj.__class__.objects.filter(slug=slug)


def generate_slug(obj, slug_target, persistant_slug=False):
    """
    Create a slug for obj based on slug_target

    Does not allow duplicates - appends a number
    """
    slug = obj.slug

    to_slug = getattr(obj, slug_target)

    if not slug or not persistant_slug:
        slug = slugify(to_slug)

        orig_slug = slug

        num = 1
        while (find_slug_matches(obj, slug)):
            slug = "%s-%s" % (orig_slug, num)
            num += 1

    return slug


class LittleSlugger(models.Model):
    """
    Model for slugifying some attribute
    """

    slug = models.CharField(max_length=300, editable=False, blank=True)
    
    def __unicode__(self):
        return getattr(self, self.get_slug_target())
    
    class Meta:
        """
        Remember to inherit if needed
        """
        abstract = True

    def get_slug_target(self):
        """
        return the slug target and persistant as a tuple

        e.g. if the subclass has a 'name' property, this should return 'name'

        persistant refers to whether the slug should persist if the field value changes

        so, if persist is True and a subclass' slug target value changes, the slug will not update
            - Useful for public permalinks
        """
        raise NotImplementedError("classes inheriting from LittleSlugger must implement a 'get_slug_target' method")

    def save(self, *args, **kwargs):
        """
        Custom save

        - Slugifies title
        """

        try:
            slug_target, persist = self.get_slug_target()
        except ValueError:
            slug_target = self.get_slug_target()
            persist = True

        self.slug = generate_slug(self, slug_target, persist)
        super(LittleSlugger, self).save(*args, **kwargs)


class NameSlug(LittleSlugger):
    """
    gives a 'name' attribute and slug for that name
    """
    name = models.CharField(max_length=300)
    
    def get_slug_target(self):
        """ 
        Implementing required method
        """
        return 'name'
    
    class Meta:
        """
        Django metadata
        """
        abstract = True
        

class NameSlugActive(NameSlug):
    """
    Inherits a name and a slug
    
    also gives an 'active' field
    """
    
    active = models.BooleanField(default=True)
    
    class Meta:
        """
        Django metadata
        """
        abstract = True
        

class ContactSubmission(models.Model):
    """
    Name/email/message contact form submission
    """
    name = models.CharField(max_length=300)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

@receiver(post_save, sender=ContactSubmission, dispatch_uid="Noodel_Contact_Submission")
def send_notification_email(sender, **kwargs):
    """
    Pop off an email notification when a contact submission goes through
    """
    if kwargs["created"]:
        
        submission = kwargs["instance"]
        
        EmailMessage(
            "%s Contact from %s" % (settings.EMAIL_SUBJECT_PREFIX, submission.name), 
            "Name: %s\nEmail: %s\n\nMessage:\n%s" % (submission.name, submission.email, submission.message),  
            settings.DEFAULT_FROM_EMAIL,
            get_email_send_to_list(),
            headers = {"Reply-To": submission.email}
        ).send(fail_silently=True)
    

class TitleDateSlug(models.Model):
    """
    Abstract model that provides a few things
    
    Title turns to slug
    Date can be used for whatever
    """
    title = models.CharField(max_length=900)
    slug = models.CharField(max_length=900, blank=True)
    date = models.DateTimeField(blank=True)
    
    def save(self, *args, **kwargs):
        """
        Custom save
        
        - Slugifies title
        """
        
        self.slug = self._generate_slug()
        
        if not self.date:
            self.date = datetime.now() + timedelta(days=5)
            
        super(TitleDateSlug, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        """
        Django metadata
        
        Don't forget to inherit this if you need more Meta
        https://docs.djangoproject.com/en/1.3/topics/db/models/#meta-inheritance
        
        class TitleDateSlugConcrete(TitleDateSlug):
            class Meta(TitleDateSlug.Meta):
                ordering = ["-title"]
        """
        abstract = True
        
    def _find_slug_matches(self, slug):
        """
        Figure out if the slug is taken
        """
        if self.id:
            return self.__class__.objects.filter(~Q(pk=self.id), slug=slug)
        
        return self.__class__.objects.filter(slug=slug)
    
    def _generate_slug(self):
        """
        Create a slug based on the title
        Does not allow duplicates - appends a number
        """
        slug = self.slug
        
        if not slug:
            slug = slugify(self.title)    

            orig_slug = slug
            
            num = 1
            while (self._find_slug_matches(slug)):
                slug = "%s-%s" % (orig_slug, num)
                num += 1
         
        return slug


class ActiveToggler(models.Model):
    """
    An 'active/deactive' toggle model
    
    Only one on the type can be active at a time
    """
    active = models.BooleanField(default=False)
    
    class Meta:
        """
        Django Meta
        """
        abstract = True
    
    def save(self, *args, **kwargs):
        """
        Custom save to "toggle" all other actives to inactive
        """
        if self.active:
            for obj in self.__class__.objects.filter(active=True):
                obj.active = False
                obj.save()
                
        super(ActiveToggler, self).save(*args, **kwargs)


class SiteMeta(models.Model):
    """
    A key/value store for simple site metadata
    """
    key = models.CharField(max_length=500)
    value = models.CharField(max_length=800)
        
    class Meta:
        """
        Django Metadata
        """
        verbose_name_plural = 'Site metadata'