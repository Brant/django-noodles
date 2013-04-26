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
from noodles.models import LittleSlugger

class MySluggedModel(LittleSlugger):
    title = models.CharField(max_length=50)
    
    def get_slug_target(self):
        return "title"	    
```
Not adding the "get_slug_target" method to your model will raise NotImplementedError.

Little Slugger will look for another object of the same model type with a matching slug. If it finds one, it will append a number (in sequence) to the end of the slug.

For example, if you had an entry with a title of "A good day", it would have a slug of "a-good-day". If you then made _another_ entry titled "A good day", it would end up with a slug of "a-good-day-1". If a third entry with the same title was created, it would become "a-good-day-2". This allows reliably querying on slugs, as if they would always be unique.

Another default behavior of LittleSlugger is to keep the slug, once it has been established, even if the sluggified field should change. This allows, for example, title changes on blog posts without changing the URL of that post.

For example, if you titled a post "A good days" and published it, you might have a URL of "http://myblog.com/a-good-days/". Realizing it should be titled "A good day", you would change the title. However, the slug would stay the same, keeping any pointers to the URL the same as well.

To disable this behavior, you simply need to make a small addition to the "get_slug_target" method.
```python
from noodles.models import LittleSlugger

class MySluggedModel(LittleSlugger):
    title = models.CharField(max_length=50)
    
    def get_slug_target(self):
        return ("title", False)	    
```
The second variable returned in the tuple designates whether or not the slug should "persist" through field changes.

### ActiveToggler
Active Toggler lets you toggle 1 entry of the model to be considered "active". Only 1 entry can be active at a time. 

Active Toggler adds an "active" attribute to your model. When an object of the model is saved (by calling .save()) and set to active=True, it will run through all other entries for the model and set them all to active=False.

```python
from noodles.models import ActiveToggler

class FavoriteIcecream(ActiveToggler):
    """ You can only have 1 favorite at a time """
    name = models.CharField(max_length=50)
```

You could then use the model to query as if "active" was a unique field.
```python
current_favorite_icecream = FavoriteIcecream.objects.get(active=True)
```

### NameSlug
NameSlug is a subclass of LittleSlugger, which has a "name" attribute. That name attribute is what the slug will be built from.

### NameSlugActive
NameSlugActive is a subclass of NameSlug (which is a subclass of LittleSlugger). In addition to a name and a slug of that name, there is an "active" attribute (BooleanField that defaults to True). 

**Note:** The 'active' attribute is _not_ a toggler (like ActiveToggler's active field).
 
### TitleDateSlug
TitleDateSlug is a subclass of LittleSlugger. It's attributes are 'title', 'date', and 'slug'. Slug is derived from the title. 

The date attribute could be used as something like a publish date. It does not auto-populate.


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