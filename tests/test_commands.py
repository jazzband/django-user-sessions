from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase
from django.test.utils import modify_settings
from django.utils.timezone import now

from user_sessions.models import Session


class ClearsessionsCommandTest(TestCase):
    def test_can_call(self):
        Session.objects.create(expire_date=now() - timedelta(days=1),
                               ip='127.0.0.1')
        call_command('clearsessions')
        self.assertEqual(Session.objects.count(), 0)


class MigratesessionsCommandTest(TransactionTestCase):
    @modify_settings(INSTALLED_APPS={'append': 'django.contrib.sessions'})
    def test_migrate_from_login(self):
        from django.contrib.sessions.backends.db import (
            SessionStore as DjangoSessionStore,
        )
        from django.contrib.sessions.models import Session as DjangoSession
        try:
            call_command('migrate', 'sessions')
            call_command('clearsessions')
            user = User.objects.create_user('bouke', '', 'secret')
            session = DjangoSessionStore()
            session['_auth_user_id'] = user.id
            session.save()
            self.assertEqual(Session.objects.count(), 0)
            self.assertEqual(DjangoSession.objects.count(), 1)
            call_command('migratesessions')
            new_sessions = list(Session.objects.all())
            self.assertEqual(len(new_sessions), 1)
            self.assertEqual(new_sessions[0].user, user)
            self.assertEqual(new_sessions[0].ip, '127.0.0.1')
        finally:
            call_command('migrate', 'sessions', 'zero')
