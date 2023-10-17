from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from .utils import Client


class ViewsTest(TestCase):
    client_class = Client

    def setUp(self):
        self.user = User.objects.create_user('bouke', '', 'secret')
        assert self.client.login(username='bouke', password='secret')

    def test_list(self):
        self.user.session_set.create(session_key='ABC123', ip='127.0.0.1',
                                     expire_date=now() + timedelta(days=1),
                                     user_agent='Firefox')
        with self.assertWarnsRegex(UserWarning, r"The address 127\.0\.0\.1 is not in the database"):
            response = self.client.get(reverse('user_sessions:session_list'))
        self.assertContains(response, 'Active Sessions')
        self.assertContains(response, 'Firefox')
        self.assertNotContains(response, 'ABC123')

    def test_delete(self):
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        response = self.client.post(reverse('user_sessions:session_delete',
                                            args=[session_key]))
        self.assertRedirects(response, '/')

    def test_delete_all_other(self):
        self.user.session_set.create(ip='127.0.0.1', expire_date=now() + timedelta(days=1))
        self.assertEqual(self.user.session_set.count(), 2)
        response = self.client.post(reverse('user_sessions:session_delete_other'))
        with self.assertWarnsRegex(UserWarning, r"The address 127\.0\.0\.1 is not in the database"):
            self.assertRedirects(response, reverse('user_sessions:session_list'))
        self.assertEqual(self.user.session_set.count(), 1)

    def test_delete_some_other(self):
        other = self.user.session_set.create(session_key='OTHER', ip='127.0.0.1',
                                             expire_date=now() + timedelta(days=1))
        self.assertEqual(self.user.session_set.count(), 2)
        response = self.client.post(reverse('user_sessions:session_delete',
                                            args=[other.session_key]))
        with self.assertWarnsRegex(UserWarning, r"The address 127\.0\.0\.1 is not in the database"):
            self.assertRedirects(response, reverse('user_sessions:session_list'))
        self.assertEqual(self.user.session_set.count(), 1)
