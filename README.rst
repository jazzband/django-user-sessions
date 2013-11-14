====================
Django User Sessions
====================

.. image:: https://travis-ci.org/Bouke/django-user-sessions.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/Bouke/django-user-sessions

Django includes excellent built-in sessions, however all the data is hidden
away into a base64 encoded data string. This makes it very difficult to run a
query on all active sessions for a particular user. Django User Sessions fixes
this and makes session objects just as queryable as other objects.

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

1. ``pip install django-user-sessions --pre``
2. In ``INSTALLED_APPS`` replace ``'django.contrib.sessions'`` with
   ``'user_sessions'``.
3. In ``MIDDLEWARE_CLASSES`` replace
   ``'django.contrib.sessions.middleware.SessionMiddleware'`` with
   ``'user_sessions.middleware.SessionMiddleware'``.
4. Add ``SESSION_ENGINE = 'user_sessions.backends.db'``.
5. Run ``python manage.py syncdb`` and start hacking!

GeoIP
-----
You need to setup GeoIP for the location detection to work. See the Django
documentation on `installing GeoIP`_.

.. _installing GeoIP:
   https://docs.djangoproject.com/en/1.6/ref/contrib/gis/geoip/

Demo application
----------------
Also, have a look at the demo application. It includes template examples and
shows how to use the session list and delete views.

Compatibility
-------------
Tested on Django 1.6 with Python 2.7 and 3.3. However it should work fine on
Django 1.4 and above.

Contributing
============
* Fork the repository on GitHub and start hacking
* Send a pull request with your changes
