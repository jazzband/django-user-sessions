Installation
============
1. ``pip install django-user-sessions``
2. In ``INSTALLED_APPS`` replace ``'django.contrib.sessions'`` with
   ``'user_sessions'``.
3. In ``MIDDLEWARE_CLASSES`` replace
   ``'django.contrib.sessions.middleware.SessionMiddleware'`` with
   ``'user_sessions.middleware.SessionMiddleware'``.
4. Add ``SESSION_ENGINE = 'user_sessions.backends.db'``.
5. Add ``url(r'', include('user_sessions.urls', 'user_sessions')),`` to your
   ``urls.py``.
6. Make sure ``LOGOUT_REDIRECT_URL`` is set to some page to redirect users
   after logging out.
7. Run ``python manage.py syncdb`` (or ``migrate``) and browse to
   ``/account/sessions/``.

GeoIP
-----
You need to setup GeoIP for the location detection to work. See the Django
documentation on `installing GeoIP`_.

.. _installing GeoIP:
   https://docs.djangoproject.com/en/1.6/ref/contrib/gis/geoip/

IP Data Accuracy
----------------
If you're running Django behind a proxy like nginx, you will have to set 
the `REMOTE_ADDR` META header manually using a middleware, to stop it from 
always returning the ip of the proxy (e.g. 127.0.0.1 in many cases).

An example middleware to fix this issue is https://github.com/allo-/django-xforwardedfor-middleware
Which simply does this for each request:

``request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()``

Your particular configuration may vary, X-Forwarded-For is not always accurate in some cases.
