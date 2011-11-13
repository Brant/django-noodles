import os
import sys

from setuptools import setup, find_packages

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    
    Taken from Django's setup.py
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)



def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Taken from Django's setup.py
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != "":
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk("noodles"):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])    


setup(
    name = "django-noodles",
    version = ".1",
    url = 'http://github.com/Brant/django-noodles',
    license = 'GPL',
    description = "Half-baked noodles of ideas for little bits of functionality for Django",
    long_description = read('README.md'),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',
    
    packages = packages,
    data_files = data_files,
    zip_safe = False,

    install_requires = ['setuptools', 'django'],

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)