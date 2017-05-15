# coding: utf-8
import os
import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import call_command
from django.http import HttpResponse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, '..'))

conf_kwargs = dict(
    ALLOWED_HOSTS=('testserver', '127.0.0.1', 'localhost', '::1'),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test.db',
            'TEST_NAME': 'test.db'
        }
    },
    SITE_ID=1,
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'online_users.middleware.OnlineNowMiddleware',
    ],
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'online_users'
    ),
    ROOT_URLCONF=(
        url(r'^', lambda _: HttpResponse('<h1>Hello World</h1')),
    ),
)

settings.configure(**conf_kwargs)

try:
    # For django>=1.10
    from django import setup
except ImportError:
    pass
else:
    setup()

call_command('migrate')


# from django.test.utils import get_runner
# runner = get_runner(settings)()
# runner.run_tests(('online_users',))
