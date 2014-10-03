Installation
============
1. ``pip install django-user-sessions``
2. In ``INSTALLED_APPS`` replace ``'django.contrib.sessions'`` with
   ``'user_sessions'``.
3. In ``MIDDLEWARE_CLASSES`` replace
   ``'django.contrib.sessions.middleware.SessionMiddleware'`` with
   ``'user_sessions.middleware.SessionMiddleware'``.
4. Setup ``SESSION_ENGINE`` setting: Please see `Session Engine`_ to choose the
   best option for your project.
5. Add ``url(r'', include('user_sessions.urls', 'user_sessions')),`` to your
   ``urls.py``.

GeoIP
-----
You need to setup GeoIP for the location detection to work. See the Django
documentation on `installing GeoIP`_.


Session Engine
--------------
``django-user-sessions`` supports two types of Session Engine.

database-backed
  Sessions will be stored in the database::

    SESSION_ENGINE = 'user_sessions.backends.db'

  You will need to run ``python manage.py syncdb`` (or ``migrate``)

cached
   Session data is stored using Django's cache system. Depending on the cache system can be
   persistent or not::

     SESSION_ENGINE = 'user_sessions.backends.db'

   For configuring the Django's cache system, please read `configuring Cache`_.

For for information about sessions, see the Django documentation on `configuring SessionEngine`_.


.. _installing GeoIP:
   https://docs.djangoproject.com/en/1.6/ref/contrib/gis/geoip/
.. _configuring SessionEngine:
   https://docs.djangoproject.com/en/1.6/topics/http/sessions/
.. _configuring Cache:
   https://docs.djangoproject.com/en/1.6/topics/cache/
