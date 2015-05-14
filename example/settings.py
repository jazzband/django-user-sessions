import os

DEBUG = True
TEMPLATE_DEBUG = True

PROJECT_PATH = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'database.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

STATIC_URL = '/static/'

SECRET_KEY = 'DO NOT USE THIS KEY!'

MIDDLEWARE_CLASSES = (
    'example.middleware.SetRemoteAddrFromForwardedFor',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_sessions',
    'debug_toolbar',
)


# Custom configuration

SESSION_ENGINE = 'user_sessions.backends.db'

GEOIP_PATH = os.path.join(PROJECT_PATH, 'GeoLiteCity.dat')

LOGIN_URL = '/admin/'
