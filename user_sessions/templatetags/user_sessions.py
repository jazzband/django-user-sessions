import re
import warnings

from django import template
from django.contrib.gis.geoip2 import HAS_GEOIP2
from django.utils.translation import gettext_lazy as _

register = template.Library()

BROWSERS = (
    (re.compile('Edg'), _('Edge')),
    (re.compile('OPR'), _('Opera')),
    (re.compile('Chrome'), _('Chrome')),
    (re.compile('Safari'), _('Safari')),
    (re.compile('Firefox'), _('Firefox')),
    (re.compile('IE'), _('Internet Explorer')),
)
PLATFORMS = (
    (re.compile('Windows Mobile'), _('Windows Mobile')),
    (re.compile('Android'), _('Android')),
    (re.compile('Linux'), _('Linux')),
    (re.compile('iPhone'), _('iPhone')),
    (re.compile('iPad'), _('iPad')),
    (re.compile('Mac OS X 10[._]9'), _('OS X Mavericks')),
    (re.compile('Mac OS X 10[._]10'), _('OS X Yosemite')),
    (re.compile('Mac OS X 10[._]11'), _('OS X El Capitan')),
    (re.compile('Mac OS X 10[._]12'), _('macOS Sierra')),
    (re.compile('Mac OS X 10[._]13'), _('macOS High Sierra')),
    (re.compile('Mac OS X 10[._]14'), _('macOS Mojave')),
    (re.compile('Mac OS X 10[._]15'), _('macOS Catalina')),
    (re.compile('Mac OS X'), _('macOS')),
    (re.compile('NT 5.1'), _('Windows XP')),
    (re.compile('NT 6.0'), _('Windows Vista')),
    (re.compile('NT 6.1'), _('Windows 7')),
    (re.compile('NT 6.2'), _('Windows 8')),
    (re.compile('NT 6.3'), _('Windows 8.1')),
    (re.compile('NT 10.0'), _('Windows 10')),
    (re.compile('Windows'), _('Windows')),
)


@register.filter
def platform(value):
    """
    Transform the platform from a User Agent into human readable text.

    Example output:

    * iPhone
    * Windows 8.1
    * macOS
    * Linux
    * None
    """

    platform = None
    for regex, name in PLATFORMS:
        if regex.search(value):
            platform = name
            break

    return platform


@register.filter
def browser(value):
    """
    Transform the browser from a User Agent into human readable text.

    Example output:

    * Safari
    * Chrome
    * Safari
    * Firefox
    * None
    """

    browser = None
    for regex, name in BROWSERS:
        if regex.search(value):
            browser = name
            break

    return browser


@register.filter
def device(value):
    """
    Transform a User Agent into human readable text.

    Example output:

    * Safari on iPhone
    * Chrome on Windows 8.1
    * Safari on macOS
    * Firefox
    * Linux
    * None
    """

    browser_ = browser(value)
    platform_ = platform(value)

    if browser_ and platform_:
        return _('%(browser)s on %(device)s') % {
            'browser': browser_,
            'device': platform_
        }

    if browser_:
        return browser_

    if platform_:
        return platform_

    return None


@register.filter
def city(value):
    location = geoip() and geoip().city(value)
    if location and location['city']:
        return location['city']
    return None


@register.filter
def country(value):
    location = geoip() and geoip().country(value)
    if location and location['country_name']:
        return location['country_name']
    return None


@register.filter
def location(value):
    """
    Transform an IP address into an approximate location.

    Example output:

    * Zwolle, The Netherlands
    * The Netherlands
    * None
    """
    try:
        location = geoip() and geoip().city(value)
    except Exception:
        try:
            location = geoip() and geoip().country(value)
        except Exception as e:
            warnings.warn(str(e), stacklevel=2)
            location = None
    if location and location['country_name']:
        if 'city' in location and location['city']:
            return f"{location['city']}, {location['country_name']}"
        return location['country_name']
    return None


_geoip = None


def geoip():
    global _geoip
    if _geoip is None:
        if HAS_GEOIP2:
            from django.contrib.gis.geoip2 import GeoIP2
            try:
                _geoip = GeoIP2()
            except Exception as e:
                warnings.warn(str(e), stacklevel=2)
    return _geoip
