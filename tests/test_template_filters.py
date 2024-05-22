from unittest import skipUnless

from django.test import TestCase
from django.test.utils import override_settings

from user_sessions.templatetags.user_sessions import (
    browser, city, country, device, location, platform,
)


try:
    from django.contrib.gis.geoip2 import GeoIP2
    geoip = GeoIP2()
    geoip_msg = None
except Exception as error_geoip2:  # pragma: no cover
    try:
        from django.contrib.gis.geoip import GeoIP
        geoip = GeoIP()
        geoip_msg = None
    except Exception as error_geoip:
        geoip = None
        geoip_msg = str(error_geoip2) + " and " + str(error_geoip)


class LocationTemplateFilterTest(TestCase):
    @override_settings(GEOIP_PATH=None)
    def test_no_location(self):
        with self.assertWarnsRegex(
            UserWarning,
            r"The address 127\.0\.0\.1 is not in the database",
        ):
            loc = location('127.0.0.1')
        self.assertEqual(loc, None)

    @skipUnless(geoip, geoip_msg)
    def test_city(self):
        self.assertEqual('San Diego', city('44.55.66.77'))

    @skipUnless(geoip, geoip_msg)
    def test_country(self):
        self.assertEqual('United States', country('8.8.8.8'))

    @skipUnless(geoip, geoip_msg)
    def test_locations(self):
        self.assertEqual('United States', location('8.8.8.8'))
        self.assertEqual('San Diego, United States', location('44.55.66.77'))


class PlatformTemplateFilterTest(TestCase):
    def test_windows(self):
        # Generic Windows
        self.assertEqual("Windows", platform("Windows NT 5.1 not a real browser/10.3"))
        self.assertEqual("Windows", platform("Windows NT 6.0 not a real browser/10.3"))
        self.assertEqual("Windows", platform("Windows NT 6.1 not a real browser/10.3"))
        self.assertEqual("Windows", platform("Windows NT 6.2 not a real browser/10.3"))
        self.assertEqual("Windows", platform("Windows NT 6.3 not a real browser/10.3"))
        self.assertEqual("Windows", platform("Windows not a real browser/10.3"))

        # IE
        self.assertEqual(
            'Windows',
            platform('Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; '
                     '.NET CLR 2.0.50727)')
        )
        self.assertEqual(
            'Windows',
            platform('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; '
                     'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
                     ' InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; '
                     'MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3;'
                     ' .NET CLR 3.0.30729)')
        )
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                     'Trident/6.0)')
        )
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; '
                     'Win64; x64; Trident/6.0)')
        )
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; '
                     '.NET4.0E; .NET4.0C; rv:11.0) like Gecko')
        )

        # Edge
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, '
                     'like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136')
        )
        self.assertEqual(
            'Windows Mobile',
            platform('Mozilla/5.0 (Windows Mobile 10; Android 8.0.0; Microsoft; Lumia '
                     '950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.62 '
                     'Mobile Safari/537.36 Edge/40.15254.369')
        )

        # Edge Chromium
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 '
                     'Safari/537.36 Edg/81.0.416.62')
        )

        # Firefox
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) '
                     'Gecko/20130328 Firefox/22.0')
        )

        # Chrome
        self.assertEqual(
            'Windows',
            platform('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ('
                     'KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')
        )

    def test_apple(self):
        # Generic iPad
        self.assertEqual("iPad", platform("iPad not a real browser/10.3"))

        # Generic iPhone
        self.assertEqual("iPhone", platform("iPhone not a real browser/10.3"))

        self.assertEqual(
            'iPad',
            platform('Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) '
                     'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
                     'Mobile/8C148 Safari/6533.18.5')
        )

        self.assertEqual(
            'iPhone',
            platform('Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) '
                     'AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
                     'Mobile/11A465 Safari/9537.53')
        )

        self.assertEqual(
            'macOS',
            platform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/85.0.4178.0 Safari/537.36')
        )
        self.assertEqual(
            'macOS',
            platform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) '
                     'Gecko/20100101 Firefox/77.0')
        )
        self.assertEqual(
            'macOS',
            platform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
                     'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
                     'Safari/536.26.17')
        )

        # Edge Chromium
        self.assertEqual(
            'macOS',
            platform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 '
                     'Safari/537.36 Edg/85.0.564.51')
        )

    def test_android(self):
        # androids identify themselves as Safari to get the good stuff
        self.assertEqual(
            'Android',
            platform('Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic '
                     'Build/CRB17) AppleWebKit/528.5+ (KHTML, like Gecko) '
                     'Version/3.1.2 Mobile Safari/525.20.1')
        )

        # Edge Chromium
        self.assertEqual(
            'Android',
            platform('Mozilla/5.0 (Linux; Android 11; Pixel 3 XL) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 '
                     'Mobile Safari/537.36 EdgA/45.07.4.5059')
        )

    def test_linux_only(self):
        self.assertEqual("Linux", platform("Linux not a real browser/10.3"))


class BrowserTemplateFilterTest(TestCase):
    def test_ie(self):
        self.assertEqual(
            'Internet Explorer',
            browser('Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; '
                    '.NET CLR 2.0.50727)')
        )
        self.assertEqual(
            'Internet Explorer',
            browser('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; '
                    'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
                    ' InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; '
                    'MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3;'
                    ' .NET CLR 3.0.30729)')
        )
        self.assertEqual(
            'Internet Explorer',
            browser('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                    'Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer',
            browser('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; '
                    'Win64; x64; Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer',
            browser('Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; '
                    '.NET4.0E; .NET4.0C; rv:11.0) like Gecko')
        )

    def test_edge(self):
        self.assertEqual(
            'Edge',
            browser('Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, '
                    'like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136')
        )
        self.assertEqual(
            'Edge',
            browser('Mozilla/5.0 (Windows Mobile 10; Android 8.0.0; Microsoft; Lumia '
                    '950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.62 '
                    'Mobile Safari/537.36 Edge/40.15254.369')
        )

    def test_edge_chromium(self):
        self.assertEqual(
            'Edge',
            browser('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 '
                    'Safari/537.36 Edg/81.0.416.62')
        )
        self.assertEqual(
            'Edge',
            browser('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 '
                    'Safari/537.36 Edg/85.0.564.51')
        )
        self.assertEqual(
            'Edge',
            browser('Mozilla/5.0 (Linux; Android 11; Pixel 3 XL) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 '
                    'Mobile Safari/537.36 EdgA/45.07.4.5059')
        )

    def test_safari(self):
        self.assertEqual(
            'Safari',
            browser('Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) '
                    'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
                    'Mobile/8C148 Safari/6533.18.5')
        )
        self.assertEqual(
            'Safari',
            browser('Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) '
                    'AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
                    'Mobile/11A465 Safari/9537.53')
        )
        self.assertEqual(
            'Safari',
            browser('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
                    'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
                    'Safari/536.26.17')
        )

        self.assertEqual("Safari", browser("Not a legit OS Safari/5.2"))

    def test_chrome(self):
        self.assertEqual(
            'Chrome',
            browser('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/85.0.4178.0 Safari/537.36')
        )

        self.assertEqual(
            'Chrome',
            browser('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ('
                    'KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')
        )

        self.assertEqual("Chrome", browser("Not a legit OS Chrome/54.0.32"))

    def test_firefox(self):
        self.assertEqual(
            'Firefox',
            browser('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) '
                    'Gecko/20100101 Firefox/77.0')
        )

        self.assertEqual(
            'Firefox',
            browser('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) '
                    'Gecko/20130328 Firefox/22.0')
        )

        self.assertEqual("Firefox", browser("Not a legit OS Firefox/51.0"))

    def test_android(self):
        # androids identify themselves as Safari to get the good stuff
        self.assertEqual(
            'Safari',
            browser('Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic '
                    'Build/CRB17) AppleWebKit/528.5+ (KHTML, like Gecko) '
                    'Version/3.1.2 Mobile Safari/525.20.1')
        )


class DeviceTemplateFilterTest(TestCase):
    def test_ie(self):
        self.assertEqual(
            'Internet Explorer on Windows',
            device('Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; '
                   '.NET CLR 2.0.50727)')
        )
        self.assertEqual(
            'Internet Explorer on Windows',
            device('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; '
                   'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
                   ' InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; '
                   'MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3;'
                   ' .NET CLR 3.0.30729)')
        )
        self.assertEqual(
            'Internet Explorer on Windows',
            device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                   'Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer on Windows',
            device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; '
                   'Win64; x64; Trident/6.0)')
        )
        self.assertEqual(
            'Internet Explorer on Windows',
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
            'Chrome on macOS',
            device('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/85.0.4178.0 Safari/537.36')
        )
        self.assertEqual(
            'Firefox on macOS',
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
            'Firefox on Windows',
            device('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) '
                   'Gecko/20130328 Firefox/22.0')
        )

    def test_chrome(self):
        self.assertEqual(
            'Chrome on Windows',
            device('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ('
                   'KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')
        )

    def test_edge(self):
        self.assertEqual(
            'Edge on Windows',
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
            'Edge on Windows',
            device('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 '
                   'Safari/537.36 Edg/81.0.416.62')
        )
        self.assertEqual(
            'Edge on macOS',
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
        self.assertEqual("Windows", device("Windows NT 5.1 not a real browser/10.3"))

    def test_windowsvista_only(self):
        self.assertEqual("Windows", device("Windows NT 6.0 not a real browser/10.3"))

    def test_windows7_only(self):
        self.assertEqual("Windows", device("Windows NT 6.1 not a real browser/10.3"))

    def test_windows8_only(self):
        self.assertEqual("Windows", device("Windows NT 6.2 not a real browser/10.3"))

    def test_windows81_only(self):
        self.assertEqual("Windows", device("Windows NT 6.3 not a real browser/10.3"))

    def test_windows_only(self):
        self.assertEqual("Windows", device("Windows not a real browser/10.3"))
