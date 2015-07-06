from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=RedirectView.as_view(
            url=reverse_lazy('user_sessions:session_list'),
            permanent=True,
        ),
        name='home',
    ),
    url(r'', include('user_sessions.urls', 'user_sessions')),
    url(r'^admin/', include(admin.site.urls)),
)
