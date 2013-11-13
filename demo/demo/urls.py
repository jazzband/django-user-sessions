from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from extended_sessions.views import SessionListView, SessionDeleteView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=RedirectView.as_view(url=reverse_lazy('session_list')),
        name='home',
    ),
    url(
        regex=r'^sessions/$',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    url(
        regex=r'^sessions/(?P<pk>\w+)/delete/$',
        view=SessionDeleteView.as_view(
            success_url=reverse_lazy('session_list')),
        name='session_delete',
    ),
    url(r'^admin/', include(admin.site.urls)),
)
