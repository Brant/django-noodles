from setuptools import setup, find_packages


setup(
    name = "django-noodles",
    version = "0.2.3",
    url = 'http://github.com/Brant/django-noodles',
    license = 'GPL',
    description = "Half-baked noodles of ideas for little bits of functionality for Django",
    long_description = open('README.md').read(),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',

    packages = find_packages(exclude=('noodles_tests', )),
    include_package_data = True,
    zip_safe = False,


    install_requires = ['django', ],

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
