Noodles for Django
==============
Noodles is an app containing all sorts of misc. bits of code that I see to use across projects.

There aren't really any connecting dots or common design patterns. It's just stuff I use.

## Documentation
The pieces that noodles offers are explained in the [Documentation](http://brant.github.io/django-noodles/)

## Quickstart
First, install with pip (for the time being, noodles is only available directly from github):
```
pip install git+https://github.com/Brant/django-noodles.git@master
```

Then, add noodles to your installed apps:
```python
INSTALLED_APPS = (
    ...
    'noodles',
)
```

## Tests
To run the the test suite:
```
virtualenv env
. ./env/bin/activate
pip install -r noodles_tests/requirements.txt
./noodles_tests/runtests.py
```
