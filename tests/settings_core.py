"""
Alliance Auth Test Suite Django settings

Testing core packages only
"""

from allianceauth.project_template.project_name.settings.base import *

# Celery configuration
CELERY_ALWAYS_EAGER = True  # Forces celery to run locally for testing


ROOT_URLCONF = 'tests.urls'

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "localhost:6379",
        "OPTIONS": {
            "DB": 1,
        }
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGGING = None  # Comment out to enable logging for debugging
