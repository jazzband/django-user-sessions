from collections import OrderedDict
import re
import warnings

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext

try:
    from django.contrib.gis.geoip import GeoIP
    geoip = GeoIP()
except Exception as e:
    warnings.warn(str(e))
    geoip = None

register = template.Library()

BROWSERS = OrderedDict((
    (re.compile('Safari'), _('Safari')),
    (re.compile('Firefox'), _('Firefox')),
    (re.compile('Chrome'), _('Chrome')),
    (re.compile('Opera'), _('Opera')),
    (re.compile('MSIE'), _('Internet Explorer')),
))
DEVICES = OrderedDict((
    (re.compile('iPhone'), _('iPhone')),
    (re.compile('iPad'), _('iPad')),
    (re.compile('(Macintosh|OS_X)'), _('Mac OS X')),
    (re.compile('Apple'), _('Apple')),
    (re.compile('Android'), _('Android')),
    (re.compile('NT 5.1'), _('Windows XP')),
    (re.compile('NT 6.0'), _('Windows Vista')),
    (re.compile('NT 6.1'), _('Windows 7')),
    (re.compile('NT 6.2'), _('Windows 8')),
    (re.compile('Windows'), _('Windows')),
    (re.compile('Linux'), _('Linux')),
))


@register.filter
def humanagent(value):
    for regex, name in BROWSERS.items():
        if regex.search(value):
            browser = name
            break
    else:
        browser = 'unknown'
    for regex, name in DEVICES.items():
        if regex.search(value):
            device = name
            break
    else:
        device = 'unknown'
    return _('%s on %s') % (browser, device)


@register.filter
def location(value):
    location = geoip and geoip.city(value)
    if location and location['country_name']:
        if location['city']:
            return '%s, %s' % (location['city'], location['country_name'])
        else:
            return location['country_name']
    return mark_safe('<i>%s</i>' % ugettext('unknown'))
