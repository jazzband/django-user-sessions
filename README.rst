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

Compatible with Django 1.4, 1.5, 1.6 and 1.7 on Python 2.6, 2.7, 3.2, 3.3 and
3.4. Documentation is available at `readthedocs.org`_.


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


.. include:: docs/installation.rst

Contribute
==========
* Fork the repository on GitHub and start hacking.
* Run the tests.
* Send a pull request with your changes.
* Provide a translation using Transifex_.


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
