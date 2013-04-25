Django Noodles
==============
Noodles is an app containing all sorts of misc. bits of code that I see to use across projects.

There aren't really any connecting dots or common design patterns. It's just stuff I use.

Website Metadata
----------------
Website metadata consists of key/value pairs that can be used in templates. After a syncdb with noodles installed, this will be available in the admin interface.

You'll need to add noodles.context_processors.site_meta to your context processors.
	TEMPLATE_CONTEXT_PROCESSORS = (
	    ...
	    'noodles.context_processors.site_meta',
	    ...	    
	)

For example, perhaps you don't want to hardcode something like a user's Twitter URL into your templates. Instead, you could assign a key/value pair like this:
	key: MY_TWITTER
	value: http://twitter.com/someuser

Then, in your templates, you can refer to it like this:
	<a href="{{ SITE_META.MY_TWITTER }}">Follow me!</a>

Contact Submission
------------------
NOODLES_EMAIL_LIST = []

Abstract Models
---------------
### LittleSlugger
### ActiveToggler
### TitleDateSlug
### NameSlug
### NameSlugActive

Assets From Image
-----------------