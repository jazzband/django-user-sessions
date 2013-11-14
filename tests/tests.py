from datetime import timedelta
from unittest import skipUnless

from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.utils.timezone import now

from user_sessions.backends.db import SessionStore
from user_sessions.models import Session
from user_sessions.templatetags.user_sessions import location, device

try:
    from django.contrib.gis.geoip import GeoIP
    geoip = GeoIP()
    geoip_msg = None
except Exception as e:
    geoip = None
    geoip_msg = str(e)


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


@skipUnless(geoip, geoip_msg)
class LocationTemplateFilterTest(TestCase):
    def test_no_location(self):
        self.assertEqual(location('127.0.0.1'), '<i>unknown</i>')

    def test_google(self):
        self.assertEqual(location('8.8.8.8'), 'United States')


class DeviceTemplateFilterTest(TestCase):
    def test_ie(self):
        self.assertEqual(
            'Internet Explorer on Windows XP',
            device('Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; '
                   '.NET CLR 2.0.50727)')
        )
        self.assertEqual(
            'Internet Explorer on Windows Vista',
            device('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; '
                   'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; '
                   'InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; '
                   'MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; '
                   '.NET CLR 3.0.30729)')
        )
        self.assertEqual(
            'Internet Explorer on Windows 7',
            device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                   'Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer on Windows 8',
            device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; '
                   'x64; Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer on Windows 8.1',
            device('Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; '
                   '.NET4.0E; .NET4.0C; rv:11.0) like Gecko')
        )

    def test_apple(self):
        self.assertEqual(
            'Safari on iPad',
            device('Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) '
                   'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
                   'Mobile/8C148 Safari/6533.18.5')
        )
        self.assertEqual(
            'Safari on iPhone',
            device('Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) '
                   'AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
                   'Mobile/11A465 Safari/9537.53')
        )
        self.assertEqual(
            'Safari on Mac OS X',
            device('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
                   'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
                   'Safari/536.26.17')
        )

    def test_android(self):
        # androids identify themselves as Safari to get the good stuff
        self.assertEqual(
            'Safari on Android',
            device('Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic '
                   'Build/CRB17) AppleWebKit/528.5+ (KHTML, like Gecko) '
                   'Version/3.1.2 Mobile Safari/525.20.1')
        )

