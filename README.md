Django Noodles
==============
Noodles is an app containing all sorts of misc. bits of code that I see to use across projects.

There aren't really any connecting dots or common design patterns. It's just stuff I use.

First, add noodles to your installed apps:
```python
INSTALLED_APPS = (
    ...
    'noodles',
)
```

The remaining documentation goes through individual noodles. Each is separate from the others - you can pick and choose which things to use.

Abstract Models
---------------
Each abstract model is essentially named exactly to match the fields it will give you. For example, "TitleDateSlug" will give you title, date, and slug fields. 

Your models can just inherit from these models to save yourself some typing.



### LittleSlugger
LittleSlugger allows you to designate a field on your model to be "slugified". It provides some additional calculations to prevent conflicting slugs, so you can query reliably on the slug field.

In order to implement, you need to create a method for your model named "get_slug_target". It should return the name of the field you want to slugify, as a string.
```python
class MySluggedModel(LittleSlugger):
    title = models.CharField(max_length=50)
    
    def get_slug_target(self):
        return "title"	    
```
### ActiveToggler
### TitleDateSlug
### NameSlug
### NameSlugActive

Website Metadata
----------------
Website metadata consists of key/value pairs that can be used in templates. After a syncdb with noodles installed, this will be available in the admin interface.

You'll need to add noodles.context_processors.site_meta to your context processors.
```python
TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    'noodles.context_processors.site_meta',
)
```
For example, perhaps you don't want to hardcode something like a user's Twitter URL into your templates. Instead, you could assign a key/value pair (through the admin interface) like this:

	key: MY_TWITTER
	value: http://twitter.com/someuser

Then, in your templates, you can refer to it like this:
```html
<a href="{{ SITE_META.MY_TWITTER }}">Follow me!</a>
```

Contact Submission
------------------
NOODLES_EMAIL_LIST = []

Assets From Image
-----------------