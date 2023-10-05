Usage
=====

Current session
---------------
The current session is available on the request, just like the normal session
middleware makes the session available::

    def my_view(request):
        request.session


All sessions
------------
To get the list of a user's sessions::

    sessions = user.session_set.filter(expire_date__gt=now())

You could logout the user everywhere::

    user.session_set.all().delete()


Generic views
-------------
There are two views included with this application,
:class:`~user_sessions.views.SessionListView` and
:class:`~user_sessions.views.SessionDeleteView`. Using this views you have a
simple, but effective, user session management that even looks great out of
the box:

.. image:: _static/custom-view.png

Template tags
~~~~~~~~~~~~~

- ``browser`` - used to get just
  the browser from a session
- ``platform`` - used to get just
  the operating system from a session
- ``device`` - used to get both
  the user's browser and the operating system from a session

    .. code-block:: html+django

        {% load user_sessions %}
        {{ session.user_agent|device }}   -> Safari on macOS
        {{ session.user_agent|browser }}  -> Safari
        {{ session.user_agent|platform }} -> macOS

- ``location`` - used to show an
  approximate location of the last IP address for a session

    .. code-block:: html+django

        {% load user_sessions %}
        {{ session.ip|location }} -> Zwolle, The Netherlands


Admin views
-----------

The user's IP address and user agent are also stored on the session. This
allows to show a list of active sessions to the user in the admin:

.. image:: _static/admin-view.png
