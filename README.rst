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

Also, have a look at the online `example app`_, hosted by Heroku_. It also
contains the package `django-two-factor-auth`_, but that application is not a
dependency for this package. Also have a look at the bundled example templates
and views to see how you can integrate the application into your project.

Compatible with Django 1.8, 1.9 and 1.10 on Python 2.7, 3.2, 3.3, 3.4 and 3.5.
Documentation is available at `readthedocs.org`_.


Features
========

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
6. Run ``python manage.py syncdb`` (or ``migrate``) and browse to
   ``/account/sessions/``.

GeoIP
-----
You need to setup GeoIP for the location detection to work. See the Django
documentation on `installing GeoIP`_.


Getting help
============

For general questions regarding this package, please hop over to Stack 
Overflow. If you think there is an issue with this package; check if the
issue is already listed (either open or closed), and file an issue if
it's not.


Development
===========

How to contribute
-----------------
* Fork the repository on GitHub and start hacking.
* Run the tests.
* Send a pull request with your changes.
* Provide a translation using Transifex_.

Running tests
-------------
This project aims for full code-coverage, this means that your code should be
well-tested. Also test branches for hardened code. You can run the full test
suite with::

    make test

Or run a specific test with::

    make test TARGET=tests.tests.MiddlewareTest

For Python compatibility, tox_ is used. You can run the full test suite with::

    tox

Releasing
---------
The following actions are required to push a new version:

* Update release notes
* If any new translations strings were added, push the new source language to
  Transifex_. Make sure translators have sufficient time to translate those
  new strings::

    make tx-push

* Add migrations::

    python example/manage.py makemigrations user_sessions
    git commit user_sessions/migrations -m "Added migrations"

* Update translations::

    make tx-pull

* Package and upload::

    bumpversion [major|minor|patch]
    git push && git push --tags
    python setup.py sdist bdist_wheel
    twine upload dist/*


License
=======
This project is licensed under the MIT license.


.. _Transifex: https://www.transifex.com/projects/p/django-user-sessions/
.. _`readthedocs.org`: http://django-user-sessions.readthedocs.org/
.. _`example app`: http://example-two-factor-auth.herokuapp.com
.. _Heroku: https://www.heroku.com
.. _`django-two-factor-auth`: https://github.com/Bouke/django-two-factor-auth
.. _installing GeoIP:
   https://docs.djangoproject.com/en/1.6/ref/contrib/gis/geoip/
.. _tox: https://testrun.org/tox/latest/
