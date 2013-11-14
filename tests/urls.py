from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.http import HttpResponse


admin.autodiscover()


def empty(request):
    return HttpResponse('')


def modify_session(request):
    request.session['FOO'] = 'BAR'
    return HttpResponse('')


urlpatterns = patterns(
    '',
    url(r'^$', empty),
    url(r'^modify_session/$', modify_session),
    url(r'^admin/', include(admin.site.urls)),
)
