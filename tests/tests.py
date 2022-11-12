from datetime import datetime, timedelta
from unittest import skipUnless
from unittest.mock import patch
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import CreateError
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase
from django.test.utils import modify_settings, override_settings
from django.urls import reverse
from django.utils.timezone import now

from user_sessions.backends.db import SessionStore
from user_sessions.models import Session
from user_sessions.templatetags.user_sessions import device, location
from user_sessions.utils.tests import Client

try:
    from django.contrib.gis.geoip2 import GeoIP2
    geoip = GeoIP2()
    geoip_msg = None
except Exception as error_geoip2:
    try:
        from django.contrib.gis.geoip import GeoIP
        geoip = GeoIP()
        geoip_msg = None
    except Exception as error_geoip:
        geoip = None
        geoip_msg = str(error_geoip2) + " and " + str(error_geoip)


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


class ViewsTest(TestCase):
    client_class = Client

    def setUp(self):
        self.user = User.objects.create_user('bouke', '', 'secret')
        assert self.client.login(username='bouke', password='secret')

    def test_list(self):
        self.user.session_set.create(session_key='ABC123', ip='127.0.0.1',
                                     expire_date=datetime.now() + timedelta(days=1),
                                     user_agent='Firefox')
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
        self.user.session_set.create(ip='127.0.0.1', expire_date=datetime.now() + timedelta(days=1))
        self.assertEqual(self.user.session_set.count(), 2)
        response = self.client.post(reverse('user_sessions:session_delete_other'))
        self.assertRedirects(response, reverse('user_sessions:session_list'))
        self.assertEqual(self.user.session_set.count(), 1)

    def test_delete_some_other(self):
        other = self.user.session_set.create(session_key='OTHER', ip='127.0.0.1',
                                             expire_date=datetime.now() + timedelta(days=1))
        self.assertEqual(self.user.session_set.count(), 2)
        response = self.client.post(reverse('user_sessions:session_delete',
                                            args=[other.session_key]))
        self.assertRedirects(response, reverse('user_sessions:session_list'))
        self.assertEqual(self.user.session_set.count(), 1)


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
        my_sessions = '{}?{}'.format(self.admin_url, urlencode({'owner': 'my'}))
        response = self.client.get(my_sessions)
        self.assertContains(response, '127.0.0.1')
        self.assertNotContains(response, '1.1.1.1')

    def test_expired(self):
        expired = '{}?{}'.format(self.admin_url, urlencode({'active': '0'}))
        response = self.client.get(expired)
        self.assertContains(response, '20.13.1.1')
        self.assertNotContains(response, '1.1.1.1')

    def test_unexpired(self):
        unexpired = '{}?{}'.format(self.admin_url, urlencode({'active': '1'}))
        response = self.client.get(unexpired)
        self.assertContains(response, '1.1.1.1')
        self.assertNotContains(response, '20.13.1.1')


class SessionStoreTest(TestCase):
    def setUp(self):
        self.store = SessionStore(user_agent='Python/2.7', ip='127.0.0.1')
        User.objects.create_user('bouke', '', 'secret', id=1)

    def test_untouched_init(self):
        self.assertFalse(self.store.modified)
        self.assertFalse(self.store.accessed)

    def test_auth_session_key(self):
        self.assertFalse(auth.SESSION_KEY in self.store)
        self.assertFalse(self.store.modified)
        self.assertTrue(self.store.accessed)

        self.store.get(auth.SESSION_KEY)
        self.assertFalse(self.store.modified)

        self.store[auth.SESSION_KEY] = 1
        self.assertTrue(self.store.modified)

    def test_save(self):
        self.store[auth.SESSION_KEY] = 1
        self.store.save()

        session = Session.objects.get(pk=self.store.session_key)
        self.assertEqual(session.user_agent, 'Python/2.7')
        self.assertEqual(session.ip, '127.0.0.1')
        self.assertEqual(session.user_id, 1)
        self.assertAlmostEqual(now(), session.last_activity,
                               delta=timedelta(seconds=5))

    def test_load_unmodified(self):
        self.store[auth.SESSION_KEY] = 1
        self.store.save()
        store2 = SessionStore(session_key=self.store.session_key,
                              user_agent='Python/2.7', ip='127.0.0.1')
        store2.load()
        self.assertEqual(store2.user_agent, 'Python/2.7')
        self.assertEqual(store2.ip, '127.0.0.1')
        self.assertEqual(store2.user_id, 1)
        self.assertEqual(store2.modified, False)

    def test_load_modified(self):
        self.store[auth.SESSION_KEY] = 1
        self.store.save()
        store2 = SessionStore(session_key=self.store.session_key,
                              user_agent='Python/3.3', ip='8.8.8.8')
        store2.load()
        self.assertEqual(store2.user_agent, 'Python/3.3')
        self.assertEqual(store2.ip, '8.8.8.8')
        self.assertEqual(store2.user_id, 1)
        self.assertEqual(store2.modified, True)

    def test_duplicate_create(self):
        s1 = SessionStore(session_key='DUPLICATE', user_agent='Python/2.7', ip='127.0.0.1')
        s1.create()
        s2 = SessionStore(session_key='DUPLICATE', user_agent='Python/2.7', ip='127.0.0.1')
        s2.create()
        self.assertNotEqual(s1.session_key, s2.session_key)

        s3 = SessionStore(session_key=s1.session_key, user_agent='Python/2.7', ip='127.0.0.1')
        with self.assertRaises(CreateError):
            s3.save(must_create=True)

    def test_delete(self):
        # not persisted, should just return
        self.store.delete()

        # create, then delete
        self.store.create()
        session_key = self.store.session_key
        self.store.delete()

        # non-existing sessions, should not raise
        self.store.delete()
        self.store.delete(session_key)

    def test_clear(self):
        """
        Clearing the session should clear all non-browser information
        """
        self.store[auth.SESSION_KEY] = 1
        self.store.clear()
        self.store.save()

        session = Session.objects.get(pk=self.store.session_key)
        self.assertEqual(session.user_id, None)


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


class LocationTemplateFilterTest(TestCase):
    @override_settings(GEOIP_PATH=None)
    def test_no_location(self):
        self.assertEqual(location('127.0.0.1'), None)

    @skipUnless(geoip, geoip_msg)
    def test_locations(self):
        self.assertEqual('United States', location('8.8.8.8'))
        self.assertEqual('San Diego, United States', location('44.55.66.77'))


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
                   'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
                   ' InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; '
                   'MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3;'
                   ' .NET CLR 3.0.30729)')
        )
        self.assertEqual(
            'Internet Explorer on Windows 7',
            device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                   'Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer on Windows 8',
            device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; '
                   'Win64; x64; Trident/6.0)')
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
            'Chrome on macOS Mojave',
            device('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/85.0.4178.0 Safari/537.36')
        )
        self.assertEqual(
            'Firefox on macOS Catalina',
            device('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) '
                   'Gecko/20100101 Firefox/77.0')
        )
        self.assertEqual(
            'Safari on macOS',
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

    def test_firefox(self):
        self.assertEqual(
            'Firefox on Windows 7',
            device('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) '
                   'Gecko/20130328 Firefox/22.0')
        )

    def test_chrome(self):
        self.assertEqual(
            'Chrome on Windows 8.1',
            device('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ('
                   'KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')
        )

    def test_edge(self):
        self.assertEqual(
            'Edge on Windows 10',
            device('Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, '
                   'like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136')
        )
        self.assertEqual(
            'Edge on Windows Mobile',
            device('Mozilla/5.0 (Windows Mobile 10; Android 8.0.0; Microsoft; Lumia '
                   '950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.62 '
                   'Mobile Safari/537.36 Edge/40.15254.369')
        )

    def test_edge_chromium(self):
        self.assertEqual(
            'Edge on Windows 10',
            device('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 '
                   'Safari/537.36 Edg/81.0.416.62')
        )
        self.assertEqual(
            'Edge on macOS Catalina',
            device('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 '
                   'Safari/537.36 Edg/85.0.564.51')
        )
        self.assertEqual(
            'Edge on Android',
            device('Mozilla/5.0 (Linux; Android 11; Pixel 3 XL) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 '
                   'Mobile Safari/537.36 EdgA/45.07.4.5059')
        )

    def test_firefox_only(self):
        self.assertEqual("Firefox", device("Not a legit OS Firefox/51.0"))

    def test_chrome_only(self):
        self.assertEqual("Chrome", device("Not a legit OS Chrome/54.0.32"))

    def test_safari_only(self):
        self.assertEqual("Safari", device("Not a legit OS Safari/5.2"))

    def test_linux_only(self):
        self.assertEqual("Linux", device("Linux not a real browser/10.3"))

    def test_ipad_only(self):
        self.assertEqual("iPad", device("iPad not a real browser/10.3"))

    def test_iphone_only(self):
        self.assertEqual("iPhone", device("iPhone not a real browser/10.3"))

    def test_windowsxp_only(self):
        self.assertEqual("Windows XP", device("NT 5.1 not a real browser/10.3"))

    def test_windowsvista_only(self):
        self.assertEqual("Windows Vista", device("NT 6.0 not a real browser/10.3"))

    def test_windows7_only(self):
        self.assertEqual("Windows 7", device("NT 6.1 not a real browser/10.3"))

    def test_windows8_only(self):
        self.assertEqual("Windows 8", device("NT 6.2 not a real browser/10.3"))

    def test_windows81_only(self):
        self.assertEqual("Windows 8.1", device("NT 6.3 not a real browser/10.3"))

    def test_windows_only(self):
        self.assertEqual("Windows", device("Windows not a real browser/10.3"))


class ClearsessionsCommandTest(TestCase):
    def test_can_call(self):
        Session.objects.create(expire_date=datetime.now() - timedelta(days=1),
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
