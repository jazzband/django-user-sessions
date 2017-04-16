import re
import warnings

from django import template
from django.utils.translation import ugettext_lazy as _

try:
    # Django 1.9 and above
    from django.contrib.gis.geoip2 import HAS_GEOIP2
    HAS_GEOIP = False
except:
    # Django 1.8
    from django.contrib.gis.geoip import HAS_GEOIP
    HAS_GEOIP2 = False


register = template.Library()

BROWSERS = (
    (re.compile('Chrome'), _('Chrome')),
    (re.compile('Safari'), _('Safari')),
    (re.compile('Firefox'), _('Firefox')),
    (re.compile('Opera'), _('Opera')),
    (re.compile('IE'), _('Internet Explorer')),
)
DEVICES = (
    (re.compile('Android'), _('Android')),
    (re.compile('Linux'), _('Linux')),
    (re.compile('iPhone'), _('iPhone')),
    (re.compile('iPad'), _('iPad')),
    (re.compile('(Mac OS X)'), _('OS X')),
    (re.compile('NT 5.1'), _('Windows XP')),
    (re.compile('NT 6.0'), _('Windows Vista')),
    (re.compile('NT 6.1'), _('Windows 7')),
    (re.compile('NT 6.2'), _('Windows 8')),
    (re.compile('NT 6.3'), _('Windows 8.1')),
    (re.compile('Windows'), _('Windows')),
)


@register.filter
def device(value):
    """
    Transform a User Agent into human readable text.

    Example output:

    * Safari on iPhone
    * Chrome on Windows 8.1
    * Safari on OS X
    * Firefox
    * Linux
    * None
    """

    browser = None
    for regex, name in BROWSERS:
        if regex.search(value):
            browser = name
            break

    device = None
    for regex, name in DEVICES:
        if regex.search(value):
            device = name
            break

    if browser and device:
        return _('%(browser)s on %(device)s') % {
            'browser': browser,
            'device': device
        }

    if browser:
        return browser

    if device:
        return device

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
        if location and location['country_name']:
            if location['city']:
                return '{}, {}'.format(location['city'], location['country_name'])
            return location['country_name']
    except:
        pass
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
                warnings.warn(str(e))
        elif HAS_GEOIP:
            from django.contrib.gis.geoip import GeoIP
            try:
                _geoip = GeoIP()
            except Exception as e:
                warnings.warn(str(e))
    return _geoip
