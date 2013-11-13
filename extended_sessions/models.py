import django
from django.conf import settings
from django.contrib.sessions.models import SessionManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Session(models.Model):
    """
    Django provides full support for anonymous sessions. The session
    framework lets you store and retrieve arbitrary data on a
    per-site-visitor basis. It stores data on the server side and
    abstracts the sending and receiving of cookies. Cookies contain a
    session ID -- not the data itself.

    The Django sessions framework is entirely cookie-based. It does
    not fall back to putting session IDs in URLs. This is an intentional
    design decision. Not only does that behavior make URLs ugly, it makes
    your site vulnerable to session-ID theft via the "Referer" header.

    For complete documentation on using Sessions in your code, consult
    the sessions documentation that is shipped with Django (also available
    on the Django Web site).
    """
    session_key = models.CharField(_('session key'), max_length=40,
                                   primary_key=True)
    session_data = models.TextField(_('session data'))
    expire_date = models.DateTimeField(_('expire date'), db_index=True)
    objects = SessionManager()

    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

    def get_decoded(self):
        return SessionStore().decode(self.session_data)


    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    device = models.CharField(max_length=100)
    if django.VERSION[:2] >= (1, 6):
        ip = models.GenericIPAddressField()
    else:
        ip = models.IPAddressField()


# At bottom to avoid circular import
from .backends.db import SessionStore
