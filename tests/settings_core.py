"""
Alliance Auth Test Suite Django settings

Testing core packages only
"""

from allianceauth.project_template.project_name.settings.base import *

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    #'--with-coverage',
    #'--cover-package=',
    #'--exe',  # If your tests need this to be found/run, check they py files are not chmodded +x
]

# Celery configuration
CELERY_ALWAYS_EAGER = True  # Forces celery to run locally for testing

INSTALLED_APPS += [    
    'django_nose',
]

ROOT_URLCONF = 'tests.urls'

CACHES['default'] = {'BACKEND': 'django.core.cache.backends.db.DatabaseCache'}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGGING = None  # Comment out to enable logging for debugging
