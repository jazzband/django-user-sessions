from unittest.mock import patch

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from user_sessions.backends.db import SessionStore

from .utils import Client


class ClientTest(TestCase):
    def test_invalid_login(self):
        client = Client()
        self.assertFalse(client.login())

    def test_restore_session(self):
        store = SessionStore(user_agent='Python/2.7', ip='127.0.0.1')
        store['foo'] = 'bar'
        store.save()
        client = Client()
        client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        User.objects.create_user('bouke', '', 'secret')
        assert client.login(username='bouke', password='secret')
        self.assertEqual(client.session['foo'], 'bar')

    def test_login_logout(self):
        client = Client()
        User.objects.create_user('bouke', '', 'secret')
        assert client.login(username='bouke', password='secret')
        assert settings.SESSION_COOKIE_NAME in client.cookies

        client.logout()
        assert settings.SESSION_COOKIE_NAME not in client.cookies

        # should not raise
        client.logout()

    @patch('django.contrib.auth.signals.user_logged_in.send')
    def test_login_signal(self, mock_user_logged_in):
        client = Client()
        User.objects.create_user('bouke', '', 'secret')
        assert client.login(username='bouke', password='secret')
        assert mock_user_logged_in.called
        request = mock_user_logged_in.call_args[1]['request']
        assert getattr(request, 'user', None) is not None

    @override_settings(INSTALLED_APPS=())
    def test_no_session(self):
        self.assertIsNone(Client().session)
