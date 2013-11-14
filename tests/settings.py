import os
BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'user_sessions',
    'tests',
]

MIDDLEWARE_CLASSES = (
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'tests.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

GEOIP_PATH = os.path.join(os.path.dirname(BASE_DIR),
                          'example', 'GeoLiteCity.dat')
SESSION_ENGINE = 'user_sessions.backends.db'
