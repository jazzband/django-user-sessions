from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from user_sessions.models import Session


class MiddlewareTest(TestCase):
    def test_unmodified_session(self):
        self.client.get('/', HTTP_USER_AGENT='Python/2.7')
        self.assertNotIn(settings.SESSION_COOKIE_NAME, self.client.cookies)

    def test_modify_session(self):
        self.client.get('/modify_session/', HTTP_USER_AGENT='Python/2.7')
        self.assertIn(settings.SESSION_COOKIE_NAME, self.client.cookies)
        session = Session.objects.get(
            pk=self.client.cookies[settings.SESSION_COOKIE_NAME].value
        )
        self.assertEqual(session.user_agent, 'Python/2.7')
        self.assertEqual(session.ip, '127.0.0.1')

    def test_login(self):
        admin_login_url = reverse('admin:login')
        user = User.objects.create_superuser('bouke', '', 'secret')
        response = self.client.post(admin_login_url,
                                    data={
                                        'username': 'bouke',
                                        'password': 'secret',
                                        'this_is_the_login_form': '1',
                                        'next': '/admin/'},
                                    HTTP_USER_AGENT='Python/2.7')
        self.assertRedirects(response, '/admin/')
        session = Session.objects.get(
            pk=self.client.cookies[settings.SESSION_COOKIE_NAME].value
        )
        self.assertEqual(
            self.client.cookies[settings.SESSION_COOKIE_NAME]["samesite"],
            settings.SESSION_COOKIE_SAMESITE,
        )
        self.assertEqual(user, session.user)

    def test_long_ua(self):
        self.client.get('/modify_session/',
                        HTTP_USER_AGENT=''.join('a' for _ in range(400)))
