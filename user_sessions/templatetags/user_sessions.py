import re
import warnings

from django import template
from django.contrib.gis.geoip import HAS_GEOIP
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext

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
    Transform a User Agent into a human readable text.

    Example output:

    * Safari on iPhone
    * Chrome on Windows 8.1
    * Safari on OS X
    """

    for regex, name in BROWSERS:
        if regex.search(value):
            browser = name
            break
    else:
        browser = 'unknown'
    for regex, name in DEVICES:
        if regex.search(value):
            device = name
            break
    else:
        device = 'unknown'
    return _('%(browser)s on %(device)s') % {'browser': browser,
                                             'device': device}


@register.filter
def location(value):
    """
    Transform an IP address into an approximate location.

    Example output:

    * Zwolle, The Netherlands
    * ``<i>unknown</i>``
    """
    location = geoip() and geoip().city(value)
    if location and location['country_name']:
        if location['city']:
            return '%s, %s' % (location['city'], location['country_name'])
        else:
            return location['country_name']
    return mark_safe('<i>%s</i>' % ugettext('unknown'))


_geoip = None


def geoip():
    global _geoip
    if _geoip is None and HAS_GEOIP:
        from django.contrib.gis.geoip import GeoIP
        try:
            _geoip = GeoIP()
        except Exception as e:
            warnings.warn(str(e))
    return _geoip
