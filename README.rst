====================
Django User Sessions
====================

.. image:: https://jazzband.co/static/img/badge.svg
    :target: https://jazzband.co/
    :alt: Jazzband

.. image:: https://github.com/jazzband/django-user-sessions/workflows/Test/badge.svg
    :alt: GitHub Actions
    :target: https://github.com/jazzband/django-user-sessions/actions

.. image:: https://codecov.io/gh/jazzband/django-user-sessions/branch/master/graph/badge.svg
    :alt: Test Coverage
    :target: https://codecov.io/gh/jazzband/django-user-sessions

.. image:: https://badge.fury.io/py/django-user-sessions.svg
    :alt: PyPI
    :target: https://pypi.python.org/pypi/django-user-sessions

Django includes excellent built-in sessions, however all the data is hidden
away into base64 encoded data. This makes it very difficult to run a query on
all active sessions for a particular user. `django-user-sessions` fixes this
and makes session objects a first class citizen like other ORM objects. It is
a drop-in replacement for `django.contrib.sessions`.

I would love to hear your feedback on this package. If you run into
problems, please file an issue on GitHub, or contribute to the project by
forking the repository and sending some pull requests. The package is
translated into English, Dutch and other languages. Please contribute your own
language using Transifex_.

Also have a look at the bundled example templates and views to see how you
can integrate the application into your project.

Compatible with Django 3.2 and 4.0 on Python 3.7, 3.8, 3.9 and 3.10.
Documentation is available at `readthedocs.org`_.


Features
========

To get the list of a user's sessions:

.. code-block:: python

    user.session_set.filter(expire_date__gt=now())

Or logout the user everywhere:

.. code-block:: python

    user.session_set.all().delete()

The user's IP address and user agent are also stored on the session. This
allows to show a list of active sessions to the user in the admin:

.. image:: http://i.imgur.com/YV9Nx3f.png

And also in a custom layout:

.. image:: http://i.imgur.com/d7kZtr9.png


Installation
============
Refer to the `installation instructions`_ in the documentation.

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


Credits
=======
This library was written by `Bouke Haarsma`_ and contributors_.


.. _Transifex: https://www.transifex.com/projects/p/django-user-sessions/
.. _`readthedocs.org`: https://django-user-sessions.readthedocs.org/
.. _`installation instructions`:
   https://django-user-sessions.readthedocs.io/en/stable/installation.html
.. _installing GeoIP:
   https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geoip2/
.. _tox: https://testrun.org/tox/latest/
.. _Bouke Haarsma:
   https://github.com/Bouke
.. _contributors:
   https://github.com/jazzband/django-user-sessions/graphs/contributors
