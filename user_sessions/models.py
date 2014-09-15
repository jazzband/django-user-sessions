import django
from django.conf import settings
from django.contrib.sessions.models import SessionManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Session(models.Model):
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
    session_key = models.CharField(_('session key'), max_length=40,
                                   primary_key=True)
    session_data = models.TextField(_('session data'))
    expire_date = models.DateTimeField(_('expiry date'), db_index=True)
    objects = SessionManager()

    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

    def get_decoded(self):
        return SessionStore(None, None).decode(self.session_data)

    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             to_field=getattr(settings, 'USER_SESSIONS_USER_TO_FIELD', None),
                             null=True)
    user_agent = models.CharField(max_length=200)
    last_activity = models.DateTimeField(auto_now=True)
    if django.VERSION[:2] >= (1, 6):
        ip = models.GenericIPAddressField()
    else:
        ip = models.IPAddressField()


# At bottom to avoid circular import
from .backends.db import SessionStore
