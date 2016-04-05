#!/usr/bin/env python
import sys
import os

import django
from django.conf import settings
from django.test.utils import get_runner


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

if not settings.configured:
    settings.configure(
        BASE_DIR = BASE_DIR,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'noodles',
            'noodles_tests',
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sites',
        ],
        SITE_ID=1,
        STATIC_URL='/static/',
        MEDIA_URL='/media/',
        ROOT_URLCONF='noodles_tests.urls',
    )


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["noodles_tests"])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests(*sys.argv[1:])
