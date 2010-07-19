"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1
(C) 2010 oDesk www.oDesk.com
"""


# Django settings for mailposttest project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
DIRNAME = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = DIRNAME + '/test.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'some_secret_key'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'mailposttest.urls'

TEMPLATE_DIRS = (
     os.path.join(DIRNAME, 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'mailposttest.testapp',
    'mailpost',
)
LOGIN_REDIRECT_URL = '/admin/'
