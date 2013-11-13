from datetime import timedelta
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.utils.timezone import now

from user_sessions.backends.db import SessionStore
from user_sessions.models import Session


class SessionStoreTest(TestCase):
    def setUp(self):
        self.store = SessionStore('Python/2.7', '127.0.0.1', None)

    def test_untouched_init(self):
        self.assertFalse(self.store.modified)
        self.assertFalse(self.store.accessed)

    def test_auth_session_key(self):
        _ = SESSION_KEY in self.store
        self.assertFalse(self.store.modified)
        self.assertTrue(self.store.accessed)

        self.store.get(SESSION_KEY)
        self.assertFalse(self.store.modified)

        self.store[SESSION_KEY] = 1
        self.assertTrue(self.store.modified)

    def test_save(self):
        self.store[SESSION_KEY] = 1
        self.store.save()

        session = Session.objects.get(pk=self.store.session_key)
        self.assertEqual(session.user_agent, 'Python/2.7')
        self.assertEqual(session.ip, '127.0.0.1')
        self.assertEqual(session.user_id, 1)
        self.assertAlmostEqual(now(), session.last_activity,
                               delta=timedelta(seconds=5))

    def test_load_unmodified(self):
        self.store[SESSION_KEY] = 1
        self.store.save()
        store2 = SessionStore('Python/2.7', '127.0.0.1', self.store.session_key)
        store2.load()
        self.assertEqual(store2.user_agent, 'Python/2.7')
        self.assertEqual(store2.ip, '127.0.0.1')
        self.assertEqual(store2.user_id, 1)
        self.assertEqual(store2.modified, False)

    def test_load_modified(self):
        self.store[SESSION_KEY] = 1
        self.store.save()
        store2 = SessionStore('Python/3.3', '8.8.8.8', self.store.session_key)
        store2.load()
        self.assertEqual(store2.user_agent, 'Python/3.3')
        self.assertEqual(store2.ip, '8.8.8.8')
        self.assertEqual(store2.user_id, 1)
        self.assertEqual(store2.modified, True)
