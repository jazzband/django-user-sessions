====================
Django User Sessions
====================

.. image:: https://travis-ci.org/Bouke/django-user-sessions.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/Bouke/django-user-sessions

.. image:: https://coveralls.io/repos/Bouke/django-user-sessions/badge.png?branch=master
    :alt: Test Coverage
    :target: https://coveralls.io/r/Bouke/django-user-sessions?branch=master

.. image:: https://badge.fury.io/py/django-user-sessions.png
    :alt: PyPI
    :target: https://pypi.python.org/pypi/django-user-sessions

Django includes excellent built-in sessions, however all the data is hidden
away into base64 encoded data. This makes it very difficult to run a query on
all active sessions for a particular user. `django-user-sessions` fixes this
and makes session objects a first class citizen like other ORM objects.

To get the list of a user's sessions::

    user.session_set.filter(expire_date__gt=now())

Or logout the user everywhere::

    user.session_set.all().delete()

The user's IP address and user agent are also stored on the session. This
allows to show a list of active sessions to the user in the admin:

.. image:: http://i.imgur.com/YV9Nx3f.png

And also in a custom layout:

.. image:: http://i.imgur.com/d7kZtr9.png

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
6. Run ``python manage.py syncdb`` (or ``migrate``) and start hacking!

GeoIP
-----
You need to setup GeoIP for the location detection to work. See the Django
documentation on `installing GeoIP`_.

.. _installing GeoIP:
   https://docs.djangoproject.com/en/1.6/ref/contrib/gis/geoip/

Example application
-------------------
Also, have a look at the example application. It includes template examples and
shows how to use the session list and delete views.

Compatibility
-------------
Tested on Django 1.4, 1.5 and 1.6 with Python 2.7 and 3.3. However it should 
work fine with Python 2.6 and 3.2 as well.

Contributing
============
* Fork the repository on GitHub and start hacking.
* Run the tests.
* Send a pull request with your changes.
* Provide a translation using Transifex_.

.. _Transifex: https://www.transifex.com/projects/p/django-user-sessions/
