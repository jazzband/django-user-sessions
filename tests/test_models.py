from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase

from user_sessions.backends.db import SessionStore
from user_sessions.models import Session


class ModelTest(TestCase):
    def test_get_decoded(self):
        User.objects.create_user('bouke', '', 'secret', id=1)
        store = SessionStore(user_agent='Python/2.7', ip='127.0.0.1')
        store[auth.SESSION_KEY] = 1
        store['foo'] = 'bar'
        store.save()

        session = Session.objects.get(pk=store.session_key)
        self.assertEqual(session.get_decoded(),
                         {'foo': 'bar', auth.SESSION_KEY: 1})

    def test_very_long_ua(self):
        ua = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; ' \
             'Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; ' \
             '.NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; ' \
             'InfoPath.3; ms-office; MSOffice 14)'
        store = SessionStore(user_agent=ua, ip='127.0.0.1')
        store.save()

        session = Session.objects.get(pk=store.session_key)
        self.assertEqual(session.user_agent, ua[:200])
