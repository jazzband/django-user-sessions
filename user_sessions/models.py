from django.conf import settings
from django.contrib.sessions.base_session import (
    AbstractBaseSession, BaseSessionManager,
)
from django.db import models

from .backends.db import SessionStore


class SessionManager(BaseSessionManager):
    use_in_migrations = True


# https://docs.djangoproject.com/en/4.2/topics/http/sessions/#extending-database-backed-session-engines
class Session(AbstractBaseSession):
    """
    Session objects containing user session information.

    Django provides full support for anonymous sessions. The session
    framework lets you store and retrieve arbitrary data on a
    per-site-visitor basis. It stores data on the server side and
    abstracts the sending and receiving of cookies. Cookies contain a
    session ID -- not the data itself.

    Additionally this session object providers the following properties:
    ``user``, ``user_agent`` and ``ip``.
    """
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             null=True, on_delete=models.CASCADE)
    user_agent = models.CharField(null=True, blank=True, max_length=200)
    last_activity = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')

    objects = SessionManager()

    # Used in get_decoded
    @classmethod
    def get_session_store_class(cls):
        return SessionStore
