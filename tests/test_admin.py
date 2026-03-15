from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from user_sessions.backends.db import SessionStore

from .utils import Client


class AdminTest(TestCase):
    client_class = Client

    def setUp(self):
        User.objects.create_superuser('bouke', '', 'secret')
        assert self.client.login(username='bouke', password='secret')

        expired = SessionStore(user_agent='Python/2.5', ip='20.13.1.1')
        expired.set_expiry(-365 * 86400)
        expired.save()
        unexpired = SessionStore(user_agent='Python/2.7', ip='1.1.1.1')
        unexpired.save()

        self.admin_url = reverse('admin:user_sessions_session_changelist')

    def test_list(self):
        response = self.client.get(self.admin_url)
        self.assertContains(response, 'Select session to change')
        self.assertContains(response, '127.0.0.1')
        self.assertContains(response, '20.13.1.1')
        self.assertContains(response, '1.1.1.1')

    def test_search(self):
        response = self.client.get(self.admin_url, {'q': 'bouke'})
        self.assertContains(response, '127.0.0.1')
        self.assertNotContains(response, '20.13.1.1')
        self.assertNotContains(response, '1.1.1.1')

    def test_mine(self):
        my_sessions = f"{self.admin_url}?{urlencode({'owner': 'my'})}"
        response = self.client.get(my_sessions)
        self.assertContains(response, '127.0.0.1')
        self.assertNotContains(response, '1.1.1.1')

    def test_expired(self):
        expired = f"{self.admin_url}?{urlencode({'active': '0'})}"
        response = self.client.get(expired)
        self.assertContains(response, '20.13.1.1')
        self.assertNotContains(response, '1.1.1.1')

    def test_unexpired(self):
        unexpired = f"{self.admin_url}?{urlencode({'active': '1'})}"
        response = self.client.get(unexpired)
        self.assertContains(response, '1.1.1.1')
        self.assertNotContains(response, '20.13.1.1')
